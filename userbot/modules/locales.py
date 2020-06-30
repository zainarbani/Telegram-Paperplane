# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

from importlib import reload
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, LOCALES, MONGO
from userbot.events import register, grp_exclude

# Available locales (ISO-639-1)
COUNTRY = {
  "en",
  "id"
}

# Excluded ISO-639-1 country code
EXC = {
  "zh-cn",
  "zh-tw"
}


@register(pattern="^.lang (.*)", outgoing=True)
@grp_exclude()
async def lang(value):
    """ For .lang command, change the default language of userbot.
        Following ISO-639-1 for rest modules.
    """
    query = value.pattern_match.group(1).lower()

    if query in EXC:
        lang = query
    else:
        lang = query.split("-")[0]

    MONGO.lang.update_one(
        {"_id": chk_lang()["_id"]}, {"$set": {"def_lang": lang}},
    )

    await value.edit(get_reply("lang_changed").format(lang))
    if BOTLOG:
        await value.client.send_message(
            BOTLOG_CHATID, get_reply("lang_changed").format(lang))


def chk_lang():
    data = MONGO.lang.find_one({"def_lang": {"$exists": True}})

    if data:
        return data
    else:
        MONGO.lang.insert_one({"def_lang": "en"})
        return reload(data)


def get_lang():
    return chk_lang()["def_lang"]


def get_reply(query):
    lang = get_lang()

    if lang in COUNTRY:
        local = lang
    else:
        local = "en"

    return LOCALES[local][query]


CMD_HELP.update({
    "locales": [
        'Locales',
        f' - `.lang <lang>`: Changes the default language of userbot\n'
    ]
})