# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for managing events.
 One of the main components of the userbot. """

import sys
from asyncio import create_subprocess_shell as asyncsubshell
from asyncio import subprocess as asyncsub
from os import remove
from time import gmtime, strftime
from traceback import format_exc

from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins

from userbot import LogicWorker, bot


header = """**Sorry, I encountered a error!**
If you wanna you can report it \
- just forward this message to [{}]({}).
I won't log anything except the fact of error and date"""

disclaimer = """Disclaimer:
This file is ONLY uploaded here, \
we logged only the fact of error and date, \
and we respect your privacy, \
you may not report this error if you've \
any confidential data here, noone will see your data.


--------BEGIN USERBOT TRACEBACK LOG--------

Date: {date}
Group ID: {group}
Sender ID: {sender}

Event Trigger:
{trigger}

Traceback info:
{traceback}

Error text:
{error}

--------END USERBOT TRACEBACK LOG--------


Last 5 commits:
{commits}"""


def register(**args):
    """ Register a new event. """
    pattern = args.get('pattern', None)
    disable_edited = args.get('disable_edited', False)
    ignore_unsafe = args.get('ignore_unsafe', False)
    unsafe_pattern = r'^[^/!#@\$A-Za-z]'
    group_only = args.get('group_only', False)
    disable_errors = args.get('disable_errors', False)
    permit_sudo = args.get('permit_sudo', False)
    if pattern is not None and not pattern.startswith('(?i)'):
        args['pattern'] = '(?i)' + pattern

    if "disable_edited" in args:
        del args['disable_edited']

    if "ignore_unsafe" in args:
        del args['ignore_unsafe']

    if "group_only" in args:
        del args['group_only']

    if "disable_errors" in args:
        del args['disable_errors']

    if "permit_sudo" in args:
        del args['permit_sudo']

    if pattern:
        if not ignore_unsafe:
            args['pattern'] = pattern.replace('^.', unsafe_pattern, 1)

    def decorator(func):
        async def wrapper(check):
            if group_only and not check.is_group:
                await check.respond("`Are you sure this is a group?`")
                return

            # Check if the sudo is an admin already.
            if permit_sudo and not check.out:
                if check.sender_id in LogicWorker:
                    async for user in check.client.iter_participants(
                            check.chat_id, filter=ChannelParticipantsAdmins):
                        if user.id in LogicWorker:
                            return
                    # Announce that you are handling the request
                    await check.respond("`Processing Sudo Request!`")
                else:
                    return

            try:
                await func(check)
            #
            # Raise StopPropagation again if required by a function
            #
            # TODO
            # Rewrite events to not passing all exceptions
            #
            except events.StopPropagation:
                raise events.StopPropagation
            # Exception must be passed out to avoid unexpected spam.
            except KeyboardInterrupt:
                pass
            except BaseException:

                # Check if we have to disable it.
                # If not silence the log spam on the console,
                # with a dumb except.

                if not disable_errors:
                    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    command = "git log --pretty=format:\"%an: %s\" -5"
                    process = await asyncsubshell(command,
                                                  stdout=asyncsub.PIPE,
                                                  stderr=asyncsub.PIPE)
                    stdout, stderr = await process.communicate()
                    result = str(stdout.decode().strip()) \
                        + str(stderr.decode().strip())

                    text = header.format(
                        "https://t.me/userbot_support", "Userbot Support Chat)"
                    )
                    ftext = disclaimer.format(
                        date=date,
                        group=str(check.chat_id),
                        sender=str(check.sender_id),
                        trigger=str(check.text),
                        traceback=str(format_exc()).strip(),
                        error=str(sys.exc_info()[1]),
                        commits=result
                    )

                    file = open("error.log", "w+")
                    file.write(ftext)
                    file.close()

                    if bot.is_connected():
                        await check.client.send_file(
                            check.chat_id,
                            "error.log",
                            caption=text,
                        )
                        remove("error.log")
            else:
                pass

        if not disable_edited:
            bot.add_event_handler(wrapper, events.MessageEdited(**args))
        bot.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper

    return decorator
