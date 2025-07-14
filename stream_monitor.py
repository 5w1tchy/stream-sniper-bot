# stream_monitor.py
import asyncio

import discord
from discord.ext import tasks

import config
from twitch_api import TwitchAPI
from utils.live_cache import LiveCache

bot = None  # Will be injected in main.py

twitch_api = TwitchAPI()
cache = LiveCache()


@tasks.loop(minutes=2)
async def check_streams():
    all_usernames = []
    category_map = {}

    # Gather all usernames and map them to categories and channels
    for category, data in config.TWITCH_STREAMERS.items():
        for username in data["channels"]:
            all_usernames.append(username.lower())
            category_map[username.lower()] = {
                "category": category,
                "discord_channel": data["discord_channel"]
            }

    print(f"[Check] Checking {len(all_usernames)} Twitch channels...")

    live_streams = await twitch_api.get_live_streams(all_usernames)
    current_live = {stream["user_login"].lower(
    ): stream for stream in live_streams}

    for username in all_usernames:
        stream_data = current_live.get(username)

        category_info = category_map.get(username)
        if not category_info:
            continue

        channel_id = category_info["discord_channel"]
        if not channel_id:
            continue

        if stream_data:
            title = stream_data["title"]
            thumb = stream_data["thumbnail_url"]

            if not cache.is_live(username):
                await post_stream(username, title, thumb, channel_id)
            else:
                cached = cache.get_message_info(username)
                if cached:
                    print(f"[Check] Cached title: {cached['title']}")
                    print(f"[Check] Current title: {title}")
                    if cached["title"] != title:
                        print(
                            f"[UPDATE TRIGGERED] {username} - Title has changed")
                        await update_stream(username, title, channel_id)
                    else:
                        print(f"[NO UPDATE] {username} - Title unchanged")
        else:
            if cache.is_live(username):
                cache.increment_miss(username)
                if cache.should_cleanup(username):
                    await delete_stream(username)


async def post_stream(username, title, thumb_url, channel_id):
    channel = bot.get_channel(channel_id)
    if not channel:
        print(f"Could not find channel: {channel_id}")
        return

    preview_url = thumb_url.replace(
        "{width}", "1280").replace("{height}", "720")

    embed = discord.Embed(
        title=title,
        url=f"https://twitch.tv/{username}",
        description=f"🔴 **{username}** is now live!",
        color=0x9146FF
    )
    embed.set_image(url=preview_url)

    msg = await channel.send(embed=embed)
    cache.add_stream(username, msg.id, channel_id, title)
    print(f"✅ Posted: {username} → {title}")


async def update_stream(username, new_title, channel_id):
    info = cache.get_message_info(username)
    if not info:
        return

    channel = bot.get_channel(channel_id)
    if not channel:
        return

    try:
        # Fetch old message to delete
        old_msg = await channel.fetch_message(info["message_id"])

        # Get fresh stream data (to grab updated thumbnail)
        stream_data = await twitch_api.get_live_streams([username])
        if not stream_data:
            print(f"No live data found for {username} during update.")
            return

        stream = stream_data[0]
        thumb = stream["thumbnail_url"].replace(
            "{width}", "1280").replace("{height}", "720"
                                       )

        embed = discord.Embed(
            title=new_title,
            url=f"https://twitch.tv/{username}",
            description=f"🔁 **{username}** updated their stream title!",
            color=0x9146FF
        )
        embed.set_image(url=thumb)

        # Send new embed message
        new_msg = await channel.send(embed=embed)
        await old_msg.delete()

        # Update cache with new info
        cache.update_title(username, new_title, new_msg.id)
        print(f"Updated title for {username}")
    except Exception as e:
        print(f"Error updating {username}: {e}")


async def delete_stream(username):
    info = cache.get_message_info(username)
    if not info:
        return

    channel = bot.get_channel(info["channel_id"])
    if not channel:
        return

    try:
        msg = await channel.fetch_message(info["message_id"])
        await msg.delete()
        cache.remove_stream(username)
        print(f"Stream offline: {username}")
    except Exception as e:
        print(f"Error deleting stream {username}: {e}")
