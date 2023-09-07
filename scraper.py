import requests
import parser
from bs4 import element


def get_base_url() -> str:
    with open("secrets\\base_url.txt", "r") as f:
        base_url = f.read().strip()
    return base_url


def get_repacks(year_month="2023-09") -> list[dict]:
    print(f"SCRAPING {year_month}:")
    base_url = get_base_url()
    (year, month) = year_month.split("-")
    url = base_url + year + "/" + month + "/" + "page/"

    repacks: list[dict] = []

    i = 1
    while (response := requests.get(url + str(i))).status_code == 200:
        print(f"    <Page {i}>")
        html = response.text

        repacks_html: list[element.Tag] = parser.find(html)

        for repack_html in repacks_html:
            repack: dict | str = parser.parse(repack_html)

            # dont include repacks which failed to parse
            if isinstance(repack, dict):
                repacks.append(repack)
            else:
                print(repack)

        i += 1

    return repacks
