from bs4 import BeautifulSoup, element


def find(response_text: str) -> list[element.Tag]:
    soup = BeautifulSoup(response_text, "html.parser")
    repacks = soup.find_all("article", class_="category-lossless-repack")
    return repacks


def parse(repack_html: element.Tag, redact=False) -> dict:
    a_tag = repack_html.find("h1", class_="entry-title").findChild("a")
    title = a_tag.string
    link = a_tag.attrs["href"]

    upload_date_str = repack_html.find(
        "time", class_="entry-date").attrs["datetime"][:10]
    upload_date = [int(x) for x in upload_date_str.split("-")]

    entry_content = repack_html.find(
        "div", class_="entry-content")  # .find("strong").string

    # Sometimes this has extra formatting and this fails
    try:
        release_num = entry_content.findChild(
            "h3").findChild("span").string.split(" ")[0][1:]
    except:
        print(f"ERROR: Failed to parse release number for '{title}'")
        return None

    # this could maybe fail and should be error checked for None
    info = [e.string for e in entry_content.find("p").find_all("strong")]

    # Sometimes there is no "Genres/Tags" info
    i = 0
    if len(info) == 4:
        genres = None
        i = -1
    else:
        try:
            genres = info[0].split(", ")
        except:
            genres = None

    try:
        companies = info[1+i].split(", ")
    except:
        companies = None

    langs = info[2+i]
    # repack size
    size = info[4+i]

    if redact:
        link = "<REDACTED>"

    repack = {
        "num": release_num,
        "title": title,
        "date": upload_date,
        "link": link,
        "genres": genres,
        "companies": companies,
        "langs": langs,
        "size": size
    }

    return repack
