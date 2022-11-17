from character import Character

import random


class EnemyCharacter(Character):
    def __init__(self, win=0, name='name', pokemon_list=None):
        Character.__init__(self, win, name, pokemon_list)
        if pokemon_list is None:
            self.pokemon_list = []

    def attack_hero_character(self, hero_character):
        attacking_pokemon = random.choice([poke for poke in self.pokemon_list if poke.alive])
        attacked_pokemon = random.choice([poke for poke in hero_character.pokemon_list if poke.alive])

        game_over = self.pokemon_attacking_pokemon(attacking_pokemon, attacked_pokemon, hero_character)
        return game_over
