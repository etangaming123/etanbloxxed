"""Tails a Roblox player log and drives the Discord presence off of it.

This replaces the old processLines()/theactualetanbloxxedshi() global-variable
soup with a small stateful object, so a `scan` session that runs Roblox
multiple times in a row can just call reset() between runs instead of relying
on module-level globals staying in sync.
"""
from __future__ import annotations

import json
import time
import traceback

from .constants import (
    LOG_MARKER_BLOXSTRAP_RPC,
    LOG_MARKER_CLIENT_CLOSED_1,
    LOG_MARKER_CLIENT_CLOSED_2,
    LOG_MARKER_DISCONNECT,
    LOG_MARKER_GAME_JOIN,
    LOG_MARKER_UDMUX,
    LOG_MARKER_UPDATING,
    PLACE_UNIVERSE_REGEX,
    UDMUX_IP_REGEX,
)
from .logs import follow
from .notifier import Notifier
from .presence import DiscordPresence
from .roblox_api import RobloxApiClient
from .utils import logger


class LogWatcher:
    def __init__(self, api: RobloxApiClient, presence: DiscordPresence, notifier: Notifier):
        self.api = api
        self.presence = presence
        self.notifier = notifier
        self.reset()

    def reset(self) -> None:
        self.place_id: str | None = None
        self.universe_id: str | None = None
        self.game_name: str = ""
        self.creator_name: str = ""
        self.image_asset_id: str = ""
        self.cached_status = 0  # 0 = not connected to a server, 1 = connected
        self.cached_ip: str | None = None
        self.seen_lines: set[str] = set()
        self.should_close = False

    def process_line(self, line: str) -> None:
        if line in self.seen_lines:
            return
        self.seen_lines.add(line)

        if LOG_MARKER_GAME_JOIN in line and self.cached_status == 0:
            self._handle_game_join(line)
        if LOG_MARKER_DISCONNECT in line and self.cached_status == 1:
            self._handle_disconnect()
        if LOG_MARKER_UDMUX in line and self.cached_status == 0:
            self._handle_server_connect(line)
        if LOG_MARKER_CLIENT_CLOSED_1 in line or LOG_MARKER_CLIENT_CLOSED_2 in line:
            self._handle_roblox_closed()
        if LOG_MARKER_UPDATING in line:
            self._handle_roblox_updating()
        if LOG_MARKER_BLOXSTRAP_RPC in line:
            self._handle_bloxstrap_rpc(line)

    def _handle_game_join(self, line: str) -> None:
        match = PLACE_UNIVERSE_REGEX.search(line)
        if not match:
            return
        self.place_id, self.universe_id = match.groups()
        print(f"Place ID: {self.place_id}, Universe ID: {self.universe_id}")
        self.game_name, self.creator_name = self.api.get_game_details(self.universe_id)
        self.image_asset_id = self.api.get_place_icon(self.place_id)
        if self.game_name:
            self.presence.set_game(self.game_name, self.place_id, self.image_asset_id)
        else:
            self.presence.set_default(self.place_id)
        print("Got game data!")

    def _handle_disconnect(self) -> None:
        print("Detected disconnect!")
        self.reset()
        self.presence.custom_state.clear()
        self.presence.set_idle()

    def _handle_server_connect(self, line: str) -> None:
        self.cached_status = 1
        match = UDMUX_IP_REGEX.search(line)
        if not match:
            message = (
                f"Game: {self.game_name}\nNo IP found!"
                if self.game_name
                else "No game found!\nNo IP found!"
            )
            self.notifier.notify(message)
            print("No IP Address found")  # this doesn't happen i hope
            return

        self.cached_ip = match.group(1)
        location = self.api.get_geolocation(self.cached_ip)
        location_text = f'{location.get("city")}, {location.get("region")}' if location else "Unknown"
        print(f"IP Address of UDMUX server: {self.cached_ip}")
        print(f"Connected to: {location_text}")

        if self.game_name:
            self.notifier.notify(f"Game: {self.game_name}\nLocation: {location_text}")
            self.presence.set_game(self.game_name, self.place_id, self.image_asset_id)
        else:
            self.notifier.notify(f"No game found!\nLocation: {location_text}")
            self.presence.set_default(self.place_id)

    def _handle_roblox_closed(self) -> None:
        print("Detected Roblox client closed, closing RPC...")
        self.presence.clear_and_close()
        self.should_close = True

    def _handle_roblox_updating(self) -> None:
        print("Roblox is updating. Rerun etanbloxxed when it is done updating.")
        self.presence.clear_and_close()
        self.should_close = True

    def _handle_bloxstrap_rpc(self, line: str) -> None:
        try:
            rpc_data = line.split("[BloxstrapRPC] ", 1)[1].strip()
            command_data = json.loads(rpc_data)
        except (IndexError, json.JSONDecodeError) as e:
            logger.debug("Failed to parse BloxstrapRPC line: %s", e)
            return
        self.presence.apply_bloxstrap_rpc(command_data, self.game_name, self.place_id)

    def run(self, logfile, read_existing: bool) -> None:
        print("Starting etanbloxxed...")
        print("Connecting to Discord...")
        if self.presence.connect():
            print("Connected to Discord")

        read_existing_done = False
        while True:
            try:
                if read_existing and not read_existing_done:
                    print("Waiting...")
                    time.sleep(3)  # give roblox a moment to write its first lines
                    print("Reading existing lines in log file...")
                    read_existing_done = True
                    for line in logfile:
                        self.process_line(line)

                self.should_close = False
                print("Following new lines in log file...")
                for line in follow(logfile):
                    self.process_line(line)
                    if self.should_close:
                        break
                if self.should_close:
                    break

            except UnicodeDecodeError:
                continue
            except KeyboardInterrupt:
                print("Ctrl+C detected, closing RPC...")
                self.presence.clear_and_close()
                break
            except Exception:
                print("An error occurred!")
                logger.debug(traceback.format_exc())
