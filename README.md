# ordering_bot

## Description
This bot allows to order congratulation and song.
This bot based on [aiogram](https://github.com/aiogram/aiogram).


## How to run

* Clone the code from this repository
* Fill `.env` file (`.env.example` as example):
  * First, you'll need a Telegram Bot Token, you can get it via BotFather
([more info here](https://core.telegram.org/bots)).
  * Enter your Token in `.env`:
    > TOKEN = "Token_From_BotFather"
  * Load your tracklist (`tracklist.txt` as example). 
  You can name it otherwise than `tracklist.txt`, but you need to set TRACKLIST_NAME in `bot/config.py` as you named your tracklist file.

* Install requirements:  
  ``` make install ```
* Run bot:  
  ``` make run ```
