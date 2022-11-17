import csv


class Character:
    def __init__(self, win=0, name='name', pokemon_list=None, enemies_list=None):
        self.win = win
        self.name = name
        if pokemon_list is None:
            self.pokemon_list = []
        self.pokemon_list = pokemon_list
        if enemies_list is None:
            enemies_list = []
        self.enemies_list = enemies_list

    def pokemon_attacking_pokemon(self, attacking_pokemon, attacked_pokemon, character):
        print(f'\n{attacking_pokemon.name} is attacking {attacked_pokemon.name}\n')

        data_list = attacking_pokemon.attack_pokemon(attacked_pokemon)
        # data_list = [damage, roll20, type_coefficient, atck_dfns_diff_coefficient]

        print(f'damage = roll20 * (against type coefficient) * (attack defense coefficient)')
        print(f'damage = {data_list[1]} * {data_list[2]} * {data_list[3]}\n')

        print(f'{attacking_pokemon.name} attacked {attacked_pokemon.name} and dealt {data_list[0]} damage to him ')

        if attacked_pokemon.curr_hp == 0:
            print(f'\nPokemon {attacked_pokemon.name} died.\n')
            if [poke.name for poke in character.pokemon_list if poke.alive] == []:
                self.win = 1
                return True
            else:
                return False
        elif attacked_pokemon.speed >= attacking_pokemon.speed:
            data_list = attacked_pokemon.attack_pokemon(attacking_pokemon)
            # data_list = [damage, roll20, type_coefficient, atck_dfns_diff_coefficient]

            print(f'{attacked_pokemon.name} is attacking {attacking_pokemon.name}\n')

            print(f'damage = roll20 * (against type coefficient) * (attack defense coefficient)')
            print(f'damage = {data_list[1]} * {data_list[2]} * {data_list[3]}\n')

            print(
                f'{attacking_pokemon.name} attacked {attacked_pokemon.name} and dealt {data_list[0]} damage to him \n')

            if attacking_pokemon.curr_hp == 0:
                print(f'\nPokemon {attacking_pokemon.name} died.\n')
                if [poke for poke in self.pokemon_list if poke.alive] == []:
                    character.win = 1
                    return True
                else:
                    return False
        else:
            print(f"{attacking_pokemon.name} tried to dodge {attacked_pokemon.name}'s responding attack, "
                  f"and succeeded.\n")

    def character_first_save(self):
        data_string = self.name + str([int(poke.pokedex_number) for poke in self.pokemon_list])

        with open('saves.txt', 'r') as file:
            saves = file.read()

        if saves.find(self.name) == -1:
            saves = saves.replace('.', '')
            with open('saves.txt', 'w') as file:
                file.write(saves)

            with open('saves.txt', 'a+') as file:
                file.write(f"\n{data_string}.")
        else:
            self.do_you_want_to_rewrite_pokemons_of_character(data_string, saves)

    def do_you_want_to_rewrite_pokemons_of_character(self, data_string, saves):
        question_answered = False
        while not question_answered:
            question = input("There is already a character with such name. "
                             "Do You want to rewrite pokes of this character? y/n: ").lower()
            if question == 'y':
                start_index = saves.index(self.name)
                end_index = saves.index(']', start_index)

                saves = saves.replace(saves[start_index:end_index + 1], '')

                with open('saves.txt', 'w') as file:
                    file.write(saves)

                question_answered = True
            elif question == 'n':
                name_question = input('\nPlease, enter Your name: ')
                self.name = name_question
                if saves.find(self.name) != -1:
                    self.do_you_want_to_rewrite_pokemons_of_character(data_string, saves)
                else:
                    saves = saves.replace('.', '')
                    with open('saves.txt', 'w') as file:
                        file.write(saves)

                    data_string = self.name + str([int(poke.pokedex_number) for poke in self.pokemon_list])
                    with open('saves.txt', 'a+') as file:
                        file.write(f"\n{data_string}")
                question_answered = True
            else:
                print('Invalid syntax. Please try again!')

        question_answered = False

    def character_save(self):
        with open('saves.txt', 'r') as file:
            saves = file.read()

        data_string = str([int(poke.pokedex_number) for poke in self.pokemon_list])
        print(data_string)
        start_index = saves.index(self.name) + len(self.name)
        end_index = saves.index(']', start_index)

        saves = saves.replace(saves[start_index:end_index + 1], data_string)

        with open('saves.txt', 'w') as file:
            file.write(saves)
