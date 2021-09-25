import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["movieScriptsDB"]
mycoll = mydb["movieScripts"]


def get_film_ids (sub):
    filmList = []
    filmIds = []

    scriptQuery = {"subtitles": sub}

    results = mycoll.find(scriptQuery)

    for r in results:
            filmList.append(r)
        
    for f in filmList:
            filmIds.append(f["_id"])
            
        
    return filmIds

def insert_script (id, kwlist, sblist):

    movieScript = {"keywords": kwlist, "subtitles":sblist, "_id": id}
    mstest = mycoll.insert_one(movieScript)




    
    
   
