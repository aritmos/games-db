from bs4 import BeautifulSoup, element
import datetime


def find(response_text: str) -> list[element.Tag]:
    soup = BeautifulSoup(response_text, "html.parser")
    repacks = soup.find_all("article", class_="category-lossless-repack")
    return repacks


def parse_error(error_code: int, title: str | None) -> str:
    # Used for error logging
    # TODO: Does python have enums? If so then refactor.
    match error_code:
        case 0:
            return f"ERROR while parsing '{title}':\
                \n> search for `h1.entry-title` did not return a Tag"
        case 1:
            return f"ERROR while parsing '{title}':\
                \n> search for `h1.entry-title > ... > a` did not return a Tag"
        case 2:
            return f"ERROR while parsing '{title}':\
                \n> search for `time.entry-date` did not return a Tag"
        case 3:
            return f"ERROR while parsing '{title}':\
                \n> search for `h3 > span` did not return a Tag"
        case 4:
            return f"ERROR while parsing '{title}':\
                \n> search for `div.entry-content > ... > span`\
                did not return a Tag"
        case 5:
            return f"ERROR while parsing '{title}':\
                \n> release number could not be parsed"
        case 6:
            return f"ERROR while parsing '{title}':\
                \n> manual release number could not be parsed or was skipped"
        case 7:
            return f"ERROR while parsing '{title}':\
                \n> search for `div.entry-content > ... > p`\
                did not return a Tag"
        case _:
            return f"ERROR while parsing '{title}':\
            \n> < unknown error code >"


def manual_release_num(title: str | None, link: str) -> str | None:
    print(parse_error(5, title))
    print(link)
    num = input("Insert release number:\n>")
    if num == "":
        return None
    return num


def parse(repack_html: element.Tag, redact=False) -> dict | str:
    # lots of bulky code to accommodate for the union return types in bs4
    h1 = repack_html.find("h1", class_="entry-title")
    match h1:
        case element.Tag():
            pass
        case _:
            return parse_error(0, None)

    a = h1.findChild("a")
    match a:
        case element.Tag():
            pass
        case _:
            return parse_error(1, None)

    # these should always work without the need for None checks
    title = a.string
    link = a.attrs["href"]

    entry_date = repack_html.find("time", class_="entry-date")
    match entry_date:
        case element.Tag():
            pass
        case _:
            return parse_error(2, title)

    entry_date_str = entry_date.attrs["datetime"][:10]
    entry_date_fields = [int(x) for x in entry_date_str.split("-")]
    # tzinfo is added so lsp doesn't complain about the unpacking
    entry_date = datetime.datetime(*entry_date_fields, tzinfo=None)

    entry_content = repack_html.find("div", class_="entry-content")
    match entry_content:
        case element.Tag():
            pass
        case _:
            return parse_error(3, title)

    # Sometimes the repack number causing the parsing to fail
    release_num = entry_content.find("span")
    match release_num:
        case element.Tag():
            pass
        case _:
            return parse_error(4, title)

    # In some cases the release number has some additional formatting, flare, etc.
    # if the number cannot be simply cast into an int, it gets passed into manual
    # input. This is managed by the `manual_release_num` function.

    release_num_str = release_num.string
    if release_num_str is None:
        num = manual_release_num(title, link)
        if num is None:
            return parse_error(6, title)
    else:
        try:
            # split is in case one has '#0000 Updated'
            num = str(int(release_num_str.split(" ")[0][1:]))
        except ValueError:
            num = manual_release_num(title, link)
            if num is None:
                return parse_error(6, title)

    # this could maybe fail and should be error checked for None
    info_p = entry_content.find("p")
    match info_p:
        case element.Tag():
            pass
        case _:
            return parse_error(7, title)

    info = [e.string for e in info_p.find_all("strong")]

    # Sometimes the `Genres/Tags` field is missing.
    # In these cases we add it as `None`
    if len(info) == 4:
        info = [None] + info

    genres = None if info[0] is None else info[0].split(", ")
    companies = None if info[1] is None else info[1].split(", ")
    langs = info[2]
    size = info[4]

    if redact:
        link = "<REDACTED>"

    repack = {
        "num": num,
        "title": title,
        "date": entry_date,
        "link": link,
        "genres": genres,
        "companies": companies,
        "langs": langs,
        "size": size
    }

    return repack
