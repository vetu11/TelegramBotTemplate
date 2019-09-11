# Telegram Bot Template

This is a template to make a Telegram bot on Python 3, it starts a few basic commands. It is intended for own usage, but you can use it 
if you want.

## Usage

You can find real examples of this project layout on other repositories of mine, but here are the basics:

* You will need to install the python-telegram-bot library

* To run the bot you must put the bot token given by [@botfather](t.me/botfather) on the bot_tokens.py file. If you want
  to use payments put there the payment provider token as well. With this done, the bot will run with the basic commands.

* Personalize the messages in the langs/ directory. If you want to add more languages or change the default you will
  have to do it on lang.py

* To add more commands or change how the behave declare/modify functions in handlers.py

* If you add more commands or need to get different Telegram Updates link the functions on handlers.py to the dispatcher
  on bot.py
