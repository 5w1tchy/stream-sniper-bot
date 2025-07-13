import asyncio

from twitch_api import TwitchAPI


async def main():
    api = TwitchAPI()
    usernames = [
        "dota2ti", "esl_dota2", "pgl_dota2",  # feel free to sub in known live ones
        "rainbow6", "worldofwarcraft"
    ]
    live = await api.get_live_streams(usernames)

    if live:
        print("✅ Live Streams:")
        for stream in live:
            print(f"- {stream['user_name']}: {stream['title']}")
    else:
        print("❌ No live streams found or Twitch API failed.")

asyncio.run(main())
