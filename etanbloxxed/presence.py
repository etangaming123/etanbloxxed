"""Everything to do with talking to Discord's Rich Presence over pypresence."""
from __future__ import annotations

import time
import traceback
from typing import Optional

import pypresence

from .constants import DEFAULT_LARGE_IMAGE, ERROR_IMAGE, GAME_PAGE_URL_TEMPLATE, GITHUB_URL, IDLE_IMAGE
from .roblox_api import RobloxApiClient
from .utils import get_random_idle_text, logger

GET_ETANBLOXXED_BUTTON = {"label": "get etanbloxxed", "url": GITHUB_URL}


def game_buttons(place_id: Optional[str]) -> list[dict]:
    buttons = [GET_ETANBLOXXED_BUTTON]
    if place_id:
        buttons.append(
            {"label": "My Current Game", "url": GAME_PAGE_URL_TEMPLATE.format(place_id=place_id)}
        )
    return buttons


class DiscordPresence:
    def __init__(self, client_id: int, api: RobloxApiClient, user_id: str):
        self.client = pypresence.Client(client_id=client_id)
        self.api = api
        self.user_id = user_id
        self.enabled = True
        self.custom_state: dict = {}
        self.has_custom_state = False

    def connect(self) -> bool:
        try:
            self.client.start()
            self.set_idle()
            return True
        except Exception:
            print(
                "Failed to connect to Discord! RPC will be disabled for this session.\n"
                "Is Discord installed and running?"
            )
            logger.debug(traceback.format_exc())
            self.enabled = False
            return False

    def set_game(self, game_name: str, place_id: Optional[str], image_asset_id: str) -> None:
        if not self.enabled:
            return
        try:
            username_text = self.api.get_user_display_text(self.user_id)
            small_image = self.api.get_user_thumbnail(self.user_id)
            buttons = game_buttons(place_id)
            self.client.set_activity(
                name=game_name,
                details=game_name,
                state=username_text,
                large_image=image_asset_id,
                large_text=game_name,
                small_image=small_image,
                small_text=username_text,
                start=time.time(),
                buttons=buttons,
            )
            self.custom_state = {
                "details": f"Roblox - {game_name}",
                "state": username_text,
                "large_image": image_asset_id,
                "large_text": game_name,
                "small_image": small_image,
                "small_text": username_text,
                "start": time.time(),
                "buttons": buttons,
            }
            self.has_custom_state = True
            print(f"RPC set to {game_name}")
        except Exception:
            print("An error occurred while setting RPC!")
            logger.debug(traceback.format_exc())

    def set_default(self, place_id: Optional[str]) -> None:
        if not self.enabled:
            return
        self.has_custom_state = False
        try:
            username_text = self.api.get_user_display_text(self.user_id)
            small_image = self.api.get_user_thumbnail(self.user_id)
            if place_id:
                self.client.set_activity(
                    name="etanbloxxed",
                    details=f"Roblox - Game ID: {place_id}",
                    state=username_text,
                    large_image=DEFAULT_LARGE_IMAGE,
                    large_text=place_id,
                    small_image=small_image,
                    small_text=username_text,
                    start=time.time(),
                    buttons=game_buttons(place_id),
                )
            else:
                self.client.set_activity(
                    name="etanbloxxed",
                    details="Roblox - Unknown Game",
                    state=username_text,
                    large_image=ERROR_IMAGE,
                    large_text="idk what this guys playing",
                    small_image=small_image,
                    small_text=username_text,
                    buttons=game_buttons(None),
                )
            print("RPC set with default message")
        except Exception:
            print("An error occurred while setting RPC!")
            logger.debug(traceback.format_exc())

    def set_idle(self) -> None:
        if not self.enabled:
            return
        self.has_custom_state = False
        try:
            username_text = self.api.get_user_display_text(self.user_id)
            self.client.set_activity(
                name="Roblox",
                details="Roblox",
                state=username_text,
                large_image=IDLE_IMAGE,
                large_text=get_random_idle_text(),
                small_image=self.api.get_user_thumbnail(self.user_id),
                small_text=username_text,
                buttons=[GET_ETANBLOXXED_BUTTON],
            )
        except Exception:
            print("An error occurred while setting RPC!")
            logger.debug(traceback.format_exc())

    def apply_bloxstrap_rpc(
        self, command_data: dict, game_name: str, place_id: Optional[str]
    ) -> None:
        """Handle a [BloxstrapRPC] line a game wrote to its log, letting it
        override the rich presence with custom details/images/timestamps."""
        if not self.enabled or command_data.get("command") != "SetRichPresence":
            return

        data = command_data.get("data", {})
        state = self.custom_state

        if "state" in data:
            state["state"] = data["state"] or f"Roblox - {game_name}"
        if "details" in data:
            state["details"] = data["details"]

        if "largeImage" in data:
            large_image = data["largeImage"]
            if "assetId" in large_image:
                image_url = self.api.get_asset_image(large_image["assetId"])
                if image_url:
                    state["large_image"] = image_url
            if "hoverText" in large_image:
                state["large_text"] = large_image["hoverText"]

        if "smallImage" in data:
            small_image = data["smallImage"]
            if "assetId" in small_image:
                image_url = self.api.get_asset_image(small_image["assetId"])
                if image_url:
                    state["small_image"] = image_url
            if "hoverText" in small_image:
                state["small_text"] = small_image["hoverText"]

        start_time = data.get("timeStart")
        end_time = data.get("timeEnd")
        if start_time is not None and end_time is not None:
            if start_time == 0 or end_time == 0 or start_time > end_time:
                state.pop("start", None)
                state.pop("end", None)
            else:
                state["start"] = start_time
                state["end"] = end_time

        state["buttons"] = game_buttons(place_id)
        self.client.update(**state)
        self.custom_state = state
        print(f'state = {state.get("state")}, details = {state.get("details")}')

    def clear_and_close(self) -> None:
        try:
            self.client.clear_activity()
        except Exception:
            logger.debug("Failed to clear activity", exc_info=True)
        try:
            self.client.close()
        except Exception:
            logger.debug("Failed to close RPC connection", exc_info=True)
