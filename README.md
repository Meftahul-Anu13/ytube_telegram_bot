# YouTube Bot

This is a Telegram bot that allows users to download YouTube videos or extract audio from YouTube videos. The bot can handle both standard YouTube URLs and YouTube Shorts URLs.

## Features
- Download YouTube videos in MP4 format.
- Extract and download audio from YouTube videos in MP3 format.
- Accessible at [t.me/@hi_ytube_download_bot](https://t.me/hi_ytube_download_bot) after deployment.

## Requirements

- Python 3.7+
- Telegram Bot API token

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/Meftahul-Anu13/ytube_telegram_bot.git
    cd ytube_telegram_bot
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your Telegram Bot API token:

    ```env
    BOT_TOKEN=your-telegram-bot-token
    ```


## Usage

1. Start the bot:

    ```sh
    python main.py
    ```

2. Open Telegram and start a chat with your bot. Send a YouTube link (video or Shorts), and the bot will ask if you want to download the video or the audio.

## Acknowledgements

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [pytube](https://github.com/kszczepanskidev/pytube)
- [moviepy](https://github.com/Zulko/moviepy)
- [dotenv](https://github.com/theskumar/python-dotenv)
