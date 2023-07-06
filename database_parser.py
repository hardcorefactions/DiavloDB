import json

toPush = []

with open("Databases.sql", "r", encoding="latin-1") as f:
    text = f.read()
    text = text.split("-- Structure de la table `")
    for db in text:
        if "SQL Dump" not in db:
            final = []
            dbLines = db.split("\n")
            dbName = dbLines[0].replace("`", "")
            for line in dbLines:
                if (
                    "--" not in line
                    and line != f"{dbName}`"
                    and line.strip() != ""
                    and "varchar" not in line.lower()
                    and "charset" not in line.lower()
                    and "create table" not in line.lower()
                    and "insert into" not in line.lower()
                    and "commit" not in line.lower()
                    and "40101" not in line.lower()
                ):
                    data = {}
                    line = line.replace("'", '').replace("(", "").replace("),", "").replace(", ", ",").split(",")
                    if len(line[2]) == 16:
                        builtSHA = f"$SHA${line[2]}${line[1]}"
                        data = {
                            "name": line[0],
                            "password": builtSHA,
                        }
                    elif line[2] == "NULL":
                        data = {
                            "name": line[0],
                            "password": line[1],
                        }
                    else:
                        data = {
                            "name": line[0],
                            "password": line[1],
                            "salt": line[2]
                        }
                    final.append(data)
            # Finished parsing.
            toPush.append({"dbName": dbName, "data": final})

for db in toPush:
    dbName = db["dbName"]
    dbData = db["data"]
    with open(f"output/{dbName}.json", "w") as f:
        json.dump(dbData, f)
