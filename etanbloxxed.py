''' >> etanbloxed << '''
'''Welcome to etanbloxxed's source code!'''
'''This is VERY MESSY, as it is a compilation of gpt'd and handwritten code, sorry!'''
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
import subprocess

# [ variables ]
VERSION_NO = 'RELEASE_1.00.04'
CONFIG_NO = '1.00.00'
DEBUG = False

CLIENT_ID = 1229562048640319616
log_path = os.path.expanduser('~/Library/Logs/Roblox')
RPC = Presence(client_id=CLIENT_ID)
cachedstatus = 0
cachedipadress = ''
hasRPCwithextras = False
close = False
timesthestupidlagmessagehasbeenspammed = 0
sentlagnotification = False 

placeid = ''
rootplaceid = ''
creatorname = ''
gamename = ''
imageassetid = ''
ServerType = 'Public server'

notification = Notify()
notification.title = 'etanbloxxed'

bloxstrapRPCCustomState = {}

# [ functions ] 
# --internal--
def printDebug(text): # i dont think there is a SINGLE occurence of me using this at the time of writing this comment
    global DEBUG
    if DEBUG:
        print('DEBUG | ' + str(text))

def printTemporary(text):
    print(text, end='\r')

def clear():
    print('                                                      ', end='\r')

def getrandomtext(): # random text bc why not :3 // you can change these if you want to 
    randomtext = ['github powered!', 'hello chat', 'go join etan\'s gamers group', 'i love underrated roblox games', 'inflation goes crazy']
    if random.randint(1, 33) == 33:
        print('1 in 33 chance!')
        return 'there is a 1 in 33 chance of this appearing :3' # you can also change this
    else:
        thechoice = random.choice(randomtext)
        return thechoice

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

def find_latest_modified_directory(folder_path): # also also gpt written
  latest_modified_dir = None
  latest_modification_time = 0

  for dir_name in os.listdir(folder_path):
    dir_path = os.path.join(folder_path, dir_name)
    if os.path.isdir(dir_path):
      modification_time = os.path.getmtime(dir_path)
      if modification_time > latest_modification_time:
        latest_modified_dir = dir_path
        latest_modification_time = modification_time

  return latest_modified_dir

def askforyesorno(ask): # not gpt written surprisingly
    yesdefinitions = ['yes', 'y', 'true', 'yeah']
    nodefinitions = ['no', 'n', 'false', 'nah']
    while True:
        userinput = input(ask)
        if userinput.lower() in yesdefinitions:
            return True
        elif userinput.lower() in nodefinitions:
            return False
        else:
            print('Could not tell if that was a yes or no')

def askconfiguration(): # im gonna rewrite this bruh
    thingo = {'configVer': '1.00.00', 'UserID': 0, 'ipinfoapi': 0, 'isWindows': False, 'RobloxDirectory': '/Applications/Roblox.app'}
    print('Enter in your Roblox user id. Leaving this blank will not show your Roblox profile picture on etanbloxxed.')
    thingo['UserID'] = input('UserID | ')
    print('Enter in an ipinfo.io api key. A free account can be created at https://ipinfo.io/signup, and a free api key can be created, granting you 50k requests a month. Leaving this blank will not give you server info whenever you join a Roblox server.')
    thingo['ipinfoapi'] = input('API key | ')
    print('Are you running a windows machine?')
    thingo['isWindows'] = askforyesorno('Windows or not | ')
    if not thingo['isWindows']:
        print('Enter in where your Roblox app is located. Leave blank to use default (/Applications/Roblox.app)')
        temp = input('Directory | ')
        if not temp == '':
            thingo['RobloxDirectory'] = temp
    return thingo

