# Copyright (C) 2019 Rupansh Sekar.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

from telethon.events import StopPropagation

from userbot import (BOTLOG, BOTLOG_CHATID, CMD_HELP, COUNT_MSG, USERS,
                     is_redis_alive)
from userbot.events import register
from userbot.modules.dbhelper import enable_rs, is_rs_enabled
from rivescript import RiveScript


bot = RiveScript()
bot.load_directory("./brain")
bot.sort_replies()

@register(incoming=True, disable_edited=True)
async def rivescript(event):
    if(event.is_private):
        reply = bot.reply("localuser", event.message.message)
        await event.reply(reply)

