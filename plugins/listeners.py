from pyrogram import Filters, InlineKeyboardMarkup, InlineKeyboardButton, Message
from ..ass import AssKicker
from ..utils import database, i18n
import aiohttp
import asyncio

@AssKicker.on_message(Filters.group & ~Filters.new_chat_members & ~Filters.left_chat_member)
async def username_check(client: AssKicker, message: Message):
    fromuser = message.from_user
    # Skip if Linked Channel and Username Exists
    if fromuser is None or fromuser.username is not None:
        return

    userid = fromuser.id
    chatid = message.chat.id
    mention = f"{fromuser:mention}"
    groupDB = await database.get(f"group:{chatid}")
    userDB = await database.get(f"user:{userid}")
    userKicked = False

    # Group Database
    if not bool(groupDB):
        groupDB = {}
        groupDB["maxwarn"] = 2
        groupDB["lang"] = "id_ID"
        await database.put(f"group:{chatid}", groupDB)
    lang = groupDB["lang"]
    buttonText = i18n.translate("button", lang)
    kb = [[InlineKeyboardButton(f"{buttonText}", url="https://t.me/KickUrAssBot?start=vid")]]

    # User Database
    if not bool(userDB):
        userDB = {}
        userDB["warn"] = 1
        userDB["lastid"] = 0
    else:
        await client.delete_messages(chatid, int(userDB["lastid"]))

    # Warning Section
    warnUser = int(userDB["warn"])
    maxWarn = groupDB["maxwarn"]

    if warnUser is not int(maxWarn):
        headerText = i18n.translate("warn", lang, mention=mention)
        userDB["warn"] += 1
    else:
        headerText = i18n.translate("kicked", lang, mention)
        await database.delete(f"user:{userid}")
        userKicked = True

    event = await message.reply(
        f"{headerText}\nWarning Count {warnUser} / {maxWarn}", reply_markup=InlineKeyboardMarkup(kb)
    )
    if not userKicked:
        userDB["lastid"] = event.message_id
        await database.put(f"user:{userid}", userDB)
    else:
        await client.kick_members(chatid, userid)


@AssKicker.on_message(Filters.new_chat_members)
async def newuser_check(client: AssKicker, message: Message):
    fromuser = message.from_user
    userid = str(fromuser.id)
    chatid = message.chat.id
    mention = f"{fromuser:mention}"
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.cas.chat/check?user_id={userid}") as response:
            data = await response.json()

    if data["ok"]:
        await asyncio.gather(
            client.kick_members(chatid, userid),
            message.reply(f"Kicked auto-detected spambot {mention}. Powered by Combot API")
    )
