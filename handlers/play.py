from __future__ import unicode_literals
from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from pyrogram.types import CallbackQuery
from youtube_search import YoutubeSearch
import aiohttp
import wget
import youtube_dl
import json
from Python_ARQ import ARQ
import asyncio
import aiofiles
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os
from tgcalls import pytgcalls
import tgcalls
from converter import convert
from youtube import download
import sira
from config import DURATION_LIMIT
from helpers.wrappers import errors, admins_only
from helpers.errors import DurationLimitError


chat_id = None
@Client.on_message(
    filters.command("hdhdmdsj")
    & filters.group
    & ~ filters.edited
)
@errors
async def play(client: Client, message_: Message):
    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"**{bn} :-** 😕 Ses Dosyası Uzun {DURATION_LIMIT} minute(s) izin verilmez!\n🤐 Sağlanan ses, {audio.duration / 60} minute(s)"
            )

        file_name = get_file_name(audio)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    elif url:
        file_path = await converter.convert(youtube.download(url))
    else:
        return await message.reply_text(f"**{bn} :-** 🙄 Bana oynatacak bir şey vermedin.!")

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        await message.reply_text(f"**{bn} :-** 😉 Sıraya Alındı. Sırası= #{await callsmusic.queues.put(message.chat.id, file_path=file_path)} !")
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_text(f"**{bn} :-** 🥳 Oynatılıyor...")


#---------------------------------DEEZER------------------------------------------------------------------
@Client.on_message(
    filters.command("deezer")
    & filters.group
    & ~ filters.edited
)
async def deezer(client: Client, message_: Message):
    requested_by = message_.from_user.first_name
    text = message_.text.split(" ", 1)
    queryy = text[1]
    res = await message_.reply_text(f"Searching for `{queryy}` on deezer")
    try:
        arq = ARQ("https://thearq.tech")
        r = await arq.deezer(query=queryy, limit=1)
        title = r[0]["title"]
        duration = int(r[0]["duration"])
        thumbnail = r[0]["thumbnail"]
        artist = r[0]["artist"]
        url = r[0]["url"]
    except:
        await res.edit(
            "Kelimenin tam anlamıyla hiçbir şey bulamadım, İngilizceniz üzerinde çalışmalısınız!"
        )
        is_playing = False
        return
    file_path= await convert(wget.download(url))
    await res.edit("Generating Thumbnail")
    await generate_cover_square(requested_by, title, artist, duration, thumbnail)
    if message_.chat.id in tgcalls.pytgcalls.active_calls:
        await res.edit("adding in queue")
        position = sira.add(message_.chat.id, file_path)
        await res.edit_text(f"✯𝗕𝗼𝘁✯=#️⃣ Sıraya alındı. Sırası = {position}.")
    else:
        await res.edit_text("✯𝗕𝗼𝘁✯=▶️ Oynatılıyor.....")
        tgcalls.pytgcalls.join_group_call(message_.chat.id, file_path)
    await res.delete()
    m = await client.send_photo(
        chat_id=message_.chat.id,
        photo="final.png",
        caption=f"Oynatılıyor [{title}]({url}) Via [Deezer](https://t.me/Saygisizlar)."
    ) 
    os.remove("final.png")
# -----------------------------------------------------Jiosaavn-----------------------------------------------------------------
@Client.on_message(
    filters.command("saavn")
    & filters.group
    & ~ filters.edited
)
async def jiosaavn(client: Client, message_: Message):
    requested_by = message_.from_user.first_name
    chat_id=message_.chat.id
    text = message_.text.split(" ", 1)
    query = text[1]
    res = await message_.reply_text(f"Searching for `{query}` on jio saavn")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://jiosaavnapi.bhadoo.uk/result/?query={query}"
            ) as resp:
                r = json.loads(await resp.text())
        sname = r[0]["song"]
        slink = r[0]["media_url"]
        ssingers = r[0]["singers"]
        sthumb = r[0]["image"]
        sduration = int(r[0]["duration"])
    except Exception as e:
        await res.edit(
            "Found Literally Nothing!, You Should Work On Your English."
        )
        print(str(e))
        is_playing = False
        return
    file_path= await convert(wget.download(slink))
    if message_.chat.id in tgcalls.pytgcalls.active_calls:
        position = sira.add(message_.chat.id, file_path)
        await res.edit_text(f"✯𝗕𝗼𝘁✯=#️⃣ Queued at position {position}.")
    else:
        await res.edit_text("✯𝗕𝗼𝘁✯=▶️ Playing.....")
        tgcalls.pytgcalls.join_group_call(message_.chat.id, file_path)
    await res.edit("Generating Thumbnail.")
    await generate_cover_square(requested_by, sname, ssingers, sduration, sthumb)
    await res.delete()
    m = await client.send_photo(
        chat_id=message_.chat.id,
        caption=f"Playing {sname} Via [Jiosaavn](https://t.me/Saygisizlar)",
        photo="final.png",
    )
    os.remove("final.png")


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage
 
 #-----------------------------------YOUTUBE--------------------------------------------------------------
@Client.on_message(
    filters.command("bul")
    & filters.group
    & ~ filters.edited
)
async def ytp(client: Client, message_: Message):
    requested_by = message_.from_user.first_name
    chat_id=message_.chat.id
    text = message_.text.split(" ", 1)
    query = text[1]
    res = await message_.reply_text(f"Aranıyor `{query}`  You Tube")
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"]
        thumbnail = results[0]["thumbnails"][0]
        duration = results[0]["duration"]
        views = results[0]["views"]
    except Exception as e:
        await res.edit(
            "Kelimenin tam anlamıyla hiçbir şey bulamadım!"
        )
        is_playing = False
        print(str(e))
        return
    file_path = await convert(download(link))
    if message_.chat.id in tgcalls.pytgcalls.active_calls:
        position = sira.add(message_.chat.id, file_path)
        await res.edit_text(f"✯𝗕𝗼𝘁✯=#️⃣ Sıraya alındı. Sırası = {position}.")
    else:
        await res.edit_text("✯𝗕𝗼𝘁✯=▶️ Oynatılıyor....")
        tgcalls.pytgcalls.join_group_call(message_.chat.id, file_path)
    await res.edit("Generating Thumbnail.")
    await generate_cover(requested_by, title, views, duration, thumbnail)
    res.delete
    m = await client.send_photo(
        chat_id=message_.chat.id,
        caption=f"Playing `{query}` Via [YouTube](https://t.me/Saygisizlar)",
        photo="final.png",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Watch on youtube", url=link)]]
        ),
        parse_mode="markdown",
    )
    os.remove("final.png")

async def generate_cover_square(requested_by, title, artist, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()
    image1 = Image.open("./background.png")
    image2 = Image.open("Others/AURAX.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Others/font.otf", 32)
    draw.text((190, 550), f"Title: {title}", (255, 255, 255), font=font)
    draw.text((190, 550), f"Artist: {artist}", (255, 255, 255), font=font)
    draw.text(
        (190, 590),
        f"Duration: {duration} Seconds",
        (255, 255, 255),
        font=font,
    )

    draw.text(
        (190, 670),
        f"Played By: {requested_by}",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")


# Generate cover for youtube

async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image1 = Image.open("./background.png")
    image2 = Image.open("Others/AURAX.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Others/font.otf", 32)
    draw.text((190, 550), f"Title: {title}", (255, 255, 255), font=font)
    draw.text(
        (190, 590), f"Duration: {duration}", (255, 255, 255), font=font
    )
    draw.text((190, 630), f"Views: {views}", (255, 255, 255), font=font)
    draw.text((190, 670),
        f"Played By: {requested_by}",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")
