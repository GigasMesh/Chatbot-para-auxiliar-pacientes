from messages import BotMessages
import telebot
from classification import DecisionTree

botObject = BotMessages()
bot = telebot.TeleBot(token=botObject.token)


@bot.message_handler(content_types=['text'])
def message_received(message):
    # Questionary
    userId = message.from_user.id
    if userId not in botObject.usersSymptons:
        bot.send_message(chat_id=message.from_user.id, text=botObject.returnQuestion(userId, message))
        print("informações do usuário %s: " % message.from_user.username, botObject.usersInformations[userId])

    # Symptons
    else:
        result = botObject.returnMenu(userId, message)
        if result:
            print("Sintomas do usuário %s: " % message.from_user.username, botObject.usersSymptons[userId])
            bot.send_message(chat_id=message.from_user.id, text=result)
        else:
            decisionTree = DecisionTree('dataset_services/datasets/modifiedDataset.csv')
            symptons = botObject.usersSymptons[userId]
            disease = decisionTree.returnDisease(symptons)[0]
            print("Doença do usuário %s: " % message.from_user.username, disease)
            bot.send_message(chat_id=message.from_user.id, text="Não há mais sintomas para serem mostrados")
            bot.send_message(chat_id=message.from_user.id, text="Sua doença pode ser: %s" % disease)
            print("Sintomas do usuário %s: " % message.from_user.username, botObject.usersSymptons[userId])
            botObject.resetUserInformations(userId)


bot.polling(True)
