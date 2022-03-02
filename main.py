# (c) @AbirHasan2005

import os
import time
import psutil
import shutil
import string
import asyncio
from pyromod import listen
from pyrogram import Client, filters
from asyncio import TimeoutError
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, ForceReply

from configs import Config
from helpers.settings import OpenSettings
from helpers.database.access_db import db
from helpers.forcesub import ForceSub
from helpers.check_gap import CheckTimeGap
from helpers.setup_prefix import SetupPrefix
from helpers.broadcast import broadcast_handler
from helpers.uploader import UploadVideo, UploadAudio, UploadFile
from helpers.database.add_user import AddUserToDatabase
from helpers.display_progress import progress_for_pyrogram, humanbytes


RenameBot = Client(
    session_name=Config.SESSION_NAME,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton(' ʜᴇʟᴘ', url='https://telegram.me/Tellybots'),
        InlineKeyboardButton(' ᴀʙᴏᴜᴛ', callback_data='about')
        ],[
        InlineKeyboardButton(' sᴜᴘᴘᴏʀᴛ', callback_data='help'),
        InlineKeyboardButton(' sᴇᴛᴛɪɴɢs', callback_data='openSettings')
        ],[
        InlineKeyboardButton(' ᴄʟᴏsᴇ', callback_data='close')
        ]]
    )

HELP_BUTTONS = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(" ʜᴏᴍᴇ", callback_data="home"),
                 InlineKeyboardButton(" ᴀʙᴏᴜᴛ", callback_data="about"),
                 InlineKeyboardButton(" ᴄʟᴏsᴇ", callback_data="close")]
            ]
        )

ABOUT_BUTTONS = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(" ʜᴇʟᴘ", url="https://t.me/Tellybots_support")],
                [InlineKeyboardButton(" ʜᴏᴍᴇ", callback_data="home"),
                 InlineKeyboardButton(" ᴄʟᴏsᴇ", callback_data="close")]
            ]
        )


@RenameBot.on_message(filters.private & filters.command("start"))
async def start_handler(bot: Client, event: Message, cb=False):
    await AddUserToDatabase(bot, event)
    FSub = await ForceSub(bot, event)
    if FSub == 400:
        return
    if not cb:
        send_msg = await event.reply_text("**Pʀᴏᴄᴇssɪɴɢ......**", quote=True)    
    await send_msg.edit(
      text=f"{Config.START_TEXT}".format(event.from_user.mention), 
      reply_markup=START_BUTTONS, 
      disable_web_page_preview=True
       )
    if cb:
        return await event.message.edit(
                 text=f"{Config.START_TEXT}".format(event.from_user.mention),
                 reply_markup=START_BUTTONS,
                 disable_web_page_preview=True
                     )
            
@RenameBot.on_message(filters.private & filters.command("help"))
async def start_handler(bot: Client, event: Message, cb=False):
    await AddUserToDatabase(bot, event)
    FSub = await ForceSub(bot, event)
    if FSub == 400:
        return
    if not cb:
        send_msg = await event.reply_text("**Pʀᴏᴄᴇssɪɴɢ......**", quote=True)    
    await send_msg.edit(
      text=f"{Config.HELP_TEXT}".format(event.from_user.mention), 
      reply_markup=HELP_BUTTONS, 
      disable_web_page_preview=True
       )
    if cb:
        return await event.message.edit(
                 text=f"{Config.HELP_TEXT}".format(event.from_user.mention),
                 reply_markup=HELP_BUTTONS,
                 disable_web_page_preview=True
                     )
            
@RenameBot.on_message(filters.private & filters.command("about"))
async def start_handler(bot: Client, event: Message, cb=False):
    await AddUserToDatabase(bot, event)
    FSub = await ForceSub(bot, event)
    if FSub == 400:
        return
    if not cb:
        send_msg = await event.reply_text("**Pʀᴏᴄᴇssɪɴɢ......**", quote=True)    
    await send_msg.edit(
      text=f"{Config.ABOUT_TEXT}", 
      reply_markup=ABOUT_BUTTONS, 
      disable_web_page_preview=True
       )
    if cb:
        return await event.message.edit(
                 text=f"{Config.ABOUT_TEXT}",
                 reply_markup=ABOUT_BUTTONS,
                 disable_web_page_preview=True
                     )


            #try:
                #os.remove(download_location)
              #  os.remove(thumb_image_path)
            #except:
                #pass










