'''
Uses downloaded Instagram data to compare your following list with your followers list
'''
import json
import os

following = {
    "path": "/followers_and_following/following.json",
    "key": "relationships_following"
}
followers = {
    "path" : "/followers_and_following/followers.json",
    "key": "relationships_followers"
}

def getValuesFromJsonFile(dataFolder, typeObject):
    f = open(dataFolder + typeObject["path"])
    data = json.load(f)

    result = set()
    
    for userData in data[typeObject["key"]]:
        result.add(userData["string_list_data"][0]["value"])

    return result

def getUsersNotFollowingBack(dataFolder):
    # Gather set of Following and set of Followers
    followingSet = getValuesFromJsonFile(dataFolder, following)
    followersSet = getValuesFromJsonFile(dataFolder, followers)

    # For every user in your Followers, remove them from the set of Following
    for user in followersSet:
        if user in followingSet:
            followingSet.remove(user)

    return {
        "count": len(followingSet),
        "users": list(followingSet),
        }

print("Place the downloaded JSON instagram data in the same folder as this program (" + os.getcwd() +")")
while True:
    availableFolders = next(os.walk('.'))[1]

    if len(availableFolders) == 1:
        DATA_FOLDER_PATH = availableFolders[0]
    else:
        print("Available folders in current directory:")
        for f in availableFolders:
            print("\t" + f)
        DATA_FOLDER_PATH = input("Enter downloaded data folder name: ")

    if DATA_FOLDER_PATH in next(os.walk('.'))[1]:
        break
    else:
        print("ERROR Folder does not exist in current directory: " + DATA_FOLDER_PATH + "")
        exit()
    
notFollowingBackData = getUsersNotFollowingBack(DATA_FOLDER_PATH)

with open("./usersNotFollowingBack.json", "w") as outputFile:
    jsonObject = json.dumps(notFollowingBackData, indent=4)
    outputFile.write(jsonObject)
    print(os.getcwd() + "/usersNotFollowingBack.json has been created")