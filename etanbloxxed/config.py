"""User settings: prompting for them, and loading/saving them as JSON.

Settings live in etanbloxxedconfig.json next to wherever you run etanbloxxed
from, so you can also just open it in a text editor and tweak values by hand.
"""
from __future__ import annotations

import json
import pickle
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

from .constants import CONFIG_PATH, CONFIG_VERSION, DEFAULT_ROBLOX_MAC_APP, LEGACY_PICKLE_CONFIG_PATH
from .utils import ask_yes_no


@dataclass
class Config:
    config_version: str = CONFIG_VERSION
    user_id: str = ""
    ipinfo_api_key: str = ""
    is_windows: bool = False
    roblox_directory: str = DEFAULT_ROBLOX_MAC_APP

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        # Also accepts the field names used by the old pickle-based config,
        # so migrating an existing setup doesn't lose your settings.
        return cls(
            config_version=data.get("config_version", data.get("configVer", CONFIG_VERSION)),
            user_id=str(data.get("user_id", data.get("UserID", ""))),
            ipinfo_api_key=data.get("ipinfo_api_key", data.get("ipinfoapi", "")),
            is_windows=bool(data.get("is_windows", data.get("isWindows", False))),
            roblox_directory=data.get(
                "roblox_directory", data.get("RobloxDirectory", DEFAULT_ROBLOX_MAC_APP)
            ),
        )


def prompt_config() -> Config:
    print(
        "Enter in your Roblox user id. Leaving this blank will not show your "
        "Roblox profile picture on etanbloxxed."
    )
    user_id = input("UserID | ").strip()

    print(
        "Enter in an ipinfo.io api key. A free account can be created at "
        "https://ipinfo.io/signup, granting you 50k requests a month. Leaving "
        "this blank will not give you server info whenever you join a Roblox server."
    )
    ipinfo_api_key = input("API key | ").strip()

    print("Are you running a windows machine?")
    is_windows = ask_yes_no("Windows or not | ")

    roblox_directory = DEFAULT_ROBLOX_MAC_APP
    if not is_windows:
        print(
            "Enter in where your Roblox app is located. Leave blank to use "
            f"default ({DEFAULT_ROBLOX_MAC_APP})"
        )
        custom_directory = input("Directory | ").strip()
        if custom_directory:
            roblox_directory = custom_directory

    return Config(
        config_version=CONFIG_VERSION,
        user_id=user_id,
        ipinfo_api_key=ipinfo_api_key,
        is_windows=is_windows,
        roblox_directory=roblox_directory,
    )


def save_config(config: Config, path: Path = Path(CONFIG_PATH)) -> None:
    path.write_text(json.dumps(config.to_dict(), indent=2))


def _print_settings(config: Config) -> None:
    for key, value in config.to_dict().items():
        print(f"{key} - {value}")


def _migrate_legacy_pickle_config(path: Path) -> Optional[Config]:
    if not path.exists():
        return None
    print("Found a legacy etanbloxxedconfig.pkl, migrating it to the new JSON config format...")
    try:
        with path.open("rb") as file:
            legacy_data = pickle.load(file)
        return Config.from_dict(legacy_data)
    except Exception:
        print("Could not read the legacy config file, you'll need to re-enter your settings.")
        return None


def load_config(
    path: Path = Path(CONFIG_PATH), legacy_path: Path = Path(LEGACY_PICKLE_CONFIG_PATH)
) -> Config:
    if not path.exists():
        print("etanbloxxed config file does not exist!")
        config = _migrate_legacy_pickle_config(legacy_path) or prompt_config()
        save_config(config, path)
        print("Configuration saved.")
        return config

    try:
        config = Config.from_dict(json.loads(path.read_text()))
    except (json.JSONDecodeError, OSError):
        print("etanbloxxed config file is corrupted, let's set it up again.")
        config = prompt_config()
        save_config(config, path)
        print("Configuration saved.")
        return config

    if config.config_version != CONFIG_VERSION:
        print("etanbloxxed config is out of date!\nold settings:")
        _print_settings(config)
        config = prompt_config()
        save_config(config, path)
        print("Configuration saved.")

    return config
