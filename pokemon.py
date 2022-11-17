import random


class Pokemon:
    def __init__(self, characteristics_dict=None):

        if characteristics_dict is None:
            characteristics_dict = {'name': 'abc', 'type1': 'fire', 'type2': 'fire', 'hp': '10000', 'pokedex_number': '-1',
                                    'attack': '1000', 'defense': '1000', 'speed': '1000', 'generation': '1'}

        self.characteristics_dict = characteristics_dict

        self.name = characteristics_dict['name']
        self.type1 = characteristics_dict['type1']
        self.type2 = characteristics_dict['type2']
        self.hp = float(characteristics_dict['hp'])
        self.curr_hp = float(characteristics_dict['hp'])
        self.attack = float(characteristics_dict['attack'])
        self.defense = float(characteristics_dict['defense'])
        self.speed = int(characteristics_dict['speed'])
        self.generation = characteristics_dict['generation']
        self.pokedex_number = characteristics_dict['pokedex_number']

        self.alive = True

        self.against_type = {'bug': 1.0, 'dark': 1.0, 'dragon': 1.0, 'electric': 0.5, 'fairy': 0.5, 'fighting': 0.5,
                             'fire': 2.0, 'flying': 2.0, 'ghost': 1.0, 'grass': 0.25, 'ground': 1.0, 'ice': 2.0,
                             'normal': 1.0, 'poison': 1.0, 'psychic': 2.0, 'rock': 1.0, 'steel': 1.0, 'water': 0.5}

        # self.against_type = {}
        #
        # for key in characteristics_dict:
        #     if key.startswith('against'):
        #         self.against_type.update([(key.replace('against_', ''), float(characteristics_dict[key]))])

        self.strings = []
        self.create_repr_strings()

    def create_repr_strings(self):
        self.strings = []
        substrings = []
        for type_ in self.against_type:
            if self.against_type[type_] != 1:
                substrings.append('{:<10}: {:<10}'.format(type_, self.against_type[type_]))

        if len(substrings) < 4:
            for i in range(4 - len(substrings)):
                substrings.append('   {:7} {:<10} '.format('', ' '))

        if self.type2 != '':
            self.strings.append(
                "'{}'{:<11} {:<22}".format(self.generation, self.name, '(' + self.type1 + " " + self.type2 + ')'))
        else:
            self.strings.append("'{}'{:<11} {:<22}".format(self.generation, self.name, '(' + self.type1 + ')'))
        self.strings.append(' 🎔 {:<11} '.format(self.curr_hp) + substrings[0])
        substrings.pop(0)
        self.strings.append(' 🗡 {:<11} '.format(self.attack) + substrings[0])
        substrings.pop(0)
        self.strings.append(' 🛡 {:<11} '.format(self.defense) + substrings[0])
        substrings.pop(0)
        self.strings.append(' 👟 {:<11} '.format(self.speed) + substrings[0])
        substrings.pop(0)
        for type_ in substrings:
            self.strings.append(' ' + ' ' * 14 + type_)

    def draw(self):
        for string_ in self.strings:
            print(string_)

    def attack_pokemon(self, pokemon):
        roll20 = random.randint(1, 21)

        if pokemon.type2 == '':
            attacked_pokemon_types = [pokemon.type1]
        else:
            attacked_pokemon_types = [pokemon.type1, pokemon.type2]

        type_coefficient = max([self.against_type[type_] for type_ in attacked_pokemon_types])

        atck_dfns_diff = self.attack - pokemon.defense

        atck_dfns_diff_coefficient = 1

        if atck_dfns_diff >= 0:
            atck_dfns_diff_coefficient += 0.05 * atck_dfns_diff
        else:
            atck_dfns_diff_coefficient *= 0.975 ** abs(atck_dfns_diff)

        damage = roll20 * type_coefficient * atck_dfns_diff_coefficient

        pokemon.curr_hp = round(pokemon.curr_hp - damage, 2)

        if pokemon.curr_hp < 0:
            pokemon.curr_hp = 0

        pokemon.strings = []
        pokemon.create_repr_strings()

        if pokemon.curr_hp == 0:
            pokemon.alive = False

        return [round(damage, 2), roll20, type_coefficient, round(atck_dfns_diff_coefficient, 2)]
