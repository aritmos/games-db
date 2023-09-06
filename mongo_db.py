from pymongo import MongoClient


def db_connection(collection="games"):
    client = MongoClient("localhost", 27017)

    with open("secrets\\db_name.txt", "r") as f:
        db_name = f.read().strip()

    db = client[db_name]

    return db[collection]


def db_add_repacks(repacks: list[dict]):
    games = db_connection()
    inserted = 0
    updated = 0

    for repack in repacks:
        num = repack["num"]
        filter = {"num": num}

        matches = list(games.find(filter))

        match len(matches):
            case 0:
                games.insert_one(repack)
                inserted += 1
            case 1:
                external_repack_date = repack["date"]
                internal_repack_date = matches[0]["date"]

                if external_repack_date > internal_repack_date:
                    games.delete_one(filter)
                    games.insert_one(repack)
                    updated += 1
            case _:
                print(f"ERROR: 2 or more games with the upload number '{num}'")
                continue
    print(f"Inserted {inserted} games and updated {updated} games.")
