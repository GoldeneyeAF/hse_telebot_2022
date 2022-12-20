import telebot
from telebot import types

TOKEN = 
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['new_chat_members'])
def greeting(message):
    bot.reply_to(message, text='Welcome to the jungle!')

@bot.message_handler(commands=['start'])
def hello_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item_1 = types.KeyboardButton("Помощь в использовании")
    item_3 = types.KeyboardButton("Статистика по чату")
    item_4 = types.KeyboardButton("Бот - выйди из чата")
    markup.add(item_1, item_3, item_4)
    bot.send_message(message.chat.id, "Чтобы выдать бан за некультурное поведение - пропиши /ban в ответ на некультурное сообщение, /promote - аналогично, но чтобы дать кому то админку. Все остальное делается кнопками.", reply_markup=markup)

@bot.message_handler(commands=['help'])
def helper(message):
    bot.reply_to(message, "Чтобы выдать бан за некультурное поведение - пропиши /ban в ответ на некультурное сообщение, /promote - аналогично, но чтобы дать кому то админку. Все остальное делается кнопками.")

@bot.message_handler(commands=["promote"])
def promote_user_handler(message):
    if message.reply_to_message is None:
        return bot.reply_to(message, "Написано же, нужно ответить на сообщение")
    member = bot.get_chat_member(message.chat.id, message.from_user.id)
    member1 = bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    if not member.can_promote_members and member.status != 'creator':
        return bot.reply_to(message, "Ты не можешь повышать людей")
    if member1.status == 'creator' or member1.status == 'administrator':
        return bot.reply_to(message, "Этот человек уже админ")
    try:
        bot.promote_chat_member(message.chat.id, message.reply_to_message.from_user.id, True, True, True)
    except:
        bot.reply_to(message, "У бота нету прав на выдачу админок!")

@bot.message_handler(commands=["ban"])
def kick_user_handler(message):
    if message.reply_to_message is None:
        return bot.reply_to(message, "Написано же, нужно ответить на сообщение")
    member = bot.get_chat_member(message.chat.id, message.from_user.id)
    member1 = bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    if not member.can_restrict_members and member.status != 'creator':
        return bot.reply_to(message, "У тебя нет права на бан")
    if member1.status == 'creator' or member1.status == 'administrator':
        return bot.reply_to(message, "Нельзя банить другого админа!")
    try:
        bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    except:
        bot.reply_to(message, "У бота нету прав на баны!")

@bot.message_handler(content_types=['text', 'emoji'])
def message_reply(message):
    if message.text == "Бот - выйди из чата":
        member = bot.get_chat_member(message.chat.id, message.from_user.id)
        if not member.can_restrict_members and member.status != 'creator':
            bot.reply_to(message, "Ты не можешь выгнать бота!")
        else:
            bot.leave_chat(message.chat.id)
    elif message.text == "Помощь в использовании":
        bot.reply_to(message, "Чтобы выдать бан за некультурное поведение - пропиши /ban в ответ на некультурное сообщение, повысить - аналогично, но /promote. Все остальное делается кнопками.")
    elif message.text == "Статистика по чату":
        user_cnt = bot.get_chat_member_count(message.chat.id)
        temp_admins = bot.get_chat_administrators(message.chat.id)
        temp_admins1 = []
        for i in temp_admins:
            temp_admins1.append(i.user.username)
        admins = '\n'.join(temp_admins1)
        bot.send_message(message.chat.id, 'Всего пользователей: ' + str(user_cnt) + '\n' + 'Список админов:\n' + str(admins))

bot.polling(none_stop=True, interval=0)
