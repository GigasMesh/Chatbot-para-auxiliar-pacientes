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
        menu = "Digite o número do primeiro sintoma que você está sentindo:\n"
        for numero in range(index, index+5):
            menu = menu + "%d - %s\n" % (numero - index, rank[numero])
        menu = menu + "5 - Nenhum dos sintomas acima"
        return menu
