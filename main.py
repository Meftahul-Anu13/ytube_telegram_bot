import os
import logging
import re
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, Application, ConversationHandler, ContextTypes
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('BOT_TOKEN')

ASK_CHOICE, DOWNLOAD_VIDEO, DOWNLOAD_MP3 = range(3)

def extract_video_id(url):
    """
    Extract video ID from a YouTube URL.
    Handles standard and Shorts URLs.
    """
    pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:watch\?v=|shorts/)|youtu\.be/)([^\?&/]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

def construct_url(video_id):
    """
    Construct a standard YouTube video URL from the video ID.
    """
    return f"https://www.youtube.com/watch?v={video_id}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hi! Send me a YouTube link (video or Shorts), and I will ask what you want to do with it.')

async def url_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['url'] = update.message.text
    await update.message.reply_text('Do you want to download the video or the audio? Please reply with /download_video or /download_mp3.')
    return ASK_CHOICE

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = context.user_data.get('url')
    if not url:
        await update.message.reply_text('No URL provided. Please send a YouTube link first.')
        return ConversationHandler.END

    try:
        # Extract video ID and construct URL
        video_id = extract_video_id(url)
        video_url = construct_url(video_id)
        logger.info(f'Downloading video from {video_url}...')
        progress_message = await update.message.reply_text(f'Downloading video...')

        yt = YouTube(video_url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').first()
        out_file = video.download(output_path='downloads')
        
        await context.bot.delete_message(chat_id=update.message.chat_id, message_id=progress_message.message_id)
        

        await update.message.reply_text('Video downloaded successfully!')

        with open(out_file, 'rb') as video_file:
            await context.bot.send_video(chat_id=update.message.chat_id, video=video_file)

        os.remove(out_file)
    except Exception as e:
        logger.error(f'An error occurred: {e}')
        await update.message.reply_text(f'An error occurred: {e}')
    
    return ConversationHandler.END

async def download_mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = context.user_data.get('url')
    if not url:
        await update.message.reply_text('No URL provided. Please send a YouTube link first.')
        return ConversationHandler.END

    try:
        
        video_id = extract_video_id(url)
        video_url = construct_url(video_id)
        logger.info(f'Downloading audio from {video_url}...')
        progress_message = await update.message.reply_text(f'Downloading audio...')

        yt = YouTube(video_url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').first()
        out_file = video.download(output_path='downloads')

        video_clip = VideoFileClip(out_file)
        audio_file = out_file.replace('.mp4', '.mp3')
        video_clip.audio.write_audiofile(audio_file)
        video_clip.close()

        
        await context.bot.delete_message(chat_id=update.message.chat_id, message_id=progress_message.message_id)
        
        
        await update.message.reply_text('MP3 downloaded successfully!')
        

        with open(audio_file, 'rb') as audio:
            await context.bot.send_audio(chat_id=update.message.chat_id, audio=audio)

        os.remove(out_file)
        os.remove(audio_file)
    except Exception as e:
        logger.error(f'An error occurred: {e}')
        await update.message.reply_text(f'An error occurred: {e}')
    
    return ConversationHandler.END

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.warning(f'Update {update} caused error {context.error}')

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), MessageHandler(filters.TEXT & ~filters.COMMAND, url_received)],
        states={
            ASK_CHOICE: [
                CommandHandler('download_video', download_video),
                CommandHandler('download_mp3', download_mp3)
            ],
        },
        fallbacks=[],
    )

    app.add_handler(conv_handler)

    app.add_error_handler(error)

    logger.info("Bot started, polling...")
    app.run_polling(poll_interval=5)

if __name__ == '__main__':
    main()
