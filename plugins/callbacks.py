from pyrogram import Filters, CallbackQuery
from ..ass import AssKicker
from ..utils import database
import re


async def edit(key, val, chatid):
    groupDB = await database.get(f"group:{chatid}")
    groupDB[key] = str(val)
    return await database.put(f"group:{chatid}", groupDB)


lang_filter = Filters.create(lambda _, cbq: bool(re.match(r"^lang_", cbq.data)))


@AssKicker.on_callback_query(lang_filter)
async def callback_lang(client: AssKicker, query: CallbackQuery):
    lang = query.data[-5:]
    if await client.is_admin(query.message.chat.id, query.from_user.id) is False:
        return await query.answer("Only administrators can use this buton!")
    await edit("lang", lang, query.message.chat.id)
    text = f"Successfully Change Language to {lang}"
    await query.edit_message_text(text)


warn_filter = Filters.create(lambda _, cbq: bool(re.match(r"^warn_", cbq.data)))


@AssKicker.on_callback_query(warn_filter)
async def callback_warn(client: AssKicker, query: CallbackQuery):
    data = query.data.split("_")

    if await client.is_admin(query.message.chat.id, query.from_user.id) is False:
        return await query.answer("Only administrators can use this buton!")
    groupDB = await database.get(f"group:{query.message.chat.id}")
    currentWarn = int(groupDB["maxwarn"])

    if data[1] == "cancel":
        return await query.message.delete()

    if data[1] == "plus":
        currentWarn += 1
        text = f"Successfully add maximum warning to {str(currentWarn)}"
    elif data[1] == "minus":
        if currentWarn == 1:
            return await query.answer("You cant decrease maximum warning past one!")
        currentWarn -= 1
        text = f"Successfully subtract maximum warning to {str(currentWarn)}"

    await edit("maxwarn", currentWarn, query.message.chat.id)
    await query.edit_message_text(text)
