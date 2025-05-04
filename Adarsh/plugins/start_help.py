# (c) adarsh-goel 

from Adarsh.bot import StreamBot
from Adarsh.vars import Var
import logging
logger = logging.getLogger(__name__)
from Adarsh.bot.plugins.stream import MY_PASS
from Adarsh.utils.human_readable import humanbytes
from Adarsh.utils.database import Database
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from Adarsh.utils.file_properties import get_name, get_hash, get_media_file_size
db = Database(Var.DATABASE_URL, Var.name)
"""
from pyrogram.types import ReplyKeyboardMarkup

if MY_PASS:
            buttonz=ReplyKeyboardMarkup(
            [
                ["start⚡️"] #,"help📚","login🔑","DC"],
               # ["follow❤️","ping📡","status📊","maintainers😎"]
                        
            ],
            resize_keyboard=True
        )
else:
            buttonz=ReplyKeyboardMarkup(
            [
                ["start⚡️"] #,"help📚","DC"],
             #   ["follow❤️","ping📡","status📊","maintainers😎"]
                        
            ],
            resize_keyboard=True
        )

        """    
            
@StreamBot.on_message((filters.command("start") | filters.regex('start⚡️')) & filters.private )
async def start(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"**<u>✅ کاربر جدیدی به ربات پیوست 😍</u> \n\n__🔺 نام کاربر  :__ [{m.from_user.first_name}](tg://user?id={m.from_user.id}) \n __🤖 ربات : @IR_FileToLinkBot__ **"
        )
    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
            if user.status == "kicked":
                await b.send_message(
                    chat_id=m.chat.id,
                    text="__𝓢𝓞𝓡𝓡𝓨, 𝓨𝓞𝓤 𝓐𝓡𝓔 𝓐𝓡𝓔 𝓑𝓐𝓝𝓝𝓔𝓓 𝓕𝓡𝓞𝓜 𝓤𝓢𝓘𝓝𝓖 𝓜𝓔. 𝓒ᴏɴᴛᴀᴄᴛ ᴛʜᴇ 𝓓ᴇᴠᴇʟᴏᴘᴇʀ__\n\n  **𝙃𝙚 𝙬𝙞𝙡𝙡 𝙝𝙚𝙡𝙥 𝙮𝙤𝙪**",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
             await StreamBot.send_photo(
                chat_id=m.chat.id,
                photo="https://telegra.ph/file/19eeb26fa2ce58765917a.jpg",
                caption="<b>• برای کارکردن ربات در کانال زیر عضو شوید.\n\n🔚 سپس /start را کلیک کنید.😊👇👇</b>",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("✅ عضویت ⚡️", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                
            )
             return
        except Exception:
            await b.send_message(
                chat_id=m.chat.id,
                text="<i>𝓢𝓸𝓶𝓮𝓽𝓱𝓲𝓷𝓰 𝔀𝓮𝓷𝓽 𝔀𝓻𝓸𝓷𝓰</i> <b> <a href='https://t.me/vj_bot_disscussion'>CLICK HERE FOR SUPPORT </a></b>",
                
                disable_web_page_preview=True)
            return
    await StreamBot.send_photo(
        chat_id=m.chat.id,
        photo ="https://telegra.ph/file/19eeb26fa2ce58765917a.jpg",
        caption =f'**👋 سلام {m.from_user.mention(style="md")} | 🥰😉\n\n• به ربات فایل به لینک خوش آمدید ❤️\n\n• هم اکنون یک فایل برایم ارسال کنید تا من\nلینک مستقیم اونو براتون ارسال کنم.🤩\n\n🖍️ سازنده ربات : [FﾑRSみɨの-BﾑŊの](t.me/Farshidband) **',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("کانال پشتیبانی", url=f"https://t.me/{Var.UPDATES_CHANNEL}")]]))

@StreamBot.on_message((filters.command("help")) & filters.private )
async def help_handler(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(
            Var.BIN_CHANNEL,
            f"**<u>✅ کاربر جدیدی به ربات پیوست 😍</u> \n\n__🔺 نام کاربر  :__ [{m.from_user.first_name}](tg://user?id={m.from_user.id}) \n __🤖 ربات : @IR_FileToLinkBot__ **"
       )
    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await bot.get_chat_member(Var.UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="<i>Sᴏʀʀʏ Sɪʀ, Yᴏᴜ ᴀʀᴇ Bᴀɴɴᴇᴅ FROM USING ᴍᴇ. Cᴏɴᴛᴀᴄᴛ ᴛʜᴇ Dᴇᴠᴇʟᴏᴘᴇʀ</i>",
                    
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await StreamBot.send_photo(
                chat_id=message.chat.id,
                photo="https://telegra.ph/file/19eeb26fa2ce58765917a.jpg",
                Caption="**• برای کارکردن ربات در کانال زیر عضو شوید.\n\n__🔚 سپس /start را کلیک کنید.😊👇👇__ **",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("✅ عضویت ⚡️", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                
            )
            return
        except Exception:
            await bot.send_message(
                chat_id=message.chat.id,
                text="__Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ Wʀᴏɴɢ. Cᴏɴᴛᴀᴄᴛ ᴍᴇ__ [VJ](https://t.me/anjel_neha).",
                disable_web_page_preview=True)
            return
                   
    await message.reply_text(
        text="""<b> Send me any file or video i will give you streamable link and download link.</b>\n
<b> I also support Channels, add me to you Channel and send any media files and see miracle✨ also send /list to know all commands""",
        
        disable_web_page_preview=True,
                
        reply_markup=InlineKeyboardMarkup(
            [
               # [InlineKeyboardButton("💁‍♂️ DEV", url="https://t.me/anjel_neha")],
                [InlineKeyboardButton("کانال پشتیبانی", url="https://t.me/ir_botz")]
            ]
        ) 
  )
