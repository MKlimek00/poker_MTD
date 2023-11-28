import random
import poker
from typing import List
import click

from display import display_configuration, enable_ansi, generate_unique_names


@click.command()
@click.argument('n_players', type=int, default=4)
def main(n_players: int):
    enable_ansi()

    N = 52
    if n_players > 22 or n_players < 2:
        raise ValueError(f'Invalid number of players: {n_players}. Must be at least 2 and at most 22')


    deck = [poker.Card(i) for i in range(1,N+1)] # talia -> pełna lista 52 kart
    table = [] # karty leżące na stole
    burned = [] # karty odrzucone

    #rozdanie kart graczom
    players: List[poker.Player] = []
    for player_id, name in enumerate(generate_unique_names()):
        p = poker.Player(name)
        p.cards.append(deck.pop(random.randint(0, len(deck)-1)))
        p.cards.append(deck.pop(random.randint(0, len(deck)-1)))
        players.append(p)
        if player_id == n_players - 1:
            break

    # odrzucenie następnej karty
    burned.append(deck.pop(random.randint(0, len(deck)-1)))

    #losowanie pierwszych 3 kart leżących na stole
    for i in range(3):
        table.append(deck.pop(random.randint(0, len(deck)-1)))

    poker.analizeRound(players, table, deck)
    display_configuration(players, table, burned)
    for p in players:
        p.clearStats()

    # odrzucenie następnej karty
    burned.append(deck.pop(random.randint(0, len(deck)-1)))

    #wylosowanie czwartej karty
    table.append(deck.pop(random.randint(0, len(deck)-1)))

    #analiza wygranych
    poker.analizeRound(players, table, deck)
    # print(poker.summary(players, table, burned))
    display_configuration(players, table, burned)
    for p in players:
        p.clearStats()

    # #odrzucenie kolejnej
    burned.append(deck.pop(random.randint(0, len(deck)-1)))

    # #wylosowanie ostatniej - piątej karty
    table.append(deck.pop(random.randint(0, len(deck)-1)))

    #analiza wygranych
    poker.analizeRound(players, table, deck)
    display_configuration(players, table, burned, is_last_round=True)


if __name__ == '__main__':
    main()
