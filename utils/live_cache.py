import json
import os

os.makedirs("data", exist_ok=True)

CACHE_FILE = "data/live_cache.json"
GRACE_MISSES = 3  # number of times we allow stream to appear "offline" before deleting


class LiveCache:
    def __init__(self):
        self.cache = {}
        self.load()

    def load(self):
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, "r", encoding="utf-8") as f:
                    self.cache = json.load(f)
            except json.JSONDecodeError:
                print("live_cache.json was empty or corrupted. Starting fresh.")
                self.cache = {}
        else:
            self.cache = {}

    def save(self):
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, indent=2)

    def is_live(self, twitch_name):
        return twitch_name in self.cache

    def add_stream(self, twitch_name, message_id, channel_id, title):
        self.cache[twitch_name] = {
            "message_id": message_id,
            "channel_id": channel_id,
            "missed_checks": 0,
            "title": title
        }
        self.save()

    def remove_stream(self, twitch_name):
        if twitch_name in self.cache:
            del self.cache[twitch_name]
            self.save()

    def get_message_info(self, twitch_name):
        return self.cache.get(twitch_name)

    def update_title(self, twitch_name, new_title, new_message_id):
        if twitch_name in self.cache:
            self.cache[twitch_name]["title"] = new_title
            self.cache[twitch_name]["message_id"] = new_message_id
            self.cache[twitch_name]["missed_checks"] = 0
            self.save()

    def increment_miss(self, twitch_name):
        if twitch_name in self.cache:
            self.cache[twitch_name]["missed_checks"] += 1
            self.save()

    def should_cleanup(self, twitch_name):
        data = self.cache.get(twitch_name)
        if not data:
            return False
        return data["missed_checks"] >= GRACE_MISSES