@RenameBot.on_message(filters.private & (filters.video | filters.document | filters.audio))
async def rename_handler(bot: Client, event: Message):
    await AddUserToDatabase(bot, event)
    FSub = await ForceSub(bot, event)
    if FSub == 400:
        return
    isInGap, t_ = await CheckTimeGap(user_id=event.from_user.id)
    if (Config.ONE_PROCESS_ONLY is False) and (isInGap is True):
        await event.reply_text(f"**Please use me after {str(t_)} seconds !!**", quote=True)
        return
    elif (Config.ONE_PROCESS_ONLY is True) and (isInGap is True):
        await event.reply_text("**Please use me after {t_}**", quote=True)
        return
    media = event.video or event.audio or event.document
    if media and media.file_name:
        reply_ = await event.reply_text(
            text=f"**Eɴᴛᴇʀ ᴀ Nᴇᴡ Fɪʟᴇ Nᴀᴍᴇ ғᴏʀ ᴛʜɪs Fɪʟᴇ 📂\n\nNᴏᴛᴇ: Exᴛᴇɴsɪᴏɴ Nᴏᴛ Rᴇǫᴜɪʀᴇᴅ**",
            quote=True
        )
        download_location = f"{Config.DOWNLOAD_PATH}/{str(event.from_user.id)}/{str(time.time())}/"
        if os.path.exists(download_location):
            os.makedirs(download_location)
        try:
            ask_: Message = await bot.listen(event.chat.id, timeout=300)
            if ask_.text and (ask_.text.startswith("/") is False):
                ascii_ = ''.join([i if (i in string.digits or i in string.ascii_letters or i == " ") else "" for i in ask_.text.rsplit('.', 1)[0]])
                new_file_name = f"{download_location}{ascii_.replace(' ', ' ')}.{media.file_name.rsplit('.', 1)[-1]}"
                if len(new_file_name) > 255:
                    await reply_.edit("**😕 Mᴀᴋᴇ ɪᴛ Sᴍᴀʟʟᴇʀ... Dᴏɴ'ᴛ ᴡʀɪᴛᴇ ᴇssᴀʏs!!**")
                    return
                await ask_.delete(True)
                await reply_.edit("**📥 Tʀʏɪɴɢ ᴛᴏ Dᴏᴡɴʟᴏᴀᴅ...**")
                await asyncio.sleep(Config.SLEEP_TIME)
                c_time = time.time()
                try:
                    await bot.download_media(
                        message=event,
                        file_name=new_file_name,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            "**Dᴏᴡɴʟᴏᴀᴅɪɴɢ... **",
                            reply_,
                            c_time
                        )
                    )
                    if not os.path.lexists(new_file_name):
                        try:
                            await reply_.edit("**Nᴏ Fɪʟᴇ Fᴏᴜɴᴅ 😒**")
                        except:
                            print(f"**🙄 Uɴᴀʙʟᴇ ᴛᴏ Fɪɴᴅ Fɪʟᴇ Fᴏʀ {str(event.from_user.id)} !!**")
                        return
                    await asyncio.sleep(Config.SLEEP_TIME)
                    await reply_.edit("**📤 Tʀʏɪɴɢ ᴛᴏ Uᴘʟᴏᴀᴅ...**")
                    upload_as_doc = await db.get_upload_as_doc(event.from_user.id)
                    if upload_as_doc is True:
                        await UploadFile(
                            bot,
                            reply_,
                            file_path=new_file_name,
                            file_size=media.file_size
                        )
                    else:
                        if event.audio:
                            duration_ = event.audio.duration if event.audio.duration else 0
                            performer_ = event.audio.performer if event.audio.performer else None
                            title_ = event.audio.title if event.audio.title else None
                            await UploadAudio(
                                bot,
                                reply_,
                                file_path=new_file_name,
                                file_size=media.file_size,
                                duration=duration_,
                                performer=performer_,
                                title=title_
                            )
                        elif event.video or (event.document and event.document.mime_type.startswith("video/")):
                            thumb_ = event.video.thumbs[0] if ((event.document is None) and (event.video.thumbs is not None)) else None
                            duration_ = event.video.duration if ((event.document is None) and (event.video.thumbs is not None)) else 0
                            width_ = event.video.width if ((event.document is None) and (event.video.thumbs is not None)) else 0
                            height_ = event.video.height if ((event.document is None) and (event.video.thumbs is not None)) else 0
                            await UploadVideo(
                                bot,
                                reply_,
                                file_path=new_file_name,
                                file_size=media.file_size,
                                default_thumb=thumb_,
                                duration=duration_,
                                width=width_,
                                height=height_
                            )
                        else:
                            await UploadFile(
                                bot,
                                reply_,
                                file_path=new_file_name,
                                file_size=media.file_size
                            )
                except Exception as err:
                    try:
                        await reply_.edit(f"**Error:** `{err}`")
                    except:
                        print(f"**Error:** `{err}`")
            elif ask_.text and (ask_.text.startswith("/") is True):
                await reply_.edit("**❌ Cancelled the Ongoing Process... 😐**")
        except TimeoutError:
            await reply_.edit("**🤬 Do you really want to rename then please enter your new File Name... I'm not only for you 👀**")


