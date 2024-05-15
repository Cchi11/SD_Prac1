import random


class InsultingService:

    def __init__(self):
        self.insults_set = set()

    def add_insult(self, insult):
        print('Insult received: ' + insult)
        self.insults_set.add(insult)
        return 'Done'

    def get_insults(self):
        return list(self.insults_set)

    def insult_me(self):
        chosen_insult = list(self.insults_set)[random.randrange(0, len(self.insults_set))]
        print('Insult requested. Chose ' + chosen_insult)
        return chosen_insult

    def get_top_insults(self, n):
        hashmap = {}
        print("Hello World")
        lista = list(self.insults_set)
        for insult in lista:
            count = lista.count(insult)
            hashmap[insult] = count

        print(hashmap)
        lista2 = list()
        return lista2
        # Now, sort the dictionary with the most used insult in front and the least used on the tail


insulting_service = InsultingService()