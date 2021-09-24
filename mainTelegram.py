from messengers import BotMessages
import telebot

botObject = BotMessages()
bot = telebot.TeleBot(token=botObject.token)


@bot.message_handler(content_types=['text'])
def message_received(message):
    # Questionary
    userId = message.from_user.id
    if userId not in botObject.usersSymptons:
        bot.send_message(chat_id=message.from_user.id, text=botObject.returnQuestion(userId, message))
        print(botObject.usersInformations)

    # Symptons
    else:
        result = botObject.returnMenu(userId, message)
        if result:
            bot.send_message(chat_id=message.from_user.id, text=result)
        else:
            bot.send_message(chat_id=message.from_user.id, text="Não há mais sintomas para serem mostrados")
            botObject.resetUserInformations(userId)
    # print(botObject.usersInformations)
    print(botObject.usersSymptons)


bot.polling(True)
