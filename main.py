from aiogram import Bot, Dispatcher, executor, types

import emoji, datetime, os
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    ContentType, \
    InlineKeyboardMarkup, InlineKeyboardButton

import lit_model, style_model

TOKEN = '5853559476:AAFBmDxa9Qe_dj0CTGqPh5YJc1CTVv32ZcQ'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

global function
function = None

@dp.message_handler(commands=['start', 'restart'])
async def start_message(message: types.Message):

    global function
    function = None

    stylistics_button = KeyboardButton("Matnning nutq uslubini aniqlash")
    writers_button = InlineKeyboardButton("Matnning yozuvchilar uslubiga mosligini aniqlash")

    await bot.send_message(
        message.from_user.id,
        "Marhamat, funksiyani tanlang:",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(stylistics_button, writers_button)
    )


@dp.message_handler()
async def bot_message(message: types.Message):
    global function
    if function is None:

        if message.text == "Matnning nutq uslubini aniqlash":
            function = "stylistics"
            await bot.send_message(
                message.from_user.id,
                "*Matnning nutq uslubini aniqlash* funksiyasi tanlandi",
                parse_mode="Markdown",
                reply_markup=types.ReplyKeyboardRemove()
            )
            await bot.send_message(
                message.from_user.id,
                "Marhamat, matnni kiriting:",
                parse_mode="Markdown",
                reply_markup=types.ReplyKeyboardRemove()
            )

        elif message.text == "Matnning yozuvchilar uslubiga mosligini aniqlash":
            function = "writers"
            await bot.send_message(
                message.from_user.id,
                "*Matnning yozuvchilar uslubiga mosligini aniqlash* funksiyasi tanlandi",
                parse_mode="Markdown",
                reply_markup=types.ReplyKeyboardRemove()
            )
            await bot.send_message(
                message.from_user.id,
                "Marhamat, matnni kiriting:",
                parse_mode="Markdown",
                reply_markup=types.ReplyKeyboardRemove()
            )

    else:
        file_name = f"{datetime.datetime.now().strftime('%d%m%Y')}{datetime.datetime.now().strftime('%H%M%S')}.txt"
        new_file = open(file_name, 'w', encoding="utf-8")
        new_file.write(message.text)
        new_file.close()

        if function == 'writers':
            try:
                prediction = lit_model.pred(file_name)
                index_list = prediction[0]
                percent_list = prediction[1]

                writers_list = ["Tohir Malik", "Alisher Navoiy", "O‘tkir Xoshimov", "Abdulla Qodiriy", "G‘ofur G‘ulom"]

                result = ""

                for i in range(len(index_list)):
                    result += writers_list[index_list[i]] + ": " + str(int(percent_list[i])) + '%\n'

                # for i in range(5):
                #     if i in index_list:
                #         result += f"{writers_list[i]}: {int(percent_list[index_list.index(i)])}%\n"
                #     else:
                #         result += f"{writers_list[i]}: 0%\n"

                await bot.send_message(message.from_user.id, result)
            except Exception as err:
                print(err)
                await bot.send_message(message.from_user.id, "Moslik aniqlanmadi...")
                await bot.send_message(message.from_user.id, "Marhamat, matnni tering:")

            os.remove(file_name)

        else:
            try:
                prediction = style_model.pred(file_name)
                index_list = prediction[0]
                percent_list = prediction[1]

                styles_list = ["Badiiy", "Rasmiy", "Publitsistik", "Ilmiy"]

                result = ""

                for i in range(len(index_list)):
                    result += styles_list[index_list[i]] + ": " + str(int(percent_list[i])) + '%\n'

                # for i in range(5):
                #     if i in index_list:
                #         result += f"{writers_list[i]}: {int(percent_list[index_list.index(i)])}%\n"
                #     else:
                #         result += f"{writers_list[i]}: 0%\n"

                await bot.send_message(message.from_user.id, result)
            except Exception as err:
                print(err)
                await bot.send_message(message.from_user.id, "Moslik aniqlanmadi...")
                await bot.send_message(message.from_user.id, "Marhamat, matnni tering:")

            os.remove(file_name)




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)