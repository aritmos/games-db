from scraper import get_repacks
from mongo_db import db_add_repacks


def to_year_month(year: int, month: int) -> str:
    return f"{year}-{month:02}"


def get_repack_wrapper(start_date: str, end_date: str):
    # runs backwars through each month given the dates provided (given in "yyyy-mm" format)
    # runs the scraper, parser, and database manager to add the entries
    # end date is not inclusive
    [year, month] = [int(x) for x in start_date.split("-")]
    [end_year, end_month] = [int(x) for x in end_date.split("-")]

    while (year, month) != (end_year, end_month):
        year_month = to_year_month(year, month)
        print(f"Scraping and parsing entries for {year_month}")

        repacks = get_repacks(year_month)

        print(f"{len(repacks)} repacks parsed.")
        print("Adding repacks to database:")

        db_add_repacks(repacks)

        month -= 1
        if month == 0:
            month = 12
            year -= 1


get_repack_wrapper("2020-12", "2016-06")