@RenameBot.on_message(filters.private & filters.photo & ~filters.edited)
async def photo_handler(bot: Client, event: Message):
    await AddUserToDatabase(bot, event)
    FSub = await ForceSub(bot, event)
    if FSub == 400:
        return
    editable = await event.reply_text("**👀 Processing...**")
    await db.set_thumbnail(event.from_user.id, thumbnail=event.photo.file_id)
    await editable.edit("**✔︎ Cᴜsᴛᴏᴍ Tʜᴜᴍʙɴᴀɪʟ Sᴀᴠᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ!**")


@RenameBot.on_message(filters.private & filters.command(["deletethumb", "deletethumbnail"]) & ~filters.edited)
async def delete_thumb_handler(bot: Client, event: Message):
    await AddUserToDatabase(bot, event)
    FSub = await ForceSub(bot, event)
    if FSub == 400:
        return
    await db.set_thumbnail(event.from_user.id, thumbnail=None)
    await event.reply_text(
        "**🗑️ Cᴜsᴛᴏᴍ Tʜᴜᴍʙɴᴀɪʟ Dᴇʟᴇᴛᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ!**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⚙ Cᴏɴғɪɢᴜʀᴇ Sᴇᴛᴛɪɴɢs", callback_data="openSettings")]
        ])
    )


@RenameBot.on_message(filters.private & filters.command(["showthumb", "showthumbnail"]) & ~filters.edited)
async def show_thumb_handler(bot: Client, event: Message):
    await AddUserToDatabase(bot, event)
    FSub = await ForceSub(bot, event)
    if FSub == 400:
        return
    _thumbnail = await db.get_thumbnail(event.from_user.id)
    if _thumbnail is not None:
        try:
            await bot.send_photo(
                chat_id=event.chat.id,
                photo=_thumbnail,
                text=f"**Yᴏᴜʀ Cᴜʀʀᴇɴᴛ Tʜᴜᴍʙɴᴀɪʟ...**", 
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🗑️ Dᴇʟᴇᴛᴇ Tʜᴜᴍʙɴᴀɪʟ", callback_data="deleteThumbnail")]]
                ),
                reply_to_message_id=event.message_id
            )
        except Exception as err:
            try:
                await bot.send_message(
                    chat_id=event.chat.id,
                    text=f"**😐 ᴜɴᴀʙʟᴇ ᴛᴏ sᴇɴᴛ ᴛʜᴜᴍʙɴᴀɪʟ! Gᴏᴛ ᴀɴ ᴜɴᴇxᴘᴇᴄᴛᴇᴅ Eʀʀᴏʀ**",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="closeMeh")],[InlineKeyboardButton("📮 Report issue", url="https://t.me/AVBotz_Support")]]),
                    reply_to_message_id=event.message_id
                )
            except:
                pass
    else:
        await event.reply_text("**🤧 No Thumbnail Found, Send any image to set it as your custom Thumbnail**", quote=True)


@RenameBot.on_message(filters.private & filters.command(["delete_caption", "del_caption", "remove_caption", "rm_caption"]) & ~filters.edited)
async def delete_caption(bot: Client, event: Message):
    await AddUserToDatabase(bot, event)
    FSub = await ForceSub(bot, event)
    if FSub == 400:
        return
    await db.set_caption(event.from_user.id, caption=None)
    await event.reply_text("**Cᴜsᴛᴏᴍ Cᴀᴘᴛɪᴏɴ Rᴇᴍᴏᴠᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ!**")


@RenameBot.on_message(filters.private & filters.command("broadcast") & filters.user(Config.BOT_OWNER) & filters.reply)
async def _broadcast(_, event: Message):
    await broadcast_handler(event)


