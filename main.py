from scraper import get_repacks
from mongo_db import db_add_repacks


def to_year_month(year: int, month: int) -> str:
    return f"{year}-{month:02}"


def get_repack_wrapper(start_date: str, end_date: str):
    # Runs backwars through each month given the dates provided (given in "yyyy-mm" format).
    # Runs the scraper, parser, and database manager to add the entries.
    # End date is not inclusive.
    [year, month] = [int(x) for x in start_date.split("-")]
    [end_year, end_month] = [int(x) for x in end_date.split("-")]

    while (year, month) != (end_year, end_month):
        year_month = to_year_month(year, month)

        repacks = get_repacks(year_month)

        print(f"{len(repacks)} repacks parsed.")
        print("Adding repacks to database:")

        db_add_repacks(repacks)

        month -= 1
        if month == 0:
            month = 12
            year -= 1


# Go through all of the releases between Sept 2023 and July 2016.
get_repack_wrapper("2023-09", "2016-06")
