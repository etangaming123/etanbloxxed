"""The interactive command loop: open / settings / terminate / scan / exit."""
from __future__ import annotations

import argparse
import subprocess
import time
import traceback

import psutil

from .config import load_config, prompt_config, save_config
from .constants import DISCORD_CLIENT_ID, VERSION
from .logs import default_log_directory, default_roblox_versions_directory, find_latest_log_file, find_latest_modified_directory
from .notifier import Notifier
from .presence import DiscordPresence
from .roblox_api import RobloxApiClient
from .utils import ask_yes_no, configure_logging, logger
from .watcher import LogWatcher

CHANGELOG = [
    "What's new in the latest etanbloxxed update:",
    "> refactored into a proper Python package - cleaner code, easier to maintain",
    "> settings are now stored as human-readable JSON (etanbloxxedconfig.json) instead of a pickle file",
    "> fixed a handful of bugs (Windows log path was never actually used, some retries could hang forever, "
    "a location lookup crash when no ipinfo key is set)",
]

ROBLOX_PROCESS_NAMES = {"RobloxPlayer", "RobloxPlayerBeta.exe"}

COMMANDS = {
    "open": "runs roblox",
    "scan": "automatically starts etanbloxxed whenever roblox is launched",
    "settings": "modify your settings",
    "terminate": "terminates (force quits) roblox",
    "exit": "exits etanbloxxed",
}


def print_banner() -> None:
    print(
        "Welcome to etanbloxxed!\nThis is basically bloxstrap but bad and poorly optimised"
        f"\n\nYou are running version {VERSION}.\n"
    )
    for line in CHANGELOG:
        print(line)


def open_roblox(config) -> None:
    if config.is_windows:
        versions_dir = find_latest_modified_directory(default_roblox_versions_directory())
        exe_path = versions_dir / "RobloxPlayerBeta.exe"
        subprocess.Popen([str(exe_path)])
    else:
        subprocess.run(["open", config.roblox_directory], check=True)
    print("Opened Roblox")


def terminate_roblox() -> None:
    terminated = False
    for proc in psutil.process_iter(["name"]):
        try:
            if proc.info["name"] in ROBLOX_PROCESS_NAMES:
                proc.kill()
                terminated = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    print("Force terminated Roblox." if terminated else "Roblox does not appear to be running.")


def build_components(config):
    api = RobloxApiClient(ipinfo_api_key=config.ipinfo_api_key)
    presence = DiscordPresence(DISCORD_CLIENT_ID, api, config.user_id)
    notifier = Notifier()
    watcher = LogWatcher(api, presence, notifier)
    return watcher


def main() -> None:
    parser = argparse.ArgumentParser(description="etanbloxxed - a knockoff Bloxstrap RPC")
    parser.add_argument("--debug", action="store_true", help="print verbose debug output")
    args = parser.parse_args()
    configure_logging(args.debug)

    print_banner()
    config = load_config()
    watcher = build_components(config)
    log_dir = default_log_directory(config.is_windows)

    while True:
        user_input = input("Enter a command (cmds for commands)\n> ").strip()

        if user_input == "cmds":
            print("A list of valid commands:")
            for command, description in COMMANDS.items():
                print(f"{command} - {description}")

        elif user_input == "settings":
            print("These are your current settings:")
            for key, value in config.to_dict().items():
                print(f"{key} - {value}")
            if ask_yes_no("Modify options? | "):
                config = prompt_config()
                save_config(config)
                watcher = build_components(config)
                log_dir = default_log_directory(config.is_windows)

        elif user_input == "terminate":
            terminate_roblox()

        elif user_input == "exit":
            print("Goodbye!")
            break

        elif user_input == "open":
            try:
                open_roblox(config)
            except Exception:
                print("Failed to open Roblox!")
                logger.debug(traceback.format_exc())
                continue

            watcher.reset()
            print("\nFinding latest log file...")
            try:
                log_file_path = find_latest_log_file(log_dir)
            except FileNotFoundError:
                print("Could not find a Roblox log file. Is Roblox running?")
                continue
            print(f"Scanning log file {log_file_path}")
            with open(log_file_path, "r", encoding="utf-8", errors="replace") as logfile:
                watcher.run(logfile, read_existing=False)

        elif user_input == "scan":
            print("Scanner is active, etanbloxxed will automatically run when Roblox is opened.")
            try:
                last_log = find_latest_log_file(log_dir)
            except FileNotFoundError:
                last_log = None
            try:
                while True:
                    try:
                        current_log = find_latest_log_file(log_dir)
                    except FileNotFoundError:
                        time.sleep(1)
                        continue
                    if current_log != last_log:
                        print("New log file detected, running etanbloxxed...")
                        watcher.reset()
                        with open(current_log, "r", encoding="utf-8", errors="replace") as logfile:
                            watcher.run(logfile, read_existing=True)
                        print("etanbloxxed is still scanning!")
                    last_log = current_log
                    time.sleep(1)
            except KeyboardInterrupt:
                print("Scanner stopped.")

        else:
            print("Unknown command. Type 'cmds' for a list of valid commands.")


if __name__ == "__main__":
    main()
