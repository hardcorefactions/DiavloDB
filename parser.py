import json

toPush = []

with open("Databases.sql", "r", encoding="UTF-8") as f:
    text = f.read()
    text = text.split("-- Structure de la table `")
    for db in text:
        if "SQL Dump" in db:
            pass
        else:
            final = []
            dbLines = db.split("\n")
            dbName = dbLines[0].replace("`", "")
            for line in dbLines:
                if "--" in line:
                    pass
                elif line == dbName+"`":
                    pass
                elif line == "":
                    pass
                elif line == " ":
                    pass
                elif "varchar" in line.lower():
                    pass
                elif "charset" in line.lower():
                    pass
                elif "create table" in line.lower():
                    pass
                elif "insert into" in line.lower():
                    pass
                elif "commit" in line.lower():
                    pass
                elif "40101" in line.lower():
                    pass
                else:
                    data = {}
                    line = line.replace("'", '').replace("(", "").replace("),", "").replace(", ", ",").split(",")
                    if len(line[2]) == len("0abcb402d85829a9"): # Que pereza no?
                        builtSHA = "$SHA$"+line[2]+"$"+line[1]
                        data = {
                            "name": line[0],
                            "password": builtSHA,
                        }
                    else:
                        if line[2] == "NULL":
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
