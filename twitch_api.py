import time

import aiohttp

import config

TOKEN_URL = "https://id.twitch.tv/oauth2/token"
STREAMS_URL = "https://api.twitch.tv/helix/streams"


class TwitchAPI:
    def __init__(self):
        self.client_id = config.TWITCH_CLIENT_ID
        self.client_secret = config.TWITCH_CLIENT_SECRET
        self.token = None
        self.token_expiry = 0

    async def fetch_token(self):
        if not self.client_id or not self.client_secret:
            raise RuntimeError("Twitch credentials are missing!")

        async with aiohttp.ClientSession() as session:
            async with session.post(
                TOKEN_URL,
                params={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "grant_type": "client_credentials"
                }
            ) as resp:
                data = await resp.json()
                if "access_token" not in data:
                    raise RuntimeError(f"Failed to get token: {data}")
                self.token = data["access_token"]
                self.token_expiry = time.time() + data["expires_in"]

    async def get_headers(self):
        if not self.token or time.time() > self.token_expiry:
            await self.fetch_token()

        return {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.token}"
        }

    async def get_live_streams(self, usernames: list[str]) -> list[dict]:
        if not usernames:
            return []

        live_streams = []

        for i in range(0, len(usernames), 100):  # Twitch allows 100 users per call
            batch = usernames[i:i+100]
            params = [("user_login", name) for name in batch]

            async with aiohttp.ClientSession() as session:
                async with session.get(STREAMS_URL, headers=await self.get_headers(), params=params) as resp:
                    data = await resp.json()
                    if "data" in data:
                        live_streams.extend(data["data"])
                    else:
                        print(f"Error in Twitch API response: {data}")

        return live_streams
