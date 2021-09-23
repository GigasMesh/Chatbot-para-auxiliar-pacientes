from messengers import BotMessages
import telebot

botObject = BotMessages()
bot = telebot.TeleBot(token=botObject.token)


@bot.message_handler(content_types=['text'])
def message_received(message):
    # Questionary
    userId = message.from_user.id
    if userId not in botObject.usersInformations:
        botObject.usersInformations[userId] = []
        bot.send_message(chat_id=message.from_user.id, text=botObject.questionary[0])
        return None
    userInformations = botObject.usersInformations[userId]
    if len(userInformations) < len(botObject.questionary) - 1:
        userInformations.append(message.text)
        bot.send_message(chat_id=message.from_user.id, text=botObject.questionary[len(userInformations)])
        return None
    elif len(userInformations) < 4:
        userInformations.append(message.text)

    # Symptons
    userSymptons = botObject.usersSymptons
    if userId not in userSymptons:
        userSymptons[userId] = [0]
        bot.send_message(chat_id=message.from_user.id, text=botObject.generateMenu(userSymptons[userId][0]))
    else:
        if int(message.text) == 5:
            userSymptons[userId][0] = userSymptons[userId][0] + 5
            if len(userSymptons[userId]) == 1:
                bot.send_message(chat_id=message.from_user.id, text=botObject.generateMenu(userSymptons[userId][0]))
                return 0
            symptom = userSymptons[userId][-1]
            list = userSymptons[userId][1:]
            bot.send_message(chat_id=message.from_user.id,
                             text=botObject.generateMenu(userSymptons[userId][0],
                                                         rank=botObject.pandasDataset.getCorrelatedSymptoms(symptom, list)))
        else:
            list = userSymptons[userId][1:]
            if len(userSymptons[userId]) == 1:
                symptom = botObject.rank[userSymptons[userId][0] + int(message.text)]
            else:
                rank = botObject.pandasDataset.getCorrelatedSymptoms(userSymptons[userId][-1], list)
                symptom = rank[userSymptons[userId][0] + int(message.text)]
            userSymptons[userId].append(symptom)
            userSymptons[userId][0] = 0
            bot.send_message(chat_id=message.from_user.id,
                             text=botObject.generateMenu(userSymptons[userId][0],
                                                         rank=botObject.pandasDataset.getCorrelatedSymptoms(symptom, list)))

    # print(botObject.usersInformations)
    print(botObject.usersSymptons)


bot.polling(True)
