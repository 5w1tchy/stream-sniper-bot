DISCORD_TOKEN = "6a0bd566a00f2f8479b098a8a1a79ad5b736dfeb35bb2fa8629af857a7c2b6ed"

TWITCH_CLIENT_ID = "eplakianx2n11lqgcofry3varfc5h4"
TWITCH_CLIENT_SECRET = "aua68y3r8glsesmo2z6rdyzi02hh59"

DOTA2_CHANNEL = None
R6_CHANNEL = None
WOW_CHANNEL = None
SQUAD_CHANNEL = None

TWITCH_STREAMERS = {
    "dota": {
        "discord_channel": DOTA2_CHANNEL,
        "channels": [
            # English
            "dota2ti",
            "dota2ti_2",
            "dota2ti_3",
            "dota2ti_4",
            "dota2ti_5",
            "esl_dota2",
            "pgl_dota2",
            "epldota_en1",
            "epldota_en2",

            # Russian
            "dota2ti_ru",
            "dota2ti_ru_2",
            "dota2ti_ru_3",
            "dota2ti_ru_4",
            "betboom_ru",
            "betboom_ru2",
            "betboom_ru3",
            "betboom_ru4",
            "dota2_paragon_ru",
            "dota2_paragon_ru2",
            "dota2_paragon_ru3"
        ]
    },

    "rainbow6": {
        "discord_channel": R6_CHANNEL,
        "channels": [
            "Rainbow6",
            "Rainbow6Bravo"
        ]
    },

    "wow": {
        "discord_channel": WOW_CHANNEL,
        "channels": [
            "worldofwarcraft"
        ]
    },

    "squad": {
        "discord_channel": SQUAD_CHANNEL,
        "channels": [
            "offworldindustries"
        ]
    }
}