# --requests--
# MESSY CODE AHEAD BTW
def getgamedetails(place_id): # getting the details of the game, like name, publisher etc
    attemptno = 1
    while True:
        printTemporary(f'Getting game universe id... Attempt {attemptno}')
        try:
            url = f'https://apis.roblox.com/universes/v1/places/{place_id}/universe'
            response = requests.get(url) 
            data = response.json()
            if data and 'universeId':
                universeId = data['universeId']
                break
        except Exception:
            attemptno += 1
            time.sleep(1)
            clear()
    attemptno = 1
    clear()
    while True:
        try:
            printTemporary(f'Getting game details... Attempt {attemptno}')
            url = f'https://games.roblox.com/v1/games?universeIds={universeId}'
            response = requests.get(url)
            notrealdatalol = response.json()
            if notrealdatalol:
                data = notrealdatalol.get('data')[0]
                rootPlaceId = data['rootPlaceId']
                name = data['name']
                if data['creator']['hasVerifiedBadge']:
                    creator = f'by {data["creator"]["name"]} ☑️'
                else:
                    creator = f'by {data["creator"]["name"]}'
                if rootPlaceId is not None and name is not None and creator is not None:
                    clear()
                    break
        except Exception:
            attemptno += 1
            time.sleep(1)
            clear()
    clear()
    print('Got game details!')
    return rootPlaceId, name, creator

def getUserPFP(): # user pfp as url so that it shows up on discord
    global userid
    if userid == '':
        return 'etanbloxxed_main'
    attemptno = 1
    while True:
        printTemporary(f'Getting user thumbnail... Attempt {attemptno}')
        try:
            url = f'https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={userid}&size=48x48&format=Png&isCircular=false'
            response = requests.get(url)
            data = response.json()
            clear()
            return data['data'][0]['imageUrl']
        except Exception:
            attemptno += 1
            time.sleep(1)
            clear()

def getUsername(): # username and displayname
    global userid
    if userid == '':
        return 'etanbloxxed is a knockoff bloxstrap rpc, go check out bloxstrap!'
    attemptno = 1
    while True:
        printTemporary(f'Getting username and displayname... Attempt {attemptno}')
        try:
            url = f'https://users.roblox.com/v1/users/{userid}'
            response = requests.get(url)
            data = response.json()
            if data['hasVerifiedBadge']:
                clear()
                return f'Playing as {data["displayName"]} ☑️ (@{data["name"]})'
            else:
                clear()
                return f'Playing as {data["displayName"]} (@{data["name"]})'
        except Exception:
            attemptno += 1
            time.sleep(1)
            clear()

def getImageAssetId(rootplaceid): # game image
    attemptno = 1
    while True:
        printTemporary(f'Getting image asset id... Attempt {attemptno}')
        try:
            url = f'https://economy.roblox.com/v2/assets/{rootplaceid}/details'
            response = requests.get(url)
            data = response.json()
            if data and 'universeId':
                clear()
                return data['IconImageAssetId']
        except Exception:
            attemptno += 1
            time.sleep(1)
            clear()

def get_geolocation(ip_address): # get the country of a server (this thing does not have a while true loop because we don't wanna waste all your requests, do we?)
    if API_KEY == '':
        return 'None'
    url = f'https://ipinfo.io/{ip_address}?token={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'An error occured while getting location: {response.status_code}')
        return 'None'

