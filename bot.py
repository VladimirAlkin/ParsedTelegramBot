import config
import logging

from aiogram import Bot, Dispatcher, executor, types
from db_contoller import db_controller


# Logging type
logging.basicConfig(level=logging.INFO)

# Initializing Bot
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

# DB connection
db = db_controller('db.db')

# Sub subscribe
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if not db.sub_exists(message.from_user.id): #check if user exists in DB
        db.add_sub(message.from_user.id) #add if it aint
        await message.answer("Вы подписались!")
    else:
        db.update_subscription(message.from_user.id, True)
        await message.answer("Вы переподписаны! \nОжидайте новостей =)")



# Sub unsubscribe
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if (not db.sub_exists(message.from_user.id)):    #check if user exists in DB
        db.add_sub(message.from_user.id, False)     #add if it aint and make sub field FALSE
        await message.answer("Вы и так не подписаны =/")
    else:
        db.update_subscription(message.from_user.id, False)  #if user exists in db - unsub
        await message.answer("Вы отписались")





# Long pool
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)