# -*- coding: utf-8 -*-

import telebot
from telebot import types
import logging


train_types = {
    "yoga": "Йога",
    "cardio": "Кардио",
    "strong": "Силовая",
    "func": "Функциональная"
}

train_times = {
    "20": "20 минут",
    "30": "30 минут",
    "40": "40 минут",
    "60": "60 минут"
}

def on_type_sel(train_type):
    return "Итак, вы выбрали " + train_type + ". Прекрасный выбор!"

def on_time_sel(train_time):
    return "Отлично! " + train_time + " - прекрасная продолжительность тренировки!"

bot = telebot.TeleBot("1423761929:AAF_ulQQcI5viydBS1SDxi3SeFhSO__83G8")

kbd_trains = types.InlineKeyboardMarkup(row_width=1)
for one_key in train_types.keys():
    kbd_trains.add(types.InlineKeyboardButton(text=train_types[one_key], callback_data=one_key))

kbd_times = types.InlineKeyboardMarkup(row_width=1)
for one_key in train_times.keys():
    kbd_times.add(types.InlineKeyboardButton(text=train_times[one_key], callback_data=one_key))


train_query = {}

@bot.message_handler(commands=['start'])
def greeting(message):
    logging.log('Будем выбирать тип тренировки')
    bot.send_message(message.chat.id, 'Тип тренировки:', reply_markup=kbd_trains)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    print(call)
    if call.data in train_types.keys():
        logging.log('Тип тренировки выбран: ' + call.data)
        bot.edit_message_text(
            chat_id=call.message.chat.id, 
            message_id=call.message.message_id, 
            text=on_type_sel(train_types[call.data])
        )
        bot.send_message(call.from_user.id, 'Теперь давайте выберем продолжительность тренировки.')
        bot.send_message(call.from_user.id, 'Вот что я могу вам предложить:', reply_markup=kbd_times)
        train_query["type"] = train_types[call.data]
    elif call.data in train_times.keys():
        bot.edit_message_text(
            chat_id=call.message.chat.id, 
            message_id=call.message.message_id, 
            text=on_time_sel(train_times[call.data])
        )
        logging.log('Продолжительность тренировки выбрана: ' + call.data)
        train_query["time"] = train_times[call.data]
        bot.send_message(call.from_user.id, 'А на этом пока всё! Пока!')
        

if __name__ == '__main__':
    logging.log('Если вы это видите, значит, работа начата!')
    bot.infinity_polling()
