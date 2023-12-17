from pymongo_get_database import get_database

db = get_database()
betsByDate = db["betsByDate"]

docData = betsByDate.find({})

for x in docData:
    print(x)
