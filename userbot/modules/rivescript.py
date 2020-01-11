# Copyright (C) 2019 Rupansh Sekar.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

from telethon.events import StopPropagation

from userbot import (BOTLOG, BOTLOG_CHATID, CMD_HELP, COUNT_MSG, USERS,
                     is_redis_alive)
from userbot.events import register
from userbot.modules.dbhelper import disable_rs, enable_rs, is_rs_enabled
from rivescript import RiveScript


bot = RiveScript()
bot.load_directory("./brain")
bot.sort_replies()

@register(incoming=True, disable_edited=True)
async def rivescript(event):
    if(event.is_private):
        if (await is_rs_enabled()):
            reply = bot.reply("localuser", event.message.message)
            await event.reply(reply)

@register(outgoing=True, disable_errors=True, pattern="^.rs off")
async def d_ev(event):
    if not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return
    await disable_rs()
    await event.edit("Rivescript Enabled")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "You enabled RiveScript!")


@register(outgoing=True, disable_errors=True, pattern="^.rs on")
async def e_rv(event):
    if not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return
    await enable_rs()
    await event.edit("Rivescript Enabled")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "You disabled RiveScript!")
