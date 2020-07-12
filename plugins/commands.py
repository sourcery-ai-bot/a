from pyrogram import Filters, InlineKeyboardMarkup, InlineKeyboardButton, Message
from ..ass import AssKicker
from ..utils import database


@AssKicker.on_message(Filters.command("start") & Filters.private)
async def start(_client: AssKicker, message: Message):
    text = message.text
    if text[-3:] == "vid":
        return await message.reply_animation("CgADBAADowADXaFkUSGCHbl4grqRAg")
    kb = [[InlineKeyboardButton("🔗 Invite To Group", url="https://t.me/KickUrAssBot?startgroup=new_group")]]
    text = "🤖 AssKicker Extended\nAssKicker Extended is a new version of AssKicker. Adds a lot of new features."
    await message.reply(text, reply_markup=InlineKeyboardMarkup(kb))


@AssKicker.on_message(Filters.command("settings") & Filters.group)
async def settings(_client: AssKicker, message: Message):
    groupDB = await database.get(f"group:{message.chat.id}")
    current = groupDB["lang"]
    maxWarn = groupDB["maxwarn"]
    kb = [
        [
            InlineKeyboardButton("🇮🇩 Indonesia", callback_data="lang_id_ID"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en_US"),
        ],
        [
            InlineKeyboardButton("➕ Warnings", callback_data="warn_plus"),
            InlineKeyboardButton("➖ Warnings", callback_data="warn_minus"),
        ],
        [InlineKeyboardButton("❌ Cancel", callback_data="warn_cancel"),],
    ]
    await message.reply(
        f"**AssKicker Settings for {message.chat.title}**\nYour language currently set to `{current}` with maximum warnings currently set to `{maxWarn}`.\nSelect one using the keyboard below:",
        reply_markup=InlineKeyboardMarkup(kb),
    )