@RenameBot.on_message(filters.private & filters.command("status") & filters.user(Config.BOT_OWNER))
async def show_status_count(_, event: Message):
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    total_users = await db.total_users_count()
    await event.reply_text(
        text=f"**✍︎ Rename Bot - @ RemamerXProroBot \n😺 Total Disk Space: {total} \n😹 Used Space: {used}({disk_usage}%) \n😸 Free Space: {free} \n😼 CPU Usage: {cpu_usage}% \n😽 RAM Usage: {ram_usage}%\n\n✅ Total Users in DB: {total_users}**",
        parse_mode="Markdown",
        quote=True
    )


@RenameBot.on_message(filters.private & filters.command("settings"))
async def settings_handler(bot: Client, event: Message):
    await AddUserToDatabase(bot, event)
    FSub = await ForceSub(bot, event)
    if FSub == 400:
        return
    editable = await event.reply_text(
        text="** Processing...**"
    )
    await OpenSettings(editable, user_id=event.from_user.id)


@RenameBot.on_callback_query()
async def callback_handlers(bot: Client, cb: CallbackQuery):
    if "closeMeh" in cb.data:
        await cb.message.delete(True)
        await cb.message.reply_to_message.delete()
    elif "close" in cb.data:
        await cb.message.delete(True)
        await cb.message.reply_to_message.delete()
    elif "help" in cb.data:
        await cb.edit_message_text(
              text = f"{Config.HELP_TEXT}".format(cb.from_user.mention),
              disable_web_page_preview = True,
              reply_markup = HELP_BUTTONS)
    elif "home" in cb.data:
        await cb.edit_message_text(
              text = f"{Config.START_TEXT}".format(cb.from_user.mention),
              disable_web_page_preview = True,
              reply_markup = START_BUTTONS)
    elif "about" in cb.data:
        await cb.edit_message_text(
              text = f"{Config.ABOUT_TEXT}".format(cb.from_user.mention),
              disable_web_page_preview = True,
              reply_markup = ABOUT_BUTTONS)
    elif "openSettings" in cb.data:
        await OpenSettings(cb.message, user_id=cb.from_user.id)
    elif "triggerUploadMode" in cb.data:
        upload_as_doc = await db.get_upload_as_doc(cb.from_user.id)
        if upload_as_doc is True:
            await db.set_upload_as_doc(cb.from_user.id, upload_as_doc=False)
        else:
            await db.set_upload_as_doc(cb.from_user.id, upload_as_doc=True)
        await OpenSettings(cb.message, user_id=cb.from_user.id)
    elif "forceNewPrefix" in cb.data:
        await cb.message.edit(
            text="**Sᴇɴᴅ ᴍᴇ Nᴇᴡ Fɪʟᴇ Nᴀᴍᴇ Pʀᴇғɪx!**"
        )
        try:
            ask_: Message = await bot.listen(cb.message.chat.id, timeout=300)
            if ask_.text and (ask_.text.startswith("/") is False):
                await ask_.delete(True)
                await SetupPrefix(ask_.text, user_id=cb.from_user.id, editable=cb.message)
            elif ask_.text and (ask_.text.startswith("/") is True):
                await cb.message.edit(
                    text="**Current Process Cancelled!**",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="openSettings")]])
                )
        except TimeoutError:
            await cb.message.edit(
                text="**I Can't Wait More... BYE 👋🏻**",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="openSettings")]])
            )
    elif "triggerPrefix" in cb.data:
        current_prefix = await db.get_prefix(cb.from_user.id)
        if current_prefix is None:
            await cb.answer("No Prefix Found... ", show_alert=True)
            await cb.message.edit(
                text="**Send me a File Name Prefix!**"
            )
            try:
                ask_: Message = await bot.listen(cb.message.chat.id, timeout=300)
                if ask_.text and (ask_.text.startswith("/") is False):
                    await ask_.delete(True)
                    await SetupPrefix(ask_.text, user_id=cb.from_user.id, editable=cb.message)
                elif ask_.text and (ask_.text.startswith("/") is True):
                    await cb.message.edit(
                        text="**Current Process Cancelled!**",
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="openSettings")]])
                    )
            except TimeoutError:
                await cb.message.edit(
                    text="**I Can't Wait More... BYE 👋🏻**",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="openSettings")]])
                )
        else:
            await cb.message.edit(
                text=f"**Current Prefix:** `{current_prefix}`",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("sᴇᴛ ɴᴇᴡ ᴘʀᴇғɪx", callback_data="forceNewPrefix")],
                        [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="openSettings")]
                    ]
                )
            )
    elif "triggerThumbnail" in cb.data:
        thumbnail = await db.get_thumbnail(cb.from_user.id)
        if thumbnail is None:
            await cb.answer("Nᴏ Tʜᴜᴍʙɴᴀɪʟ Fᴏᴜɴᴅ... ", show_alert=True)
        else:
            await cb.answer("Tʀʏɪɴɢ ᴛᴏ sᴇɴᴅ ʏᴏᴜʀ ᴛʜᴜᴍʙɴᴀɪʟ...", show_alert=True)
            try:
                await bot.send_photo(
                    chat_id=cb.message.chat.id,
                    photo=thumbnail,
                    text=f"**ʏᴏᴜʀ ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ...**",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🗑️ Delete Thumbnail", callback_data="deleteThumbnail")]])
                )
            except Exception as err:
                try:
                    await bot.send_message(
                        chat_id=cb.message.chat.id,
                        text=f"**😐 ᴜɴᴀʙʟᴇ ᴛᴏ sᴇɴᴅ ᴛʜᴜᴍʙɴᴀɪɴ! Gᴏᴛ ᴀɴ ᴜɴᴇxᴘᴇᴄᴛᴇᴅ Eʀʀᴏʀ**",
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cʟᴏsᴇ", callback_data="closeMeh")],[InlineKeyboardButton("📮 Report issue", url="https://t.me/AVBotz_Support")]])
                    )
                except:
                    pass
    elif "deleteThumbnail" in cb.data:
        await db.set_thumbnail(cb.from_user.id, thumbnail=None)
        await cb.answer("Sᴜᴄᴄᴇssғᴜʟʟʏ Rᴇᴍᴏᴠᴇᴅ Cᴜsᴛᴏᴍ Tʜᴜᴍʙɴᴀɪʟ!", show_alert=True)
        await OpenSettings(cb.message, user_id=cb.from_user.id)
    elif ("triggerCaption" in cb.data) or ("forceChangeCaption" in cb.data):
        custom_caption_ = await db.get_caption(cb.from_user.id)
        if custom_caption_ is not None:
            try:
                await cb.message.edit(
                    text=f"**Current Custom Caption:**\n\n`{custom_caption_}`",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cʜᴀɴɢᴇ Cᴜsᴛᴏᴍ Cᴀᴘᴛɪᴏɴ ✍︎", callback_data="forceChangeCaption")]])
                )
            except MessageNotModified:
                pass
            if "forceChangeCaption" not in cb.data:
                return
        elif custom_caption_ is None:
            await cb.answer("You didn't set any File Caption!", show_alert=True)
        await cb.message.edit(
            text="**Sᴇɴᴛ ᴍᴇ Cᴜsᴛᴏᴍ Fɪʟᴇ Cᴀᴘᴛɪᴏɴ!**"
        )
        try:
            ask_: Message = await bot.listen(cb.message.chat.id, timeout=300)
            if ask_.text and (ask_.text.startswith("/") is False):
                if len(ask_.text) > 1024:
                    await ask_.reply_text(
                        "**Mᴀᴋᴇ ᴛʜᴇ Cᴀᴘᴛɪᴏɴ ᴛᴇxᴛ Sᴍᴀʟʟᴇʀ...**",
                        quote=True,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton("ᴛʀʏ ᴀɢᴀɪɴ", callback_data="triggerCaption")],
                                [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="openSettings")]
                            ]
                        )
                    )
                    return
                caption = ask_.text.markdown
                await ask_.delete(True)
                await db.set_caption(cb.from_user.id, caption=caption)
                await cb.message.edit(
                    "**Custom Caption Removed Successfully!**",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("ʙᴀᴄᴋ ᴛᴏ sᴇᴛᴛɪɴɢs", callback_data="openSettings")],
                        [InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="closeMeh")]
                    ])
                )
            elif ask_.text and (ask_.text.startswith("/") is True):
                await cb.message.edit(
                    text="**Process Cancelled!**",
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="openSettings")]])
                )
        except TimeoutError:
            await cb.message.edit(
                text="**🤬 I can't wait more.... BYE 👋🏻**",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔚 Go Back", callback_data="openSettings")]])
            )


RenameBot.run()









RenameBot.run()
