import requests
import telebot
from random import *
import json
phone_book = {}
API_TOKEN = '6593082527:AAEWJfTQ9hGEPu7kLOkLwSLinppqVxYO1P4'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Heey,это справочник контактов, здесь можно управлять своими контактами")


@bot.message_handler(commands=['add'])
def add_message(message):
    bot.send_message(message.chat.id, "Введите имя контакта: ")
    bot.register_next_step_handler(message, add_contact)

def add_contact(message):
    name = message.text
    contact = {}
    bot.send_message(message.chat.id, "Введите номер: ")
    bot.register_next_step_handler(message, add_number, name, contact)

def add_number(message, name, contact):
    num = message.text
    contact["номер"] = [num]
    bot.send_message(message.chat.id, "Введите второй номер (если есть): ")
    bot.register_next_step_handler(message, add_second_number, name, contact)

def add_second_number(message, name, contact):
    num2 = message.text
    if num2:
        contact["номер"].append(num2)
    bot.send_message(message.chat.id, "Введите ДР (если есть): ")
    bot.register_next_step_handler(message, add_birthday, name, contact)

def add_birthday(message, name, contact):
    b_day = message.text
    if b_day:
        contact["ДР"] = b_day
    bot.send_message(message.chat.id, "Введите email (если есть): ")
    bot.register_next_step_handler(message, add_email, name, contact)

def add_email(message, name, contact):
    mail = message.text
    if mail:
        contact["email"] = mail
    phone_book[name] = contact
    bot.send_message(message.chat.id, "Контакт добавлен")


@bot.message_handler(commands=['all'])
def show_all(message):
    try:
        bot.send_message(message.chat.id,"Вот список контактов:")
        if len(phone_book) > 0:
            response = "Список контактов:\n"
            for name, contact in phone_book.items():
                response += f"Имя: {name}\n"
                if "номер" in contact:
                    response += f"Номера телефонов: {', '.join(contact['номер'])}\n"
                if "ДР" in contact:
                    response += f"День рождения: {contact['ДР']}\n"
                if "email" in contact:
                    response += f"Email: {contact['email']}\n"
                response += "\n"
        bot.send_message(message.chat.id, response)
    except:
        bot.send_message(message.chat.id,"Телефонный справочник пустой ")

@bot.message_handler(commands=['save'])
def save_all(message):
    with open("contacts.json", "w", encoding="utf-8") as fh:
        fh.write(json.dumps(phone_book, ensure_ascii=False))
    bot.send_message(message.chat.id,"Телефонный справочник был успешно сохранен в файл")
   

bot.polling(none_stop=True)

