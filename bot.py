import config
import logging
import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types
from db_contoller import db_controller

from StopGame import stop_game

# Logging type
logging.basicConfig(level=logging.INFO)

# Initializing Bot
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

# DB connection
db = db_controller('db.db')

# Initializing Parser
sg = stop_game('lastkey.txt')


# Sub subscribe
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if not db.sub_exists(message.from_user.id):  # check if user exists in DB
        db.add_sub(message.from_user.id)  # add if it aint
        await message.answer("Вы подписались!")
    else:
        db.update_subscription(message.from_user.id, True)
        await message.answer("Вы переподписаны! \nОжидайте новостей =)")


# Sub unsubscribe
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if not db.sub_exists(message.from_user.id):  # check if user exists in DB
        db.add_sub(message.from_user.id, False)  # add if it aint and make sub field FALSE
        await message.answer("Вы и так не подписаны =/")
    else:
        db.update_subscription(message.from_user.id, False)  # if user exists in db - unsub
        await message.answer("Вы отписались")


# New games check
async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        new_games = sg.new_games()

        if (new_games):
            new_games.reverse()
            for ng in new_games:
                nfo = sg.game_info(ng)  # new game info
                subs = db.get_subscriptions()  # Getting subs from Data Base
                with open(sg.download_image(nfo['image']), 'rb') as photo:
                    for s in subs:
                        await bot.send_photo(
                            s[1],
                            photo,
                            caption=nfo['title'] + "\n" + "Оценка: " + nfo['score'] + "\n" + nfo['excerpt'] + "\n\n" +
                                    nfo['link'],
                            disable_notification=True
                        )
                sg.update_lastkey(nfo['id'])


# Long pool
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(10))
    executor.start_polling(dp, skip_updates=True)