# --rpc--
def updateRpc(newrpc, placeid, state): # yeah
    global hasRPCwithextras
    global imageassetid
    global bloxstrapRPCCustomState
    try:
        if not newrpc == '':
            RPC.update(details=f'Roblox - {newrpc}', state=state, large_image=f'https://assetdelivery.roblox.com/v1/asset/?id={imageassetid}', large_text=newrpc, small_image=getUserPFP(), small_text=getUsername(), start=time.time(), buttons=[{'label': 'get etanbloxxed', 'url': 'https://github.com/etangaming123/etanbloxxed'}, {'label': 'My Current Game', 'url': f'https://www.roblox.com/games/{placeid}/'}])
            bloxstrapRPCCustomState = {'details': f'Roblox - {newrpc}', 'state': state, 'large_image': f'https://assetdelivery.roblox.com/v1/asset/?id={imageassetid}', 'large_text': newrpc, 'small_image': getUserPFP(), 'small_text': getUsername(), 'start': time.time(), 'buttons': [{'label': 'get etanbloxxed', 'url': 'https://github.com/etangaming123/etanbloxxed'}, {'label': 'My Current Game', 'url': f'https://www.roblox.com/games/{placeid}/'}]}
            print('RPC set to ' + newrpc)
            hasRPCwithextras = True
        else:
            if not placeid == '': # this is when we have the placeid but getting the game name fails
                hasRPCwithextras = False
                RPC.update(details=f'Roblox - Game ID: {placeid}', state=state, large_image='etanbloxxed_main', large_text=placeid, small_image=getUserPFP(), small_text=getUsername(), start=time.time(), buttons=[{'label': 'get etanbloxxed', 'url': 'https://github.com/etangaming123/etanbloxxed'}, {'label': 'My Current Game', 'url': f'https://www.roblox.com/games/{placeid}/'}])
            else:
                RPC.update(details=f'Roblox - Unknown Game', state=state, large_image='etanbloxxed_error', large_text='idk what this guys playing', small_image=getUserPFP(), small_text=getUsername(), start=time.time(), buttons=[{'label': 'get etanbloxxed', 'url': 'https://github.com/etangaming123/etanbloxxed'}])
            print('RPC set with default message')
    except Exception:
        print('An error occured while setting RPC!')
        traceback.print_exc()

def updateCustomRPC(command_data, gamename, current_state): # when games have [BloxstrapRPC]
    global placeid
    if command_data['command'] == 'SetRichPresence':
        data = command_data['data']
        if 'state' in data:
            if data['state'] == '':
                current_state['state'] = f'Roblox - {gamename}'
            else:
                current_state['state'] = data['state']
        if 'details' in data:
            current_state['details'] = data['details']
        if 'largeImage' in data:
            if 'assetId' in data['largeImage']:
                current_state['large_image'] = f"https://assetdelivery.roblox.com/v1/asset/?id={data['largeImage']['assetId']}"
            if 'hoverText' in data['largeImage']:
                current_state['large_text'] = data['largeImage']['hoverText']
        if 'smallImage' in data:
            if 'assetId' in data['smallImage']:
                current_state['small_image'] = f"https://assetdelivery.roblox.com/v1/asset/?id={data['smallImage']['assetId']}"
            if 'hoverText' in data['smallImage']:
                current_state['small_text'] = data['smallImage']['hoverText']

        start_time = data.get('timeStart')
        end_time = data.get('timeEnd')
        if start_time is not None and end_time is not None:
            if start_time == 0 or end_time == 0 or start_time > end_time:
                if 'start' in current_state:
                    del current_state['start']
                if 'end' in current_state:
                    del current_state['end']
            else:
                current_state['start'] = start_time
                current_state['end'] = end_time
        
        current_state['buttons'] = [{'label': 'get etanbloxxed', 'url': 'https://github.com/etangaming123/etanbloxxed'}, {'label': 'My Current Game', 'url': f'https://www.roblox.com/games/{placeid}/'}]
        RPC.update(**current_state)
        print(f'state = {current_state['state']}, details = {current_state['details']}')

def idleRpc(): # set rpc to idle
    global hasRPCwithextras
    hasRPCwithextras = False
    try:
        RPC.update(details='Roblox', state='On the home screen', large_image='etanbloxxed_idle', large_text=getrandomtext(), small_image=getUserPFP(), small_text=getUsername(), buttons=[{'label': 'get etanbloxxed', 'url': 'https://github.com/etangaming123/etanbloxxed'}])
    except Exception:
        traceback.print_exc()
        print('An error occured while setting RPC!')

