""" >> etanbloxed << """
"""Welcome to etanbloxxed's source code!"""
"""This is VERY MESSY, as it is a compilation of gpt'd and handwritten code, sorry!"""
# you're better off using Bloxstrap anyway...

# [ modules ]
import time
from pypresence import Presence
import requests
import os
import re
from notifypy import Notify
import json
import random
import traceback
import pickle

# [ configuration ]
if not os.path.exists("etanbloxxedconfig.pkl"):
    print("etanbloxxed config file not found! Please configure your settings.")
    thingo = {"UserID": 0, "ipinfoapi": 0, "RobloxDirectory": "/Applications/more/Roblox.app"}
    print("Enter in your Roblox user id. Leaving this blank will not show your Roblox profile picture on etanbloxxed.")
    thingo["UserID"] = input("UserID | ")
    print("Enter in an ipinfo.io api key. A free account can be created at https://ipinfo.io/signup, and a free api key can be created, granting you 50k requests a month. Leaving this blank will not give you server info whenever you join a Roblox server.")
    thingo["ipinfoapi"] = input("API key | ")
    print("Enter in where your Roblox app is located. Leave blank to use default (/Applications/more/Roblox.app)")
    temp = input("Directory | ")
    if not temp == "":
        thingo["RobloxDirectory"] = temp
    with open("etanbloxxedconfig.pkl", "wb") as file:
        pickle.dump(thingo, file)
    print("Configuration saved. To modify this, delete \"etanbloxxedconfig.pkl\" and reopen etanbloxxed.")

with open("etanbloxxedconfig.pkl", "rb") as file:
    thingo = pickle.load(file)

API_KEY = thingo["ipinfoapi"]
userid = thingo["UserID"]
robloxdir = thingo["RobloxDirectory"]

# [ variables ]
VERSION_NO = "macos_1.03.21"
TEST_MODE = False

CLIENT_ID = 1229562048640319616
log_path = os.path.expanduser("~/Library/Logs/Roblox")
RPC = Presence(client_id=CLIENT_ID)
cachedstatus = 0
cachedipadress = ""
hasRPCwithextras = False

placeid = ""
rootplaceid = ""
creatorname = ""
gamename = ""
imageassetid = ""
ServerType = "Public server"

notification = Notify()
notification.title = "etanbloxxed"

bloxstrapRPCCustomState = {}

# [ opening roblox ]
os.system(f"open {robloxdir}")
print("Roblox opened")

# [ functions ] 
def printDebug(text): # i rarely use this oops
    global TEST_MODE
    if TEST_MODE:
        print("DEBUG | " + text)

def getrandomtext(): # random text bc why not :3
    randomtext = ["github powered!", "hello chat", "go join etan's gamers group", "i love underrated roblox games", "inflation goes crazy"]
    if random.randint(1, 33) == 33:
        print("1 in 33 chance!")
        return "there is a 1 in 33 chance of this appearing :3"
    else:
        thechoice = random.choice(randomtext)
        return thechoice

