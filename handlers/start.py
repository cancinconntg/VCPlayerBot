from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton



@Client.on_message(
    filters.command("start")
    & filters.private
    & ~ filters.edited
)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>Merhaba {message.from_user.first_name}!
⚜️ /oynat - Yanıtlanan ses dosyasını veya YouTube videosunu bağlantı üzerinden çalar.
⚜️ /durdur - Sesli Sohbet Müziğini Duraklat.
⚜️ /devam - Sesli Sohbet Müziğine Devam Et.
⚜️ /atla - Sesli Sohbette Çalan Geçerli Müziği Atlar.
⚜️ /bitir - Sırayı temizler ve Sesli Sohbet Müziği'ni sona erdirir.
⚜️ /yenile - Botu yeniler. Admin listesi yenilenir.
⚜️ /bul - Müziği youtube den bulur gruba gönderir. Örnek /bul Emir Can İğrek nalan. 
⚜️ /deezer - Müziği deezer den bulur gruba gönderir. Örnek /deezer Emir Can İğrek nalan. 
⚜️ /saavn - Müziği bulur. Fakat yabancı şarkılar. 
 </b>""",
      
       
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "👥 Group", url="https://t.me/TeLeTiPsOfficialOnTopicChat"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Join Channel", url="https://t.me/TeLeTiPsOfficialchannel"
                    )
                ]
            ]
        )
    )

@Client.on_message(
    filters.command("start")
    & filters.group
    & ~ filters.edited
)
async def start(client: Client, message: Message):
    await message.reply_text(
        "💁🏻‍♂️ Do you want to search for a YouTube video?",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✅ Yes", switch_inline_query_current_chat=""
                    ),
                    InlineKeyboardButton(
                        "No ❌", callback_data="close"
                    )
                ]
            ]
        )
    )
