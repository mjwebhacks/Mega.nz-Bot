# Copyright (c) 2022 Itz-fork

import os


class Config(object):
    APP_ID = 3796974
    API_HASH = "9511d0112631f9990337eb724d1a7d0d"
    BOT_TOKEN = "5323288890:AAHuktCFJ6XCSauKjln6b0pKsj8wU42qSLM"
    AUTH_USERS = set(int(x) for x in os.environ.get("1464063686").split())
    IS_PUBLIC_BOT = False
    LOGS_CHANNEL = -1001771465683
    # DON'T CHANGE THESE 2 VARS
    DOWNLOAD_LOCATION = "./NexaBots"
    TG_MAX_SIZE = 2040108421
    # Mega User Account
    MEGA_EMAIL = "mjwebhacks@gmail.com"
    MEGA_PASSWORD = "Manya@007"
