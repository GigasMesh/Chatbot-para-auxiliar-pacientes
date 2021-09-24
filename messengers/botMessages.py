from dataset_services import PandasDataset


class BotMessages:
    def __init__(self):
        self.token = open('messengers/tokenTelegram.txt').read()
        self.pandasDataset = PandasDataset('dataset_services/datasets/modifiedDataset.csv')
        self.rank = self.pandasDataset.getRanking()
        self.usersInformations = {}
        self.usersSymptons = {}
        self.questionary = ["Olá, meu nome é MedBot! Estarei aqui para auxiliá-lo. Primeiramente, qual o seu "
                            "nome completo?",
                            "Qual a sua data de nascimento? (DD/MM/AAAA)",
                            "Qual o seu sexo?",
                            "Qual o CEP do lugar onde você mora?"]

    def generateMenu(self, index, rank=None):
        if not rank:
            rank = self.rank
        if index > len(rank) - 5:
            return None
        print("tamanho do rank: ", len(rank))
        menu = "Digite o número do primeiro sintoma que você está sentindo:\n"
        for numero in range(index, index+5):
            menu = menu + "%d - %s\n" % (numero - index, rank[numero])
        menu = menu + "5 - Nenhum dos sintomas acima\n"
        menu = menu + "6 - Não tenho mais sintomas para listar"
        return menu

    def returnQuestion(self, userId, message):
        if userId not in self.usersInformations:
            self.usersInformations[userId] = [0]
            return self.questionary[0]
        elif self.usersInformations[userId][0] != "Done":
            self.usersInformations[userId].append(message.text)
            self.usersInformations[userId][0] += 1
            if self.usersInformations[userId][0] == 4:
                self.usersInformations[userId][0] = "Done"
                self.usersSymptons[userId] = [0]
                return self.generateMenu(0)
            return self.questionary[self.usersInformations[userId][0]]

    def returnMenu(self, userId, message):
        numberOfSymptoms = len(self.usersSymptons[userId]) - 1
        if int(message.text) == 6:
            # enviar lista para função interna
            return None
        if int(message.text) == 5:
            self.usersSymptons[userId][0] += 5
            if numberOfSymptoms == 0:
                return self.generateMenu(self.usersSymptons[userId][0])
            symptom = self.usersSymptons[userId][-1]
            symptoms = self.usersSymptons[userId][1:]
            rank = self.pandasDataset.getCorrelatedSymptoms(symptom, symptoms)
            return self.generateMenu(self.usersSymptons[userId][0], rank)
        symptoms = self.usersSymptons[userId][1:]
        if numberOfSymptoms == 0:
            symptom = self.rank[self.usersSymptons[userId][0] + int(message.text)]
        else:
            pastRank = self.pandasDataset.getCorrelatedSymptoms(self.usersSymptons[userId][-1], symptoms)
            symptom = pastRank[self.usersSymptons[userId][0] + int(message.text)]
        self.usersSymptons[userId].append(symptom)
        self.usersSymptons[userId][0] = 0
        rank = self.pandasDataset.getCorrelatedSymptoms(symptom, symptoms)
        return self.generateMenu(self.usersSymptons[userId][0], rank)

    def resetUserInformations(self, userId):
        self.usersInformations.pop(userId, None)
        self.usersSymptons.pop(userId, None)
