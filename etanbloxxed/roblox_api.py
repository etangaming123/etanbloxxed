"""All outbound HTTP calls to roproxy (a Roblox API proxy) and ipinfo.io.

Every lookup is bounded to MAX_REQUEST_ATTEMPTS (see constants.py) instead of
retrying forever, so a dead network or a down proxy can't hang etanbloxxed.
"""
from __future__ import annotations

import time
from typing import Optional

import requests

from .constants import (
    ASSET_THUMBNAILS_URL,
    DEFAULT_LARGE_IMAGE,
    ERROR_IMAGE,
    GAMES_URL,
    IPINFO_URL,
    MAX_REQUEST_ATTEMPTS,
    PLACE_ICONS_URL,
    REQUEST_RETRY_DELAY_SECONDS,
    REQUEST_TIMEOUT_SECONDS,
    USERS_URL,
    USER_THUMBNAILS_URL,
)
from .utils import clear_line, logger, print_temporary


class RobloxApiClient:
    def __init__(
        self,
        ipinfo_api_key: str = "",
        timeout: float = REQUEST_TIMEOUT_SECONDS,
        max_attempts: int = MAX_REQUEST_ATTEMPTS,
    ):
        self.session = requests.Session()
        self.ipinfo_api_key = ipinfo_api_key
        self.timeout = timeout
        self.max_attempts = max_attempts
        self._asset_image_cache: dict[str, str] = {}
        self._user_info_cache: Optional[tuple[str, str, bool]] = None

    def _get_json_with_retry(self, url: str, description: str) -> Optional[dict]:
        for attempt in range(1, self.max_attempts + 1):
            print_temporary(f"{description}... Attempt {attempt}")
            try:
                response = self.session.get(url, timeout=self.timeout)
            except requests.RequestException as e:
                logger.debug("Request to %s failed: %s", url, e)
                time.sleep(REQUEST_RETRY_DELAY_SECONDS)
                continue

            if response.status_code == 429:
                time.sleep(REQUEST_RETRY_DELAY_SECONDS)
                continue
            if response.status_code == 404:
                clear_line()
                return None
            if response.status_code == 200:
                clear_line()
                try:
                    return response.json()
                except ValueError:
                    logger.debug("Invalid JSON in response from %s", url)
                    return None
            time.sleep(REQUEST_RETRY_DELAY_SECONDS)

        clear_line()
        logger.debug("Giving up on %r after %d attempts", description, self.max_attempts)
        return None

    def get_game_details(self, universe_id: str) -> tuple[Optional[str], Optional[str]]:
        url = f"{GAMES_URL}?universeIds={universe_id}"
        payload = self._get_json_with_retry(url, "Getting game details")
        data_list = (payload or {}).get("data") or []
        if not data_list:
            return None, None

        data = data_list[0]
        name = data.get("name")
        creator = data.get("creator", {})
        creator_name = creator.get("name", "Unknown")
        badge = " ☑️" if creator.get("hasVerifiedBadge") else ""
        print("Got game details!")
        return name, f"by {creator_name}{badge}"

    def get_user_thumbnail(self, user_id: str) -> str:
        if not user_id:
            return DEFAULT_LARGE_IMAGE
        url = (
            f"{USER_THUMBNAILS_URL}?userIds={user_id}&size=48x48"
            "&format=Png&isCircular=false"
        )
        payload = self._get_json_with_retry(url, "Getting user thumbnail")
        data = (payload or {}).get("data") or []
        if not data or not data[0].get("imageUrl"):
            return DEFAULT_LARGE_IMAGE
        return data[0]["imageUrl"]

    def get_user_display_text(self, user_id: str) -> str:
        if not user_id:
            return "etanbloxxed is a knockoff bloxstrap rpc, go check out bloxstrap!"

        if self._user_info_cache is None:
            url = f"{USERS_URL}/{user_id}"
            payload = self._get_json_with_retry(url, "Getting username and displayname")
            if not payload:
                return "Playing as Unknown User"
            username = payload.get("name", "Unknown")
            display_name = payload.get("displayName", username)
            verified = bool(payload.get("hasVerifiedBadge"))
            self._user_info_cache = (username, display_name, verified)

        username, display_name, verified = self._user_info_cache
        badge = " ☑️" if verified else ""
        return f"Playing as {display_name}{badge} (@{username})"

    def get_place_icon(self, place_id: str) -> str:
        url = f"{PLACE_ICONS_URL}?placeIds={place_id}&size=150x150&format=Png"
        payload = self._get_json_with_retry(url, "Getting image asset id")
        data = (payload or {}).get("data") or []
        if not data or not data[0].get("imageUrl"):
            return ERROR_IMAGE
        return data[0]["imageUrl"]

    def get_asset_image(self, asset_id_or_uri: str) -> str:
        asset_id = str(asset_id_or_uri).replace("rbxassetid://", "")
        if asset_id in self._asset_image_cache:
            return self._asset_image_cache[asset_id]

        url = f"{ASSET_THUMBNAILS_URL}?assetIds={asset_id}&size=150x150&format=Png"
        payload = self._get_json_with_retry(url, "Getting image url")
        data = (payload or {}).get("data") or []
        if not data or not data[0].get("imageUrl"):
            return ""

        image_url = data[0]["imageUrl"]
        self._asset_image_cache[asset_id] = image_url
        return image_url

    def get_geolocation(self, ip_address: str) -> Optional[dict]:
        """Returns None (never the string "None") when there's no api key or the
        lookup fails, so callers can safely do `location.get(...) if location else ...`.
        """
        if not self.ipinfo_api_key:
            return None
        url = f"{IPINFO_URL}/{ip_address}?token={self.ipinfo_api_key}"
        try:
            response = self.session.get(url, timeout=self.timeout)
        except requests.RequestException as e:
            logger.warning("An error occurred while getting location: %s", e)
            return None
        if response.status_code != 200:
            logger.warning("An error occurred while getting location: %s", response.status_code)
            return None
        return response.json()