def getgamedetails(place_id): # getting the details of the game, like name, publisher etc
    havetotryagain = False
    primaryurl = f"https://apis.roproxy.com/universes/v1/places/{place_id}/universe"
    primaryresponse = requests.get(primaryurl)
    if primaryresponse.status_code == 200:
        data = primaryresponse.json()
        if data and "universeId":
            universeId = data["universeId"]
        else:
            fallback_url = f"https://apis.roblox.com/universes/v1/places/{place_id}/universe"
            fallback_response = requests.get(fallback_url)
            if fallback_response.status_code == 200:
                fallback_data = fallback_response.json()
                if fallback_data and "universeId" in fallback_data:
                    universeId = fallback_data["universeId"]
    else:
        fallback_url = f"https://apis.roblox.com/universes/v1/places/{place_id}/universe"
        fallback_response = requests.get(fallback_url)
        if fallback_response.status_code == 200:
            fallback_data = fallback_response.json()
            if fallback_data and "universeId" in fallback_data:
                universeId = fallback_data["universeId"]
    
    primaryurl = f"https://games.roproxy.com/v1/games?universeIds={universeId}"
    primaryresponse = requests.get(primaryurl)
    if primaryresponse.status_code == 200:
        data = primaryresponse.json()["data"][0]
        if data:
            try:
                rootPlaceId = data["rootPlaceId"]
                name = data["name"]
                if data["creator"]["hasVerifiedBadge"]:
                    creator = f"by {data['creator']['name']} ☑️"
                else:
                    creator = f"by {data['creator']['name']}"
                return rootPlaceId, name, creator
            except KeyError:
                havetotryagain = True
        else:
            fallback_url = f"https://games.roblox.com/v1/games?universeIds={universeId}"
            fallback_response = requests.get(fallback_url)
            if fallback_response.status_code == 200:
                data = primaryresponse.json()["data"][0]
                if data:
                    try:
                        rootPlaceId = data["rootPlaceId"]
                        name = data["name"]
                        if data["creator"]["hasVerifiedBadge"]:
                            creator = f"by {data['creator']['name']} ☑️"
                        else:
                            creator = f"by {data['creator']['name']}"
                        return rootPlaceId, name, creator
                    except KeyError:
                        print("Couldn't find all info...")
                        return "", "", ""
    else:
        fallback_url = f"https://games.roblox.com/v1/games?universeIds={universeId}"
        fallback_response = requests.get(fallback_url)
        if fallback_response.status_code == 200:
                data = primaryresponse.json()["data"][0]
                if data:
                    try:
                        rootPlaceId = data["rootPlaceId"]
                        name = data["name"]
                        if data["creator"]["hasVerifiedBadge"]:
                            creator = f"by {data['creator']['name']} ☑️"
                        else:
                            creator = f"by {data['creator']['name']}"
                        return rootPlaceId, name, creator
                    except KeyError:
                        print("Couldn't find all info...")
                        return "", "", ""
    
    if havetotryagain:
        fallback_url = f"https://games.roblox.com/v1/games?universeIds={universeId}"
        fallback_response = requests.get(fallback_url)
        if fallback_response.status_code == 200:
                data = primaryresponse.json()["data"][0]
                if data:
                    try:
                        rootPlaceId = data["rootPlaceId"]
                        name = data["name"]
                        if data["creator"]["hasVerifiedBadge"]:
                            creator = f"by {data['creator']['name']} ☑️"
                        else:
                            creator = f"by {data['creator']['name']}"
                        return rootPlaceId, name, creator
                    except KeyError:
                        print("Couldn't find all info...")
                        return "", "", ""

def getUserPFP():
    global userid
    if userid == "":
        return "etanbloxxed_main"
    url = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={userid}&size=48x48&format=Png&isCircular=false"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["data"][0]["imageUrl"]
    else:
        return "etanbloxxed_main"

def getUsername():
    global userid
    if userid == "":
        return "etanbloxxed is a knockoff bloxstrap rpc, go check out bloxstrap!"
    url = f"https://users.roblox.com/v1/users/{userid}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["hasVerifiedBadge"]:
            return f"Playing as {data["displayName"]} ☑️ (@{data["name"]})"
        else:
            return f"Playing as {data["displayName"]} (@{data["name"]})"
    else:
        return "Failed to get user info!"

def getImageAssetId(rootplaceid): # game image
    primaryurl = f"https://economy.roproxy.com/v2/assets/{rootplaceid}/details"
    primaryresponse = requests.get(primaryurl)
    if primaryresponse.status_code == 200:
        data = primaryresponse.json()
        if data and "universeId":
            printDebug(f"getassetid --> asset id {data['IconImageAssetId']}")
            return data["IconImageAssetId"]
        else:
            fallback_url = f"https://economy.roblox.com/v2/assets/{rootplaceid}/details"
            fallback_response = requests.get(fallback_url)
            if fallback_response.status_code == 200:
                fallback_data = fallback_response.json()
                if fallback_data and "IconImageAssetId" in fallback_data:
                    printDebug(f"getassetid --> asset id {fallback_data['IconImageAssetId']}")
                    return fallback_data["IconImageAssetId"]
    else:
        fallback_url = f"https://economy.roblox.com/v2/assets/{rootplaceid}/details"
        fallback_response = requests.get(fallback_url)
        if fallback_response.status_code == 200:
            fallback_data = fallback_response.json()
            if fallback_data and "universeId" in fallback_data:
                printDebug(f"getassetid --> asset id {fallback_data['IconImageAssetId']}")
                return fallback_data["IconImageAssetId"]
    
    return ""