# [ startup ]
if __name__ == '__main__': # idk why but gpt added this so (im kidding it has somethign to do with modules or something IDK)
    literally_all_the_new_features = ['What\'s new in the latest etanbloxxed update:', '> fstring errors fixed', 'that\'s pretty much it'] # no way new noticeboard
    print(f'Welcome to etanbloxxed!\nThis is basically bloxstrap but bad and poorly optimised\n\nYou are running version {VERSION_NO}.\n')
    for item in literally_all_the_new_features:
        print(item)
    if not os.path.exists('etanbloxxedconfig.pkl'): # check if etanbloxxed config exists
        print('etanbloxxed config file does not exist!')
        with open('etanbloxxedconfig.pkl', 'wb') as file:
            pickle.dump(askconfiguration(), file)
        print('Configuration saved.')

    with open('etanbloxxedconfig.pkl', 'rb') as file:
        thingo = pickle.load(file)
    if not thingo['configVer'] == CONFIG_NO:
        print('etanbloxxed config is out of date!\nold settings:')
        for setin, value in thingo.items():
            print(f'{setin} - {value}')
        with open('etanbloxxedconfig.pkl', 'wb') as file:
            pickle.dump(askconfiguration(), file)
        print('Configuration saved.')
    API_KEY = thingo['ipinfoapi']
    userid = thingo['UserID']
    iswindows = thingo['isWindows']
    robloxdir = thingo['RobloxDirectory']

    while True: # HERE COMES ALL THE NESTED CODE
        print('Enter a command (cmds for commands)')
        userinput = input('> ')
        if userinput == 'cmds':
            print('A list of valid commands:')
            cmds = {'open': 'runs roblox', 'settings': 'modify your settings', 'exit': 'exits etanbloxxed'}
            for command, description in cmds.items():
                print(f'{command} - {description}')
        elif userinput == 'settings':
            print('These are your current settings:')
            for setin, value in thingo.items():
                print(f'{setin} - {value}')
            if askforyesorno('Modify options? | '):
                with open('etanbloxxedconfig.pkl', 'wb') as file:
                    pickle.dump(askconfiguration(), file)
        
        elif userinput == 'exit':
            print('Goodbye!')
            exit()

        elif userinput == 'open':
            if not iswindows:
                os.system(f'open {robloxdir}')
            else:
                subprocess.call(f'{os.path.join(find_latest_modified_directory(os.path.expanduser('~/AppData/Local/Roblox/versions')), 'RobloxPlayerBeta')}')
            print('Opened Roblox')
            close = False
            try:
                print('Connecting to Discord...')
                Presence.connect(self=RPC)
                idleRpc()
                print('Connected to Discord')
            except Exception:
                print('Failed to connect to Discord!')
                traceback.print_exc()
                exit()

            print('\nFinding latest log file...')
            log_file = find_latest_log_file(log_path)
            print('Scanning log file ' + log_file)
            with open(log_file, 'r', encoding='utf-8') as logfile:
                while True:
                    try:
                        loglines = follow(logfile)
                        for line in loglines:
                            if 'GameJoinUtil::joinGamePost' in line: # Handle request to join
                                if 'GameJoinUtil::joinGamePostPrivateServer' in line:
                                    ServerType = 'Private Server'
                                else:
                                    ServerType = 'Public Server'
                                match = re.search(r'BODY: ({.*})', line)
                                if match:
                                    print('Finding game information...')
                                    json_str = match.group(1)
                                    jsondata = json.loads(json_str)

                                    placeid = jsondata.get('placeId')
                                    if placeid:
                                        rootplaceid, gamename, creatorname = getgamedetails(placeid)
                                        imageassetid = getImageAssetId(rootplaceid)
                                    else:
                                        print('No placeid found!') # this almost never happens unless roblox changes the way it works
                                
                            if 'GameJoinUtil::initiateTeleportToReservedServer' in line:
                                ServerType = 'Reserved Server'
                                match = re.search(r'"placeId":(\d+)', line)
                                if match:
                                    placeid = match.group(1)
                                    rootplaceid, gamename, creatorname = getgamedetails(placeid)
                                    imageassetid = getImageAssetId(rootplaceid)
                                else:
                                    print('No placeid found!')

                            if 'GameJoinUtil::initiateTeleportToPlace' in line:
                                pattern = r'"placeId":(\d+)'
                                match = re.search(pattern, line)
                                if match:
                                    placeid = match.group(1)
                                    rootplaceid, gamename, creatorname = getgamedetails(placeid)
                                    imageassetid = getImageAssetId(rootplaceid)
                                else:
                                    print('No placeid found!')

                            if 'Replicator destroyed' in line and cachedstatus == 1: # Handle player leaving game
                                print('Detected disconnect!')
                                bloxstrapRPCCustomState.clear()
                                idleRpc()
                                cachedstatus = 0
                                timesthestupidlagmessagehasbeenspammed = 0
                                sentlagnotification = False
                                    
                            if 'Connecting to UDMUX server' in line and cachedstatus == 0: # Handle player actually connecting to server (this mostly happens after getting the place information)
                                cachedstatus = 1
                                match = re.search(r'UDMUX server (\d+\.\d+\.\d+\.\d+)', line)
                                if match:
                                    cachedipadress = match.group(1)
                                    geolocationinfo = get_geolocation(cachedipadress) # Get geolocation of current server
                                    print('IP Address of UDMUX server:', cachedipadress)
                                    print(f'Connected to: {geolocationinfo.get('city')}, {geolocationinfo.get('region')}')
                                    if not gamename == '':
                                        notification.message = f'Location: {geolocationinfo.get('city')}, {geolocationinfo.get('region')}'
                                        notification.send()
                                        if ServerType == 'Private Server':
                                            updateRpc(gamename, placeid, ServerType)
                                        else:
                                            updateRpc(gamename, placeid, creatorname)
                                    else:
                                        notification.message = f'Location: {geolocationinfo.get('city')}, {geolocationinfo.get('region')}'
                                        updateRpc('', '', ServerType)
                                        notification.send()
                                else:
                                    notification.message = 'No IP found!'
                                    notification.send()
                                    print('No IP Address found') # This doesn't happen i hope
                        
                            if 'destroyLuaApp: (stage:LuaApp) blocking:true.' in line: # Handle roblox closing
                                print('Detected Roblox client closed, closing RPC...')
                                RPC.close()
                                close = True
                        
                            if 'Found new version and the updater launched. Drain reporting and quit.' in line: # Handle roblox updating
                                print('Roblox is updating. Rerun etanbloxxed when it is done updating.')
                                RPC.close()
                                close = True

                            if '[BloxstrapRPC]' in line: # ohhh crap bloxstrap rpc !!
                                rpc_data = line.split('[BloxstrapRPC] ')[1].strip()
                                command_data = json.loads(rpc_data)
                                updateCustomRPC(command_data, gamename, bloxstrapRPCCustomState)

                            if '[DFLog::RakNetMissingPingPong]' in line:
                                timesthestupidlagmessagehasbeenspammed += 1
                                if timesthestupidlagmessagehasbeenspammed == 100 or timesthestupidlagmessagehasbeenspammed > 100 and not sentlagnotification:
                                    notification.message = 'You\'ve disconnected from the game! (You should probably leave the game now)'
                                    notification.send()
                                    sentlagnotification = True

                            if close == True:
                                break

                            time.sleep(0)

                        if close == True:
                            break
                    except Exception as e:
                        if not "'utf-8' codec can't decode" in str(e): # Ignore that error
                            print('An error occured!')
                            traceback.print_exc()
                    
                    except KeyboardInterrupt: 
                        print('Ctrl + c detected, closing RPC...')
                        RPC.close()
                        break
else:
    print('You cannot run etanbloxxed as a module! or something idk')
    exit()
