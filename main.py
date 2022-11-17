import const

from game import Game

pokemon_battle = Game()

while pokemon_battle.user_in_console:
    if pokemon_battle.user_lost:
        pokemon_battle = Game()

        pokemon_battle.start_phase()
        # break  # temp
        # Now we have a hero character with pokemons who is ready to start the game

        pokemon_battle.user_lost = False

    enemy_character = pokemon_battle.create_enemy_character()

    # pokemon_battle.countdown()y

    pokemon_battle.game()

print('Look forward to You! Bye;)')
print('To escape, press Enter')
input()
