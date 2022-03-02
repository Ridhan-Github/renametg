# (c) @AbirHasan2005

import string
from helpers.database.access_db import db
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


async def SetupPrefix(text: str, user_id: int, editable: Message):
    ascii_ = ''.join([i if (i in string.digits or i in string.ascii_letters or i == " ") else "" for i in text])
    await db.set_prefix(user_id, prefix=text)
    await editable.edit(
        text=f"Fɪʟᴇ Nᴀᴍᴇ Pʀᴇғɪx Sᴜᴄᴄᴇssғᴜʟʟʏ Aᴅᴅᴇᴅ!\n\n**Pʀᴇғɪx :** `{ascii_}`",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Bᴀᴄᴋ", callback_data="openSettings")]])
    )
