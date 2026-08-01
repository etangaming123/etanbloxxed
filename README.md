# >> etanbloxxed <<

mom, can we get bloxstrap?
no, we have bloxstrap at home

(chat gpt was used to make some parts of the script oops)

## [ etanbloxxed info ]

### --IMPORTANT NOTICE--

**etanbloxxed was originally meant to be made for me**, etan, specifically. because of this, **you may experience some unexpected behaviors** when using this script.
**etanbloxxed was made for macos** users because, at the time of writing this, bloxstrap does not support macos.

an ipinfo.io api key is required to see server location, get one at https://ipinfo.io/ (not inputting an api key will disable seeing server location)

the windows version is not tested, use at your own risk!

### --what's etanbloxxed?--

etanbloxxed is a **Python script that is ran alongside Roblox**. it will **broadcast your currently playing game to discord**, and will **show you the server location** whenever you join a game (an ipinfo api key is required https://ipinfo.io/)!

this is basically more or less a remake of Bloxstrap's Roblox RPC

## [ instructions ]

### --how do i use it?--

clone/download this repo, install the dependencies with `pip install -r requirements.txt`, then run etanbloxxed with:

```
python -m etanbloxxed
```

(pass `--debug` for verbose output, e.g. `python -m etanbloxxed --debug`)

etanbloxxed will ask you for settings (ipinfo api key, userid etc.) on first run and save them to `etanbloxxedconfig.json` (a plain JSON file you can also hand-edit), then it's as easy as typing `open` to launch Roblox with the RPC running!

if you're upgrading from an older version that used `etanbloxxedconfig.pkl`, etanbloxxed will automatically migrate your settings to the new JSON config the first time you run it.

### --i found an issue--

this is my very first **public** python project, so issues are very likely to occur. create an issue in this repo or something idk

### --what can i do with this--

**Anything**, really! take the code and make it your own, i don't mind!

This script is unlicensed, check it out [here.](./LICENSE)

## [ planned updates ]

idk where to put planned updates so i put it here

\> Automatically obtaining user's ID

## [ credits ]

\> bloxstrap - the icons that show up on discord and some of their source code

\> chat gpt - helping with code

and you! :3

## [ other ]

### --cool links--

https://github.com/bloxstraplabs/bloxstrap - bloxstrap github page
https://www.roblox.com/groups/15518039/etans-gamers#!/about - my roblox group
