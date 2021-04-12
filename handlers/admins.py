from pyrogram import Client, filters
from pyrogram.types import Message
import tgcalls
import sira
from config import SUDO_USERS
from cache.admins import set
from helpers.wrappers import errors, admins_only


@Client.on_message(
    filters.command("durdur")
    & filters.group
    & ~ filters.edited
)
@errors
@admins_only
async def pause(client: Client, message: Message):
    tgcalls.pytgcalls.pause_stream(message.chat.id)
    await message.reply_text("✯𝗕𝗼𝘁✯=⏸ Durduruldu.")


@Client.on_message(
    filters.command("devam")
    & filters.group
    & ~ filters.edited
)
@errors
@admins_only
async def resume(client: Client, message: Message):
    tgcalls.pytgcalls.resume_stream(message.chat.id)
    await message.reply_text("✯𝗕𝗼𝘁✯=▶️ Devam Ediyor.")


@Client.on_message(
    filters.command(["bitir"])
    & filters.group
    & ~ filters.edited
)
@errors
@admins_only
async def stop(client: Client, message: Message):
    try:
        sira.clear(message.chat.id)
    except:
        pass

    tgcalls.pytgcalls.leave_group_call(message.chat.id)
    await message.reply_text("✯𝗕𝗼𝘁✯=⏹ Bitirildi.")


@Client.on_message(
    filters.command(["atla"])
    & filters.group
    & ~ filters.edited
)
@errors
@admins_only
async def skip(client: Client, message: Message):
    chat_id = message.chat.id

    sira.task_done(chat_id)
    await message.reply_text("Processing")
    if sira.is_empty(chat_id):
        tgcalls.pytgcalls.leave_group_call(chat_id)
        await message.reply_text("nothing in queue")
    else:
        tgcalls.pytgcalls.change_stream(
            chat_id, sira.get(chat_id)["file_path"]
        )

        await message.reply_text("✯𝗕𝗼𝘁✯=⏩ Sonraki Şarkıya Atlandı.")


@Client.on_message(
    filters.command("yenile")
)
@errors
@admins_only
async def admincache(client, message: Message):
    set(message.chat.id, [member.user for member in await message.chat.get_members(filter="administrators")])
    await message.reply_text("✯𝗕𝗼𝘁✯=❇️ Yenilendi!")

@Client.on_message(
    filters.command("yardım") 
    & filters.group
    & ~ filters.edited
)
async def helper(client , message:Message):
     await message.reply_text("Komutlar ve kullanım burada açıklanmıştır-: \n `/saavn` To search song on jio saavan and play the first result \n `/deezer` To search the song on deezer and get good quality stream \n `/song` To search the song on Youtube and play the first matching result \n '/play` Reply this in response to a link or any telegram audio file it will be played \n `/skip` to skip current song \n `/stop or /kill` to stop the streaming of song \n `/pause` to pause the stream \n `/resume` to resume the playback. \n Inline search is also supported. \n More info join group @TeLeTiPsOfficialOnTopicChat")
