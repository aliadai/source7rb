
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
import signal

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

def run_ytdlp_sync(url, ydl_opts):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        
        # Check file size before downloading
        filesize = info.get('filesize') or info.get('filesize_approx') or 0
        if filesize > 100 * 1024 * 1024:  # 100MB limit
            raise Exception("الملف كبير جداً (أكثر من 100 ميجابايت)")
        
        # Check duration for videos
        duration = info.get('duration', 0)
        if duration > 900:  # 15 minutes limit
            raise Exception("الفيديو طويل جداً (أكثر من 15 دقيقة)")
        
        # Now download
        ydl.download([url])
        filename = ydl.prepare_filename(info)
        description = info.get('description', info.get('title', 'محتوى'))
        if description and len(description) > 100:
            description = description[:100] + '...'
        return filename, description or 'محتوى'

async def download_with_ytdlp(url):
    platform = detect_platform(url)
    
    if platform == 'youtube':
        # Optimized settings for YouTube
        ydl_opts = {
            'format': 'best[filesize<100M][ext=mp4]/best[height<=720][ext=mp4]/best[ext=mp4]',
            'outtmpl': '%(epoch)s.%(ext)s',
            'no_warnings': True,
            'quiet': True,
            'socket_timeout': 25,
            'fragment_retries': 2,
            'retries': 2,
        }
    elif platform == 'pinterest':
        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(epoch)s.%(ext)s',
            'no_warnings': True,
            'quiet': True,
        }
    else:
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': '%(epoch)s.%(ext)s',
            'no_warnings': True,
            'quiet': True,
            'socket_timeout': 20,
        }
    
    # Run in thread pool to make it truly async
    loop = asyncio.get_event_loop()
    try:
        filename, description = await loop.run_in_executor(None, run_ytdlp_sync, url, ydl_opts)
        return filename, description
    except Exception as e:
        raise e

@l313l.ar_cmd(pattern="حمل[\+\s]*(.*)")
async def universal_dl(event):
    link = event.pattern_match.group(1).strip()
    
    if not link:
        return await event.reply("الاستخدام: .حمل الرابط")
    
    # Delete original message
    await event.message.delete()
    
    # Send processing message  
    platform = detect_platform(link)
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
            # Set timeout for the entire operation
            try:
                filename, title = await asyncio.wait_for(download_with_ytdlp(link), timeout=120.0)  # 2 minutes timeout
            except asyncio.TimeoutError:
                raise Exception("انتهت مهلة التحميل (أكثر من دقيقتين)")
            
            # Check if file exists and get size
            if not os.path.exists(filename):
                raise Exception("فشل في تحميل الملف")
                
            filesize_bytes = os.path.getsize(filename)
            filesize = filesize_bytes / (1024 * 1024)
            
            # Check final file size
            if filesize > 100:
                os.remove(filename)
                raise Exception("الملف كبير جداً للإرسال")
            
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
        elif "كبير جداً" in error_msg or "طويل جداً" in error_msg:
            await a.edit(error_msg)
        elif "انتهت مهلة" in error_msg:
            await a.edit("انتهت مهلة التحميل، الملف كبير جداً")
        elif "rate-limited" in error_msg.lower() or "try again later" in error_msg.lower():
            await a.edit("يوتيوب يحد من التحميل حالياً، جرب بعد قليل أو استخدم رابط آخر")
        elif "video unavailable" in error_msg.lower():
            await a.edit("الفيديو غير متاح أو محذوف من يوتيوب")
        else:
            await a.edit("حدث خطأ في التحميل، جرب رابط آخر")
