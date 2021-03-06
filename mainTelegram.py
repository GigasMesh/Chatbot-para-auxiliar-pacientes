from messages import BotMessages
import telebot
from classification import DecisionTree
from services import GetNearHospital

botObject = BotMessages()
bot = telebot.TeleBot(token=botObject.token)


@bot.message_handler(content_types=['text'])
def message_received(message):
    # Questionary
    userId = message.from_user.id
    if userId not in botObject.usersSymptons:
        bot.send_message(chat_id=message.from_user.id, text=botObject.returnQuestion(userId, message))
        print("informações do usuário %s: " % message.from_user.first_name, botObject.usersInformations[userId])

    # Symptons
    else:
        result = botObject.returnMenu(userId, message)
        if result:
            print("Sintomas do usuário %s: " % message.from_user.first_name, botObject.usersSymptons[userId])
            bot.send_message(chat_id=message.from_user.id, text=result)
        else:
            decisionTree = DecisionTree('dataset_services/datasets/modifiedDataset.csv')
            symptons = botObject.usersSymptons[userId]
            disease = decisionTree.returnDisease(symptons)[0]
            print("Doença do usuário %s: " % message.from_user.first_name, disease)
            print("Sintomas do usuário %s: " % message.from_user.first_name, symptons)
            bot.send_message(chat_id=message.from_user.id, text="Não há mais sintomas para serem mostrados")
            hospital = GetNearHospital(botObject.usersInformations[userId][4])
            if hospital:
                bot.send_message(chat_id=message.from_user.id, text="Hospital mais próximo: %s" % hospital.name)
            else:
                bot.send_message(chat_id=message.from_user.id, text="Não encontramos seu endereço")
            # bot.send_message(chat_id=message.from_user.id, text="Sua doença pode ser: %s" % disease)
            botObject.saveInformations(userId, symptons, disease)
            botObject.resetUserInformations(userId)


bot.polling(True)
