import telebot
from datetime import datetime
import config


bot = telebot.TeleBot(config.TOKEN)

# ID администратора (замените на свой)

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Тут вы можете предложить свой материал 😉 и он обязательно будет рассмотрен и опубликован (но это не точно).")

# Обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    user_message = message.text
    user_name = message.from_user.first_name  # Имя пользователя
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Текущая дата и время

    # Отправляем текстовое сообщение администратору
    send_to_admin(user_message, user_name, timestamp, message.chat.id)
    bot.send_message(message.chat.id, "Спасибо за ваше предложение! Мы его рассмотрим.")

# Обработка фотографий
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_name = message.from_user.first_name  # Имя пользователя
    user_id = message.from_user.id  # ID пользователя
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Текущая дата и время
    photo_id = message.photo[-1].file_id  # Получаем ID самой большой фотографии

    # Получаем подпись от пользователя, если она есть
    user_caption = message.caption if message.caption else "Без подписи"

    # Формируем подпись для фотографии
    caption = f"Фото от {user_name} (ID: {user_id})\nВремя отправки: {timestamp}\nТекст: {user_caption}"

    # Отправляем фотографию администратору с подписью
    bot.send_photo(config.ADMIN_ID, photo_id, caption=caption)
    
    bot.send_message(message.chat.id, "Спасибо за вашу фотографию! Мы её рассмотрим.")

# Обработка видео
@bot.message_handler(content_types=['video'])
def handle_video(message):
    user_name = message.from_user.first_name  # Имя пользователя
    user_id = message.from_user.id  # ID пользователя
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Текущая дата и время
    video_id = message.video.file_id  # Получаем ID видео

    # Получаем подпись от пользователя, если она есть
    user_caption = message.caption if message.caption else "Без подписи"

    # Формируем подпись для видео
    caption = f"Видео от {user_name} (ID: {user_id})\nВремя отправки: {timestamp}\nТекст: {user_caption}"

    # Отправляем видео администратору с подписью
    bot.send_video(config.ADMIN_ID, video_id, caption=caption)
    
    bot.send_message(message.chat.id, "Спасибо за ваше видео! Мы его рассмотрим.")

def send_to_admin(user_message, user_name, timestamp, chat_id):
    # Формируем сообщение для администратора
    admin_message = f"Новое текстовое сообщение от {user_name} (ID чата: {chat_id}):\n{user_message}\n\nВремя отправки: {timestamp}"
    
    # Отправляем администратору сообщение
    bot.send_message(config.ADMIN_ID, admin_message)

# Запуск бота
bot.polling(none_stop=True)
