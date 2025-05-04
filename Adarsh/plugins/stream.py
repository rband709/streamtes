
# (c) Adarsh-Goel
import os
import asyncio
from asyncio import TimeoutError
from Adarsh.bot import StreamBot
from Adarsh.utils.database import Database
from Adarsh.utils.human_readable import humanbytes
from Adarsh.vars import Var
from urllib.parse import quote_plus
from pyrogram import filters, Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Adarsh.utils.file_properties import get_name, get_hash, get_media_file_size

db = Database(Var.DATABASE_URL, Var.name)

MY_PASS = os.environ.get("MY_PASS", None)
pass_dict = {}
pass_db = Database(Var.DATABASE_URL, "ag_passwords")


@StreamBot.on_message((filters.regex("login🔑") | filters.command("login")), group=4)
async def login_handler(c: Client, m: Message):
    try:
        ag = await m.reply_text(
            "Now send me password.\n\nIf you don't know, check the MY_PASS Variable in Heroku.\n\n(You can use /cancel to cancel)"
        )
        try:
            _text = await c.listen(m.chat.id, filters=filters.text, timeout=90)
            textp = _text.text
            if textp == "/cancel":
                await ag.edit("Process Cancelled Successfully")
                return
        except TimeoutError:
            await ag.edit("Timeout! Try again.")
            return

        if textp == MY_PASS:
            await pass_db.add_user_pass(m.chat.id, textp)
            ag_text = "Yeah! You entered the password correctly."
        else:
            ag_text = "Wrong password. Try again."
        await ag.edit(ag_text)

    except Exception as e:
        print(e)


@StreamBot.on_message((filters.private) & (filters.document | filters.video | filters.audio | filters.photo), group=4)
async def private_receive_handler(c: Client, m: Message):
    if MY_PASS:
        check_pass = await pass_db.get_user_pass(m.chat.id)
        if check_pass is None:
            await m.reply_text("Login first using /login\nDon’t know the password? Ask the developer.")
            return
        if check_pass != MY_PASS:
            await pass_db.delete_user(m.chat.id)
            return

    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await c.send_message(
            Var.BIN_CHANNEL,
            f"<u>✅ کاربر جدیدی به ربات پیوست 😍</u>\n\n🔺 نام کاربر: [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n🤖 ربات: @IR_FileToLinkBot"
        )

    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await c.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
            if user.status == "kicked":
                await c.send_message(
                    m.chat.id,
                    "You are banned!\n\n**Contact Developer [VJ](https://t.me/TamilBots)**",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await c.send_message(
                m.chat.id,
                "<b>• برای کارکردن ربات در کانال زیر عضو شوید.\n\n🔚 سپس /start را کلیک کنید.😊👇👇</b>",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("✅ عضویت ⚡️", url=f"https://t.me/{Var.UPDATES_CHANNEL}")]]
                )
            )
            return
        except Exception as e:
            await m.reply_text(str(e))
            return

    try:
        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)

        file_name = get_name(log_msg) or "Unknown_File"
        file_hash = get_hash(log_msg)
        stream_link = f"{Var.URL}watch/{log_msg.id}/{quote_plus(file_name)}?hash={file_hash}"
        online_link = f"{Var.URL}{log_msg.id}/{quote_plus(file_name)}?hash={file_hash}"

        msg_text = (
            f"<b><u>✅ لینک دانلود باموفقیت ساخته شد .</u></b>\n\n"
            f"<b>📂 نام فایل :</b>\n<i>{file_name}</i>\n\n"
            f"<b>📦 حجم فایل :</b> <i>{humanbytes(get_media_file_size(m))}</i>\n\n"
            f"<b>⚠️ این لینک تا 30 دقیقه معتبر میباشد.</b>\n\n"
            f"<b>🖍️ سازنده ربات : [FﾑRSみɨの-BﾑŊの](t.me/farshidband)</b>"
        )

        await log_msg.reply_text(
            f"**Requested by:** [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n"
            f"**User ID:** `{m.from_user.id}`\n"
            f"**Stream link:** {online_link}",
            disable_web_page_preview=True,
            quote=True
        )

        await m.reply_text(
            text=msg_text,
            quote=True,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔗 لینک دانلود ⚡️", url=online_link)]])
        )

    except FloodWait as e:
        print(f"Sleeping for {e.value}s")
        await asyncio.sleep(e.value)
        await c.send_message(
            chat_id=Var.BIN_CHANNEL,
            text=(
                f"GOT FLOODWAIT of {e.value}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n"
                f"**User ID:** `{m.from_user.id}`"
            ),
            disable_web_page_preview=True
        )


@StreamBot.on_message(filters.channel & ~filters.group & (filters.document | filters.video | filters.photo) & ~filters.forwarded, group=-1)
async def channel_receive_handler(bot, broadcast):
    if MY_PASS:
        check_pass = await pass_db.get_user_pass(broadcast.chat.id)
        if check_pass is None:
            await broadcast.reply_text("Login first using /login\nDon’t know the password? Ask developer!")
            return
        if check_pass != MY_PASS:
            await broadcast.reply_text("Wrong password, login again")
            await pass_db.delete_user(broadcast.chat.id)
            return

    if int(broadcast.chat.id) in Var.BANNED_CHANNELS:
        await bot.leave_chat(broadcast.chat.id)
        return

    try:
        log_msg = await broadcast.forward(chat_id=Var.BIN_CHANNEL)

        file_name = get_name(log_msg) or "Unknown_File"
        file_hash = get_hash(log_msg)
        stream_link = f"{Var.URL}watch/{log_msg.id}/{quote_plus(file_name)}?hash={file_hash}"
        online_link = f"{Var.URL}{log_msg.id}/{quote_plus(file_name)}?hash={file_hash}"

        await log_msg.reply_text(
            f"**Channel Name:** `{broadcast.chat.title}`\n"
            f"**CHANNEL ID:** `{broadcast.chat.id}`\n"
            f"**Request URL:** {stream_link}",
            quote=True
        )

        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            message_id=broadcast.id,
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("🖥STREAM", url=stream_link),
                    InlineKeyboardButton("DOWNLOAD 📥", url=online_link)
                ]]
            )
        )

    except FloodWait as w:
        print(f"Sleeping for {w.value}s")
        await asyncio.sleep(w.value)
        await bot.send_message(
            chat_id=Var.BIN_CHANNEL,
            text=(
                f"GOT FLOODWAIT of {w.value}s from {broadcast.chat.title}\n"
                f"**CHANNEL ID:** `{broadcast.chat.id}`"
            ),
            disable_web_page_preview=True
        )
    except Exception as e:
        await bot.send_message(
            chat_id=Var.BIN_CHANNEL,
            text=f"**#ERROR_TRACEBACK:** `{e}`",
            disable_web_page_preview=True
        )
        print(f"Error while editing broadcast message: {e}")
