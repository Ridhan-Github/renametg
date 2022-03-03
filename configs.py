# (c) @AbirHasan2005

import os


class Config(object):
    API_ID = int(os.environ.get("API_ID", 12345))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    SESSION_NAME = os.environ.get("SESSION_NAME", "Rename-Bot-0")
    SLEEP_TIME = int(os.environ.get("SLEEP_TIME", 5))
    BOT_OWNER = int(os.environ.get("BOT_OWNER", 1445283714))
    CAPTION = "**© ᴊᴏɪɴ : @Disney_Bots **"
    UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", None)
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", -100))
    MONGODB_URI = os.environ.get("MONGODB_URI", "")
    DOWNLOAD_PATH = os.environ.get("DOWNLOAD_PATH", "./downloads")
    BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", False))
    ONE_PROCESS_ONLY = bool(os.environ.get("ONE_PROCESS_ONLY", False))
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    DOWNLOAD_START ="Pʀᴏᴄᴇssɪɴɢ ᴛᴏ Dᴏᴡɴʟᴏᴀᴅ"
    # Telegram maximum file upload size
    SAVED_RECVD_DOC_FILE ="ʏᴏᴜʀ ғɪʟᴇ sᴀᴠᴇᴅ"
    START_TEXT = """👋 Hᴇʟʟᴏ , {} 

Tʜɪꜱ ɪꜱ ꜰɪʟᴇ ʀᴇɴᴀᴍᴇ ʙᴏᴛ ᴡɪᴛʜ ғɪʟᴇ ᴄᴀᴘᴛɪᴏɴ

Pʀᴇꜱꜱ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ꜰᴏʀ ᴍᴏʀᴇ ɪɴꜰᴏ...

Pᴏᴡᴇʀᴇᴅ ʙʏ : [ᴅɪsɴᴇʏ ʙᴏᴛ](t.me/Disney_bots)

"""
    PROGRESS = """
<b>📁 Sɪᴢᴇ : {1} ✗ {2} </b>\n\n
<b>🚀 Sᴘᴇᴇᴅ : {3}</b>/s\n\n
<b>⏱️ Eᴛᴀ : {4}</b>\n\n
"""
    
    ABOUT_TEXT = """
**Mʏ ɴᴀᴍᴇ** : [ʀᴇɴᴀᴍᴇʀ ᴘʀᴏ ʙᴏᴛ](http://t.me/RenamerXProRobot)

**Cʜᴀɴɴᴇʟ** : [ᴅɪsɴᴇʏ ʙᴏᴛs](https://t.me/Disney_Bots)

**Vᴇʀꜱɪᴏɴ** : [1.0 ʙᴇᴛᴀ](http://t.me/RenamerXProRobot)

**Sᴏᴜʀᴄᴇ** : [ᴄʟɪᴄᴋ ʜᴇʀᴇ](https://t.me/Tamilanbots)

**Sᴇʀᴠᴇʀ** : [ʜᴇʀᴏᴋᴜ](https://heroku.com/)

**Lᴀɴɢᴜᴀɢᴇ :** [Pʏᴛʜᴏɴ 3.10.2](https://www.python.org/)

**Fʀᴀᴍᴇᴡᴏʀᴋ :** [ᴘʏʀᴏɢᴀᴍ 1.3.6](https://docs.pyrogram.org/)

**Dᴇᴠᴇʟᴏᴘᴇʀ :** [EᴀʀɴMᴏɴᴇʏVIP](https://t.me/Tamilanbots)

**Pᴏᴡᴇʀᴇᴅ ʙʏ :** [@DɪsɴᴇʏHDLɪɴᴋs](https://t.me/DisneyHDlinks)

"""

    HELP_TEXT = """Yᴏᴜ ɴᴇᴇᴅ Hᴇʟᴘ ?? 
   
𖣘 Fɪʀsᴛ ɢᴏ ᴛᴏ ᴛʜᴇ /sᴇᴛᴛɪɴɢs ᴀɴᴅ ᴄʜᴀɴɢᴇ ᴛʜᴇ ʙᴏᴛ ʙᴇʜᴀᴠɪᴏʀ ᴀs ʏᴏᴜʀ ᴄʜᴏɪᴄᴇ.

𖣘 Sᴇɴᴅ ᴍᴇ ᴛʜᴇ ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ ᴛᴏ sᴀᴠᴇ ɪᴛ ᴘᴇʀᴍᴀɴᴇɴᴛʟʏ. (𝚘𝚙𝚝𝚒𝚘𝚗𝚊𝚕)

𖣘 Nᴏᴡ sᴇɴᴅ ᴍᴇ ᴛʜᴇ ғɪʟᴇ ᴏʀ ᴠɪᴅᴇᴏ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ʀᴇɴᴀᴍᴇ.

𖣘 Aғᴛᴇʀ ᴛʜᴀᴛ ʙᴏᴛ ᴡɪʟʟ ᴀsᴋ ʏᴏᴜ ғᴏʀ ᴛʜᴇ Nᴇᴡ Nᴀᴍᴇ ᴛʜᴇɴ sᴇɴᴅ ᴛʜᴇ Nᴇᴡ ғɪʟᴇ ɴᴀᴍᴇ ᴡɪᴛʜ ᴏʀ ᴡɪᴛʜᴏᴜᴛ Exᴛᴇɴᴛɪᴏɴ.

𖣘 Tʜᴇɴ ʙᴇ ʀᴇʟᴀxᴇᴅ ʏᴏᴜʀ ғɪʟᴇ ᴡɪʟʟ ʙᴇ ᴜᴘʟᴏᴀᴅᴇᴅ sᴏᴏɴ..


⚠︎ Nᴏᴛᴇ: Iғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴄʜᴀɴɢᴇ ʙᴏᴛ ᴄᴀᴘᴛɪᴏɴ Gᴏ ᴛᴏ /settings >> Cᴜsᴛᴏᴍ Cᴀᴘᴛɪᴏɴ
"""
