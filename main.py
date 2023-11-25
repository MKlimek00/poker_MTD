import random
import poker
from typing import List

def main():
    N = 52
    numberOfPlayers = 3 # liczba graczy, max = 22

    deck = [poker.Card(i) for i in range(1,N+1)] # talia -> pełna lista 52 kart
    table = [] # karty leżące na stole
    burned = [] # karty odrzucone

    #rozdanie kart graczom
    players: List[poker.Player] = []
    id = 1
    for p in range(numberOfPlayers):
        p = poker.Player()
        p.name = str(id)
        id +=1
        p.cards.append(deck.pop(random.randint(0, len(deck)-1)))
        p.cards.append(deck.pop(random.randint(0, len(deck)-1)))
        players.append(p)

    # odrzucenie następnej karty
    burned.append(deck.pop(random.randint(0, len(deck)-1)))

    #losowanie pierwszych 3 kart leżących na stole
    for i in range(3):
        table.append(deck.pop(random.randint(0, len(deck)-1)))

    poker.analizeRound(players, table, deck)
    print(poker.summary(players, table, burned))
    for p in players:
        p.clearStats()

    # odrzucenie następnej karty
    burned.append(deck.pop(random.randint(0, len(deck)-1)))

    #wylosowanie czwartej karty
    table.append(deck.pop(random.randint(0, len(deck)-1)))

    #analiza wygranych
    poker.analizeRound(players, table, deck)
    print(poker.summary(players, table, burned))
    for p in players:
        p.clearStats()

    # #odrzucenie kolejnej
    burned.append(deck.pop(random.randint(0, len(deck)-1)))

    # #wylosowanie ostatniej - piątej karty
    table.append(deck.pop(random.randint(0, len(deck)-1)))

    #analiza wygranych
    poker.analizeRound(players, table, deck)
    print(poker.summary(players, table, burned))


main()
