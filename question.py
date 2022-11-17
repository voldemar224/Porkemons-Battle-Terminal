import copy
import csv
import random

from pokemon import Pokemon


class Question:
    def __init__(self, game):
        self.game = game

    def do_you_know_how_to_play(self):
        question = input('Do You know how to play this game? y/n: ').lower()

        if question == 'y':
            return

        elif question == 'n':
            self.game.tell_rules()
            return

        else:
            print('Invalid syntax, try again!')
            self.do_you_know_how_to_play()

    def do_you_have_character(self):
        question = input('Do You have a character with pokemons already? y/n: ').lower()

        if question == 'y':
            self.game.look_for_characters()
            return
        elif question == 'n':
            self.game.create_hero_character()
            return
        else:
            print('Invalid syntax, try again!')
            self.do_you_know_how_to_play()

    def are_you_ready_to_fight(self):
        question = input(f'Nice to meet You, {self.game.hero_character.name}. '
                         'I have found an enemy for You already. '
                         'Are You ready to participate in your first battle? y/n: ').lower()
        if question == 'y':
            print('Ok, let the battle begin!')
            return
        else:
            while not self.game.question_answered:
                question = input("And why did You come here, when You don't want to fight? "
                                 "Maybe You'll think one more time better?) y/n: ").lower()
                if question == 'y':
                    print('Ok, let the battle begin!')
                    return

    def do_you_want_to_create_hero(self):
        question = input('Would You like to create a new character and try Yourself on the battlefield again? '
                         'y/n: ')
        if question == 'y':
            print('Ok, You will be returned on the start of the game.\n')
            self.game.user_lost = True
            return
        elif question == 'n':
            self.game.user_in_console = False
            return
        else:
            print('Invalid syntax, try again!')
            self.do_you_want_to_create_hero()

    def do_you_want_to_find_new_enemy(self):
        question = input('Would You like to find a new enemy? y/n: ')
        if question == 'y':
            self.game.game_over = False
            return
        elif question == 'n':
            print('Ok, I saved Your character and already waiting for Your next glorious battle!')
            self.game.save_character()
            self.game.user_in_console = False
            return
        else:
            print('Invalid syntax, try again!')
            self.do_you_want_to_find_new_enemy()

    def choose_pokemon_to_attack(self):
        chosen_pokemon_index = int(input('Choose a pokemon, '
                                         'with which You want to attack Your enemy! 1/2/3...')) - 1
        if 0 <= chosen_pokemon_index < len(self.game.hero_character.pokemon_list):
            return self.game.hero_character.pokemon_list[chosen_pokemon_index]
        else:
            print('Invalid syntax, try again!')
            self.choose_pokemon_to_attack()

    def choose_pokemon_be_attacked(self):
        chosen_pokemon_index = int(input('Choose a pokemon, which You want to attack! 1/2/3...\n')) - 1
        if 0 <= chosen_pokemon_index < len(self.game.hero_character.pokemon_list):
            return self.game.enemy_character.pokemon_list[chosen_pokemon_index]
        else:
            print('Invalid syntax, try again!')
            self.choose_pokemon_be_attacked()

    def readiness_before_enemys_attack(self):
        question = input('Enemy is attacking You. If You are ready press y! '
                         'If You want to give up, press n (Your character will be lost)! y/n: ')
        if question == 'y':
            return
        elif question == 'n':
            print('Ok, You will be returned on the start of the game.\n')
            self.game.user_lost = True
            self.game.game_over = True
            return
        else:
            print('Invalid syntax, try again!')
            self.readiness_before_enemys_attack()

    def do_you_like_pokemons(self):
        with open('pokemon.csv', 'r') as pokemons_data:
            csv_file = csv.DictReader(pokemons_data)
            pokemons = [x for x in csv_file]
            self.game.hero_character.pokemon_list = []
            for i in range(2):
                self.game.hero_character.pokemon_list.append(Pokemon(random.choice(pokemons)))
                # self.game.hero_character.pokemon_list.append(Pokemon())

            self.game.hero_character.pokemon_list[0].draw()
            print()
            self.game.hero_character.pokemon_list[1].draw()

        while not self.game.question_answered:
            question = input('Do You like pokemons, which I found for You? y/n: ').lower()
            if question == 'y':
                return
            elif question == 'n':
                print('Ok, I will look for two other pokemons for You')
                self.game.hero_character.pokemon_list = []
                for i in range(2):
                    self.game.hero_character.pokemon_list.append(Pokemon(random.choice(pokemons)))

                self.game.hero_character.pokemon_list[0].draw()
                print()
                self.game.hero_character.pokemon_list[1].draw()
            else:
                print('Invalid syntax. Try again!')

    def choose_character(self, saves):
        character_name = input("Which of Your characters You would like to choose? Type name!")
        if saves.count(character_name) != 0:
            return character_name
        else:
            print('Invalid syntax, please try again!')
            self.choose_character(saves)




