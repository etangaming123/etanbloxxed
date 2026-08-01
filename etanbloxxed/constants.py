"""All the tweakable knobs and fixed lookup values used across etanbloxxed.

Change values here rather than hunting through the rest of the package.
"""
import re

VERSION = "1.03.00"
CONFIG_VERSION = "1.00.00"

# Change this if you want to use your own Discord application for the RPC.
DISCORD_CLIENT_ID = 1229562048640319616

# -- roproxy / ipinfo endpoints --
GAMES_URL = "https://games.roproxy.com/v1/games"
USER_THUMBNAILS_URL = "https://thumbnails.roproxy.com/v1/users/avatar-headshot"
USERS_URL = "https://users.roproxy.com/v1/users"
PLACE_ICONS_URL = "https://thumbnails.roproxy.com/v1/places/gameicons"
ASSET_THUMBNAILS_URL = "https://thumbnails.roproxy.com/v1/assets"
IPINFO_URL = "https://ipinfo.io"

GITHUB_URL = "https://github.com/etangaming123/etanbloxxed"
GAME_PAGE_URL_TEMPLATE = "https://www.roproxy.com/games/{place_id}/"

# -- filesystem locations --
MAC_LOG_DIR = "~/Library/Logs/Roblox"
WINDOWS_LOG_DIR = "%LOCALAPPDATA%/Roblox/logs"
WINDOWS_ROBLOX_VERSIONS_DIR = "%LOCALAPPDATA%/Roblox/versions"
DEFAULT_ROBLOX_MAC_APP = "/Applications/Roblox.app"

CONFIG_PATH = "etanbloxxedconfig.json"
LEGACY_PICKLE_CONFIG_PATH = "etanbloxxedconfig.pkl"

# -- discord rich presence image keys (uploaded to the discord app assets) --
DEFAULT_LARGE_IMAGE = "etanbloxxed_main"
ERROR_IMAGE = "etanbloxxed_error"
IDLE_IMAGE = "etanbloxxed_idle"

# -- networking --
REQUEST_TIMEOUT_SECONDS = 10
MAX_REQUEST_ATTEMPTS = 8
REQUEST_RETRY_DELAY_SECONDS = 1.0

# -- idle rich presence flavour text, change/add to these if you want --
IDLE_TEXTS = [
    "github powered!",
    "hello chat",
    "go join etan's gamers group",
    "i love underrated roblox games",
    "inflation goes crazy",
]
RARE_IDLE_TEXT = "there is a 1 in 33 chance of this appearing :3"
RARE_IDLE_CHANCE = 33

# -- Roblox player log line markers --
LOG_MARKER_GAME_JOIN = "[FLog::GameJoinLoadTime] Report game_join_loadtime:"
LOG_MARKER_DISCONNECT = "[FLog::Network] Time to disconnect replication data:"
LOG_MARKER_UDMUX = "Connecting to UDMUX server"
LOG_MARKER_CLIENT_CLOSED_1 = "destroyLuaApp: (stage:LuaApp) blocking:true."
LOG_MARKER_CLIENT_CLOSED_2 = "[FLog::SingleSurfaceApp] shutDown: (stage:Native)."
LOG_MARKER_UPDATING = "Found new version and the updater launched. Drain reporting and quit."
LOG_MARKER_BLOXSTRAP_RPC = "[BloxstrapRPC]"

PLACE_UNIVERSE_REGEX = re.compile(r"placeid:(\d+).*universeid:(\d+)")
UDMUX_IP_REGEX = re.compile(r"UDMUX server (\d+\.\d+\.\d+\.\d+)")