def updateRpc(newrpc, placeid, state): # yeah
    global hasRPCwithextras
    global imageassetid
    global bloxstrapRPCCustomState
    try:
        if not newrpc == "":
            RPC.update(details=f"Roblox - {newrpc}", state=state, large_image=f"https://assetdelivery.roblox.com/v1/asset/?id={imageassetid}", large_text=newrpc, small_image=getUserPFP(), small_text=getUsername(), start=time.time(), buttons=[{"label": "get etanbloxxed", "url": "https://github.com/etangaming123/etanbloxxed"}, {"label": "My Current Game", "url": f"https://www.roblox.com/games/{placeid}/"}])
            bloxstrapRPCCustomState = {"details": f"Roblox - {newrpc}", "state": state, "large_image": f"https://assetdelivery.roblox.com/v1/asset/?id={imageassetid}", "large_text": newrpc, "small_image": getUserPFP(), "small_text": getUsername(), "start": time.time(), "buttons": [{"label": "get etanbloxxed", "url": "https://github.com/etangaming123/etanbloxxed"}, {"label": "My Current Game", "url": f"https://www.roblox.com/games/{placeid}/"}]}
            print("RPC set to " + newrpc)
            hasRPCwithextras = True
        else:
            if not placeid == "":
                # this is when we have the placeid but getting the game name fails
                hasRPCwithextras = False
                RPC.update(details=f"Roblox - Game ID: {placeid}", state=state, large_image="etanbloxxed_main", large_text=placeid, small_image=getUserPFP(), small_text=getUsername(), start=time.time(), buttons=[{"label": "get etanbloxxed", "url": "https://github.com/etangaming123/etanbloxxed"}, {"label": "My Current Game", "url": f"https://www.roblox.com/games/{placeid}/"}])
            else:
                RPC.update(details=f"Roblox - Unknown Game", state=state, large_image="etanbloxxed_error", large_text="idk what this guys playing", small_image=getUserPFP(), small_text=getUsername(), start=time.time(), buttons=[{"label": "get etanbloxxed", "url": "https://github.com/etangaming123/etanbloxxed"}])
            print("RPC set with default message")
    except Exception as e:
        print("An error occured while setting RPC: " + str(e))
        traceback.print_exc()

def updateCustomRPC(command_data, gamename, current_state, imageid): # when games have [BloxstrapRPC]
    global placeid
    if command_data["command"] == "SetRichPresence":
        data = command_data["data"]
        printDebug(f"command data --> {str(command_data)}\ncurrentstateinput --> {str(current_state)}")
        if "state" in data:
            if data["state"] == "":
                current_state["state"] = f"Roblox - {gamename}"
            else:
                current_state["state"] = data["state"]
        if "details" in data:
            current_state["details"] = data["details"]
        if "largeImage" in data:
            if "assetId" in data["largeImage"]:
                current_state["large_image"] = f"https://assetdelivery.roblox.com/v1/asset/?id={data['largeImage']['assetId']}"
            if "hoverText" in data["largeImage"]:
                current_state["large_text"] = data["largeImage"]["hoverText"]
        if "smallImage" in data:
            if "assetId" in data["smallImage"]:
                current_state["small_image"] = f"https://assetdelivery.roblox.com/v1/asset/?id={data['smallImage']['assetId']}"
            if "hoverText" in data["smallImage"]:
                current_state["small_text"] = data["smallImage"]["hoverText"]

        start_time = data.get("timeStart")
        end_time = data.get("timeEnd")
        if start_time is not None and end_time is not None:
            if start_time == 0 or end_time == 0 or start_time > end_time:
                if "start" in current_state:
                    del current_state["start"]
                if "end" in current_state:
                    del current_state["end"]
            else:
                current_state["start"] = start_time
                current_state["end"] = end_time
        
        current_state["buttons"] = [{"label": "get etanbloxxed", "url": "https://github.com/etangaming123/etanbloxxed"}, {"label": "My Current Game", "url": f"https://www.roblox.com/games/{placeid}/"}]
        printDebug(f"current state --> {str(current_state)}")
        RPC.update(**current_state)
        print(f"state = {current_state['state']}, details = {current_state['details']}")

def idleRpc(): # set rpc to idle
    global hasRPCwithextras
    hasRPCwithextras = False
    try:
        RPC.update(details="Roblox", state="On the home screen", large_image="etanbloxxed_idle", large_text=getrandomtext(), small_image=getUserPFP(), small_text=getUsername(), buttons=[{"label": "get etanbloxxed", "url": "https://github.com/etangaming123/etanbloxxed"}])
    except Exception as e:
        traceback.print_exc()
        print("An error occured while setting RPC: " + str(e))

def get_geolocation(ip_address): # get the country of a server
    if API_KEY == "":
        return "None"
    url = f'https://ipinfo.io/{ip_address}?token={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"An error occured while getting location: {response.status_code}")
        return "None"

def find_latest_log_file(directory): # gpt written
    files = [os.path.join(directory, f) for f in os.listdir(directory)]
    files = [f for f in files if os.path.isfile(f)]
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

def follow(thefile): # also gpt written
    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

