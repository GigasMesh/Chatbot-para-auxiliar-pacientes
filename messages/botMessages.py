from messages.inputValidation import inputTypeVerification
from dataset_services import PandasDataset
from dataset_services import DatasetObject


class BotMessages:
    def __init__(self):
        self.token = open('messages/tokenTelegram.txt').read()
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
        number = 5
        if rank is None:
            rank = self.rank
        if index == len(rank) or index > len(rank):
            return None
        if index > len(rank) - 5:
            number = len(rank) - index
        print("tamanho do rank: ", len(rank))
        menu = "Digite o número de um sintoma que você está sentindo:\n"
        for numero in range(index, index+number):
            menu = menu + "%d - %s\n" % (numero - index, rank[numero])
        menu = menu + "Prox - Próxima página\n"
        menu = menu + "Voltar - Página anterior\n"
        menu = menu + "Sair - Não tenho mais sintomas para listar"
        return menu

    def returnQuestion(self, userId, message):
        if userId not in self.usersInformations:
            self.usersInformations[userId] = [0]
            return self.questionary[0]
        elif self.usersInformations[userId][0] != "Done":
            if inputTypeVerification(message.text, self.usersInformations[userId][0]):
                self.usersInformations[userId].append(message.text)
                self.usersInformations[userId][0] += 1
            if self.usersInformations[userId][0] == 4:
                self.usersInformations[userId][0] = "Done"
                self.usersSymptons[userId] = [0]
                return self.generateMenu(0)
            return self.questionary[self.usersInformations[userId][0]]

    def returnMenu(self, userId, message):
        numberOfSymptoms = len(self.usersSymptons[userId]) - 1
        if not inputTypeVerification(message.text, 'symptoms'):
            if self.usersSymptons[userId][0] < 5:
                if numberOfSymptoms == 0:
                    return self.generateMenu(0)
                else:
                    symptom = self.usersSymptons[userId][-1]
                    symptoms = self.usersSymptons[userId][1:]
                    rank = self.pandasDataset.getCorrelatedSymptoms(symptom, symptoms)
                    return self.generateMenu(self.usersSymptons[userId][0], rank)
            else:
                if numberOfSymptoms == 0:
                    return self.generateMenu(self.usersSymptons[userId][0])
                symptom = self.usersSymptons[userId][-1]
                symptoms = self.usersSymptons[userId][1:]
                rank = self.pandasDataset.getCorrelatedSymptoms(symptom, symptoms)
                return self.generateMenu(self.usersSymptons[userId][0], rank)
        if message.text.lower() == "sair":
            # enviar lista para função interna
            return None
        if message.text.lower() == "voltar":
            if self.usersSymptons[userId][0] < 5:
                if numberOfSymptoms == 0:
                    return self.generateMenu(0)
                else:
                    symptom = self.usersSymptons[userId][-1]
                    symptoms = self.usersSymptons[userId][1:]
                    rank = self.pandasDataset.getCorrelatedSymptoms(symptom, symptoms)
                    return self.generateMenu(self.usersSymptons[userId][0], rank)
            else:
                self.usersSymptons[userId][0] -= 5
                if numberOfSymptoms == 0:
                    return self.generateMenu(self.usersSymptons[userId][0])
                symptom = self.usersSymptons[userId][-1]
                symptoms = self.usersSymptons[userId][1:]
                rank = self.pandasDataset.getCorrelatedSymptoms(symptom, symptoms)
                return self.generateMenu(self.usersSymptons[userId][0], rank)
        if message.text.lower() == "prox":
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

    def saveInformations(self, userId, symptoms, disease):
        datasetObject = DatasetObject("dataset_services/datasets")
        info = self.usersInformations[userId]
        data = {"ID": userId, "Name": info[1], "Birthdate": info[2], "Gender": info[3], "CEP": info[4],
                "Disease": disease}
        datasetObject.insere_dados("usersInformations", "Personal", data, "ID")
        for symptom in symptoms:
            size = datasetObject.retornar_numero_de_linhas("UsersSymptoms", "Relation")
            datasetObject.insere_dados("UsersSymptoms", "Relation", {"ID": size, "User ID": userId, "symptom": symptom},
                                       "ID")
