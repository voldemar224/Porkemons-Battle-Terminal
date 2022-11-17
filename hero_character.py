from character import Character
from pokemon import Pokemon

import copy
import const


class HeroCharacter(Character):
    def __init__(self, win=0, name='name', pokemon_list=None):
        Character.__init__(self, win, name, pokemon_list)
        if pokemon_list is None:
            self.pokemon_list = []

    def draw_pokemons(self):
        pass

    def create(self):
        print('creating hero')

    def choose_target(self, enemy_character):
        chosen_pokemon_index = int(input('Choose a pokemon, which You want to attack! 1/2/3...')) - 1

        pokemon = copy.deepcopy(enemy_character.pokemon_list[chosen_pokemon_index])

        return pokemon

    def attack_enemy_character(self, enemy_character):
        # Choose a pokemon, with which You want to attack Your enemy!
        question_answered = const.question_answered
        while not question_answered:
            attacking_pokemon_index = int(input('Choose a pokemon, '
                                                'with which You want to attack Your enemy! 1/2/3...')) - 1
            if 0 <= attacking_pokemon_index < len(self.pokemon_list):
                if not self.pokemon_list[attacking_pokemon_index].alive:
                    print('This pokemon has already died. Choose another one!')
                else:
                    attacking_pokemon = self.pokemon_list[attacking_pokemon_index]
                    question_answered = True
            else:
                print('Invalid syntax, try again!')

        # Choose a pokemon, which You want to attack! 1/2/3...
        question_answered = const.question_answered
        while not question_answered:
            chosen_pokemon_index = int(input('Choose a pokemon, which You want to attack! 1/2/3...')) - 1
            if not enemy_character.pokemon_list[chosen_pokemon_index].alive:
                print("You killed this pokemon already. Choose another one!")
            elif 0 <= chosen_pokemon_index < len(self.pokemon_list):
                attacked_pokemon = enemy_character.pokemon_list[chosen_pokemon_index]
                question_answered = True
            else:
                print('Invalid syntax, try again!')

        game_over = self.pokemon_attacking_pokemon(attacking_pokemon, attacked_pokemon, enemy_character)
        return game_over
