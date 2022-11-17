import ast

import const
import time
import random
import csv
import copy

from enemy_character import EnemyCharacter
from hero_character import HeroCharacter
from pokemon import Pokemon
from question import Question


class Game:
    def __init__(self, hero_character=HeroCharacter(), enemy_character=EnemyCharacter(), turn=None, game_over=False,
                 question_answered=const.question_answered, user_lost=const.user_lost,
                 user_in_console=const.user_in_console):
        self.hero_character = hero_character
        self.enemy_character = enemy_character
        self.turn = turn
        self.game_over = game_over
        self.question_answered = question_answered
        self.user_lost = user_lost
        self.user_in_console = user_in_console

        self.questions = Question(self)

    # telling rules and creating or looking for the hero_character
    def start_phase(self):
        self.questions.do_you_know_how_to_play()

        self.questions.do_you_have_character()

        self.questions.are_you_ready_to_fight()

    def create_enemy_character(self):
        self.enemy_character.pokemon_list = []
        self.enemy_character.name = random.choice(const.names)

        generations_list = []

        for pokemon in self.hero_character.pokemon_list:
            generations_list.append(pokemon.generation)

        generation_set = set(generations_list)

        with open('pokemon.csv', 'r') as file:
            csv_file = csv.DictReader(file)
            pokemon_data = []

            for row in csv_file:
                pokemon_data.append(row)

            for generation in generation_set:
                pokemons_of_n_generation = [x for x in pokemon_data if x['generation'] == str(generation)]
                for i in range(generations_list.count(generation)):
                    self.enemy_character.pokemon_list.append(Pokemon(random.choice(pokemons_of_n_generation)))

    def countdown(self):
        print(3)
        time.sleep(1)
        print(2)
        time.sleep(1)
        print(1)
        time.sleep(1)

    def game(self):
        self.draw_hero_n_enemy()

        self.toss_coin()

        while not self.game_over:
            self.make_move()

        print('It was a nice battle!')

        if self.hero_character.win:
            print('Victory\n')
            self.hero_character.win = 0
            self.collecting_pokemons()

            self.hero_character.character_save()

            self.questions.do_you_want_to_find_new_enemy()

            return

        else:
            print("You've lost(")
            self.enemy_character.win = 0
            self.save_score()
            self.questions.do_you_want_to_create_hero()
            return

    def toss_coin(self):
        print('Toss a coin, to define, who attacks first.')
        self.turn = random.choice(['enemy', 'hero'])
        print(f'First move is by {self.turn}.')

    def make_move(self):
        if self.turn == 'enemy':
            print("\nEnemy's move")
            self.game_over = self.enemy_character.attack_hero_character(self.hero_character)
            self.draw_hero_n_enemy()

            self.turn = 'hero'

        elif self.turn == 'hero':
            print("Your turn")

            self.game_over = self.hero_character.attack_enemy_character(self.enemy_character)

            self.draw_hero_n_enemy()

            self.turn = 'enemy'

            if not self.game_over:
                self.questions.readiness_before_enemys_attack()

    def save_score(self):
        print('save_score')
        pass

    def tell_rules(self):
        print('tell rules\n')
        pass

    # working with data

    def look_for_characters(self):  # choosing character from saved characters in file 'saves.txt'. characters.
        # format: name[poke_num,poke_num,poke_num]

        # print saved characters with pokemons
        with open('saves.txt', 'r') as file:
            saves = file.read()

        with open('pokemon.csv', 'r') as pokemons_data:
            csv_file = csv.DictReader(pokemons_data)
            pokemons = [x for x in csv_file]

        start_index = 0
        end_index = -2

        end = False
        while not end:
            start_index = end_index + 2
            end_index = saves.index('[', start_index)
            print(saves[start_index:end_index])

            start_index = end_index
            end_index = saves.index(']', start_index)
            list_ = ast.literal_eval(saves[start_index:end_index + 1])
            poke_list = [Pokemon(poke) for poke in pokemons if int(poke['pokedex_number']) in list_]
            for poke in poke_list:
                poke.draw()
                print()

            if saves[end_index + 1] == '.':
                end = True

        self.hero_character.name = self.questions.choose_character(saves)
        print(self.hero_character.name)

        start_index = saves.index('[', saves.index(self.hero_character.name))
        end_index = saves.index(']', start_index)

        list_ = ast.literal_eval(saves[start_index:end_index + 1])

        self.hero_character.pokemon_list = [Pokemon(poke) for poke in pokemons if int(poke['pokedex_number']) in list_]

        for poke in self.hero_character.pokemon_list:
            poke.draw()

    def create_hero_character(self):
        print('Ok, I already have chosen two good pokemons for You, here they are: ')

        self.questions.do_you_like_pokemons()

        name_question = input('\nPlease, enter Your name: ')

        self.hero_character.name = name_question

        self.hero_character.character_first_save()

    def draw_two_pokes_in_row(self, left_poke, right_poke):
        left_poke_temp = copy.deepcopy(left_poke)
        right_poke_temp = copy.deepcopy(right_poke)
        dif = len(left_poke_temp.strings) - len(right_poke_temp.strings)

        if dif < 0:
            for i in range(abs(dif)):
                left_poke_temp.strings.append(' ' * 36 + ' ')
        elif dif > 0:
            for i in range(abs(dif)):
                right_poke_temp.strings.append('')

        picture = []

        for i in range(len(left_poke_temp.strings)):
            picture.append(left_poke_temp.strings[i] + right_poke_temp.strings[i])

        for string_ in picture:
            print(string_)

    def draw_hero_n_enemy(self):
        print(' ' * 10 + self.hero_character.name + ' ' * 32 + self.enemy_character.name)
        for poke_index in range(len(self.hero_character.pokemon_list)):
            self.draw_two_pokes_in_row(self.hero_character.pokemon_list[poke_index],
                                       self.enemy_character.pokemon_list[poke_index])
            print()

    def collecting_pokemons(self):
        for pokemon in self.hero_character.pokemon_list:
            pokemon.curr_hp = pokemon.hp
            pokemon.alive = 1
            pokemon.create_repr_strings()
        for pokemon in self.enemy_character.pokemon_list:
            pokemon.curr_hp = pokemon.hp
            pokemon.alive = 1
            pokemon.create_repr_strings()

        avg_team_speed = sum([poke.speed for poke in self.hero_character.pokemon_list]) \
                         / len(self.hero_character.pokemon_list)

        q_caught_pokemons = 0

        for poke in self.enemy_character.pokemon_list:
            if poke.speed <= avg_team_speed:
                print(f'You caught {poke.name}')
                q_caught_pokemons += 1
                self.hero_character.pokemon_list.append(poke)

        if q_caught_pokemons == 0:
            print("\nUnfortunately, You didn't catch any pokemons(")
        elif q_caught_pokemons == 1:
            print(f'You have caught {q_caught_pokemons} pokemon\n')
        else:
            print(f'You have caught {q_caught_pokemons} pokemons\n')
