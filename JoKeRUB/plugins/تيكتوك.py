
import asyncio 
import shutil
import requests
from requests.exceptions import JSONDecodeError
import json
import os
import re
from bs4 import BeautifulSoup as bs
import time
from datetime import timedelta
import math
import base64
from JoKeRUB import l313l 
import yt_dlp

def detect_platform(url):
    url = url.lower()
    if 'tiktok.com' in url or 'vm.tiktok.com' in url:
        return 'tiktok'
    elif 'instagram.com' in url:
        return 'instagram'
    elif 'youtube.com' in url or 'youtu.be' in url:
        return 'youtube'
    elif 'twitter.com' in url or 'x.com' in url:
        return 'twitter'
    elif 'facebook.com' in url or 'fb.watch' in url:
        return 'facebook'
    elif 'snapchat.com' in url:
        return 'snapchat'
    elif 'pinterest.com' in url or 'pin.it' in url:
        return 'pinterest'
    else:
        return 'unknown'

async def download_with_ytdlp(url):
    platform = detect_platform(url)
    
    if platform == 'pinterest':
        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(epoch)s.%(ext)s',
            'no_warnings': True,
        }
    else:
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': '%(epoch)s.%(ext)s',
            'no_warnings': True,
            'extractaudio': False,
            'embed_subs': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
        }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            description = info.get('description', info.get('title', 'محتوى'))
            if description and len(description) > 200:
                description = description[:200] + '...'
            return filename, description or 'محتوى'
    except Exception as e:
        raise e

@l313l.ar_cmd(pattern="حمل\+(.*)")
async def universal_dl(event):
    link = event.pattern_match.group(1).strip()
    
    if not link:
        return await event.reply("الاستخدام: .حمل+الرابط")
    
    # Delete original message
    await event.message.delete()
    
    # Send processing message
    a = await l313l.send_message(event.chat_id, '⏳ جاري تحميل الفيديو...')
    
    try:
        # Detect platform
        platform = detect_platform(link)
        
        # Create temporary directory
        directory = str(round(time.time()))
        os.makedirs(directory, exist_ok=True)
        
        # Change to temp directory for download
        original_dir = os.getcwd()
        os.chdir(directory)
        
        try:
            # Download using yt-dlp for universal support
            filename, title = await download_with_ytdlp(link)
            
            # Get file info
            filesize_bytes = os.path.getsize(filename)
            filesize = filesize_bytes / (1024 * 1024)
            
            # Change back to original directory
            os.chdir(original_dir)
            
            # Update status
            await a.edit('📤 جاري رفع الفيديو...')
            
            # Get reply ID
            try:
                from ..helpers.utils import reply_id
                catid = await reply_id(event)
            except:
                catid = None
            
            # Send the file
            caption_text = f"{title}\n\nتم جلبه بواسطة @RobinSource"
            
            await l313l.send_file(
                event.chat_id, 
                f"{directory}/{filename}", 
                reply_to=catid,
                force_document=False,
                caption=caption_text
            )
            
        finally:
            # Change back to original directory if still in temp
            if os.getcwd().endswith(directory):
                os.chdir(original_dir)
        
        # Delete processing message
        await a.delete()
        
        # Clean up temporary directory
        if os.path.exists(directory):
            shutil.rmtree(directory)
            
    except Exception as er:
        # Clean up on error
        if os.getcwd().endswith(directory):
            os.chdir(original_dir)
        if os.path.exists(directory):
            shutil.rmtree(directory)
            
        error_msg = str(er)
        if "not supported" in error_msg.lower():
            await a.edit("هذا الرابط غير مدعوم حالياً")
        elif "private" in error_msg.lower():
            await a.edit("هذا المحتوى خاص ولا يمكن تحميله")
        elif "not found" in error_msg.lower():
            await a.edit("الرابط غير صحيح أو المحتوى محذوف")
        else:
            await a.edit(f"حدث خطأ في التحميل\n{error_msg}")