print(f"Welcome to etanbloxxed!\nThis is basically bloxstrap but for macos and poorly optimised\n\nYou are running version {VERSION_NO}.\n")
if __name__ == "__main__": # idk why but gpt added this so (im kidding it has somethign to do with modules or something IDK)
    while True:
        try:
            print("Connecting to Discord...")
            Presence.connect(self=RPC)
            idleRpc()
            print("Connected to Discord")
            break
        except Exception as e:
            print("Failed to connect to Discord: " + str(e))
            traceback.print_exc()
            exit()

    print("\nFinding latest log file...")
    log_file = find_latest_log_file(log_path)
    print("Scanning log file " + log_file)
    with open(log_file, "r", encoding="utf-8") as logfile:
        while True:
            try:
                    loglines = follow(logfile)
                    for line in loglines:
                        if "GameJoinUtil::joinGamePost" in line: # Handle request to join
                            if "GameJoinUtil::joinGamePostPrivateServer" in line:
                                ServerType = "Private Server"
                            else:
                                ServerType = "Public Server"
                            match = re.search(r'BODY: ({.*})', line)
                            if match:
                                print("Finding game information...")
                                json_str = match.group(1)
                                jsondata = json.loads(json_str)

                                placeid = jsondata.get("placeId")
                                if placeid:
                                    rootplaceid, gamename, creatorname = getgamedetails(placeid)
                                    imageassetid = getImageAssetId(rootplaceid)
                                else:
                                    print("No placeid found!") # this almost never happens unless roblox changes the way it works
                        
                        if "GameJoinUtil::initiateTeleportToReservedServer" in line:
                            ServerType = "Reserved Server"
                            match = re.search(r'"placeId":(\d+)', line)
                            if match:
                                placeid = match.group(1)
                                rootplaceid, gamename, creatorname = getgamedetails(placeid)
                                imageassetid = getImageAssetId(rootplaceid)
                            else:
                                print("No placeid found!")

                        if "GameJoinUtil::initiateTeleportToPlace" in line:
                            pattern = r'"placeId":(\d+)'
                            match = re.search(pattern, line)
                            if match:
                                placeid = match.group(1)
                                rootplaceid, gamename, creatorname = getgamedetails(placeid)
                                imageassetid = getImageAssetId(rootplaceid)
                            else:
                                print("No placeid found!")

                        if "Replicator destroyed" in line and cachedstatus == 1: # Handle player leaving game
                            print("Detected disconnect!")
                            bloxstrapRPCCustomState.clear()
                            idleRpc()
                            cachedstatus = 0
                            
                        if "Connecting to UDMUX server" in line and cachedstatus == 0: # Handle player actually connecting to server (this mostly happens after getting the place information)
                            cachedstatus = 1
                            match = re.search(r'UDMUX server (\d+\.\d+\.\d+\.\d+)', line)
                            if match:
                                cachedipadress = match.group(1)
                                geolocationinfo = get_geolocation(cachedipadress) # Get geolocation of current server
                                print("IP Address of UDMUX server:", cachedipadress)
                                print("Connected to: " + geolocationinfo.get('city') + ", " + geolocationinfo.get('region'))
                                if not gamename == "":
                                    notification.message = "Location: " + geolocationinfo.get('city') + ", " + geolocationinfo.get('region') + "\nGame: " + gamename
                                    if ServerType == "Private Server":
                                        updateRpc(gamename, placeid, ServerType)
                                    else:
                                        updateRpc(gamename, placeid, creatorname)
                                else:
                                    notification.message = "Location: " + geolocationinfo.get('city') + ", " + geolocationinfo.get('region') + "\nFailed to detect game!"
                                    updateRpc("", "", ServerType)
                                notification.send()
                            else:
                                notification.message = "No IP found!"
                                notification.send()
                                print("No IP Address found") # This doesn't happen i hope
                
                        if "destroyLuaApp: (stage:LuaApp) blocking:true." in line: # Handle roblox closing
                            print("Detected Roblox client closed, closing RPC...")
                            RPC.close()
                            print("Goodbye!")
                            exit()
                
                        if "Found new version and the updater launched. Drain reporting and quit." in line: # Handle roblox updating
                            print("Roblox client is updating, please run RobloxPatcher.py to patch Roblox again\n(run the script after it updates)")
                            RPC.close()
                            exit()

                        if "[BloxstrapRPC]" in line: # ohhh crap bloxstrap rpc !!
                            rpc_data = line.split("[BloxstrapRPC] ")[1].strip()
                            command_data = json.loads(rpc_data)
                            updateCustomRPC(command_data, gamename, bloxstrapRPCCustomState, imageassetid)
                        
                        time.sleep(0)

            except Exception as e:
                if not "'utf-8' codec can't decode" in str(e): # Ignore that error
                    print("An error occured in loop: " + str(e))
            
            except KeyboardInterrupt: 
                print("Ctrl + c detected, closing RPC...")
                RPC.close()
                print("Goodbye!")
                exit()
else:
    print("HOW")