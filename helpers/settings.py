# (c) @AbirHasan2005

import asyncio
from helpers.database.access_db import db
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


async def OpenSettings(event: Message, user_id: int):
    try:
        await event.edit(
            text="**⚙ Configure My Behaviour**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(f"📥 ᴜᴘʟᴏᴀᴅ ᴀs  {'ғɪʟᴇ' if ((await db.get_upload_as_doc(user_id)) is True) else 'ᴠɪᴅᴇᴏ'}",
                                          callback_data="triggerUploadMode")],
                    [InlineKeyboardButton("🌉 ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ ", callback_data="triggerThumbnail")],
                    [InlineKeyboardButton("📝 ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ ", callback_data="triggerCaption")],
                    [InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="closeMeh")]
                ]
            )
        )
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await OpenSettings(event, user_id)
    except MessageNotModified:
        pass
