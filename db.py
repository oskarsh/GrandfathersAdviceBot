import json
import os

def writeToUserAdviceJson(data):
    fname = "./userAdvice.json"
    a = []
    if not os.path.isfile(fname):
        a.append(data)
        with open(fname, mode='w') as f:
            f.write(json.dumps(a, indent=2))
    else:
        with open(fname) as feedsjson:
            feeds = json.load(feedsjson)

        feeds.append(data)
        with open(fname, mode='w') as f:
            f.write(json.dumps(feeds, indent=2))



def getAllAdvices():
    with open("./db.json") as db:
        return json.load(db)

def getAllUserAdvices():
    with open("./userAdvice.json") as db:
        return json.load(db)
    
def insertIntoLifeAdvices(data):
    # takes a quote and inserts into life advices
    advices = getAllAdvices()
    if not data in advices["life"]:
        advices["life"].append(data);
        with open("./db.json", mode='w') as f:
            f.write(json.dumps(advices, indent=2))

def insertIntoHealthAdvices(data):
    # takes a quote and inserts into life advices
    advices = getAllAdvices()
    if not data in advices["health"]:
        advices["health"].append(data);
        with open("./db.json", mode='w') as f:
            f.write(json.dumps(advices, indent=2))

def insertIntoCarrerAdvices(data):
    # takes a quote and inserts into life advices
    advices = getAllAdvices()
    if not data in advices["carrer"]:
        advices["carrer"].append(data);
        with open("./db.json", mode='w') as f:
            f.write(json.dumps(advices, indent=2))

def insertIntoFamilyAdvices(data):
    # takes a quote and inserts into life advices
    advices = getAllAdvices()
    if not data in advices["family"]:
        advices["family"].append(data);
        with open("./db.json", mode='w') as f:
            f.write(json.dumps(advices, indent=2))

def getLifeAdvicesFromDb():
    with open("./db.json") as db:
        advices = json.load(db)
        return advices["life"]

def getHealthAdvicesFromDb():
    lifeAdvices = []
    with open("./db.json") as db:
        advices = json.load(db)
        return advices["health"]

def getCarrerAdvicesFromDb():
    lifeAdvices = []
    with open("./db.json") as db:
        advices = json.load(db)
        return advices["carrer"]

def getFamilyAdvicesFromDb():
    lifeAdvices = []
    with open("./db.json") as db:
        advices = json.load(db)
        return advices["family"]
