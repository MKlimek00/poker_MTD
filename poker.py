from enum import Enum
from typing import List, Dict
import numpy as np
from combinatorics import k_subsets as kSUB, COM_5_7

class Suit(Enum):
    HEARTS = 0
    DIAMONDS = 1
    SPADES = 2
    CLUBS = 3

class Rank(Enum):
    KING = 12
    QUEEN = 11
    JACK = 10
    _10 = 9
    _9 = 8
    _8 = 7
    _7 = 6
    _6 = 5
    _5 = 4
    _4 = 3
    _3 = 2
    _2 = 1
    ACE = 0

class Combination(Enum):
    STRAIGHT_FLUSH = 9 
    FOUR_OF_A_KIND = 8 
    FULL_HOUSE = 7 
    FLUSH = 6 
    STRAIGHT = 5 
    THREE_OF_A_KIND = 4 
    TWO_PAIRS = 3 
    ONE_PAIR = 2 
    HIGH_CARD = 1




class Card():
    """
    Class for storing data about every contour detected
    """
    def __init__(self, num : int):
        self.id : int = num-1
        self.suit : Suit = Suit(self.id//13)
        self.rank : Rank = Rank(self.id%13)

    def __repr__(self) -> str:
        return f'{self.rank.name} of {self.suit.name}'


class Player():
    def __init__(self, name: str):
        self.cards : List[Card] = []
        self.name : str = name
        self.posibillities : int = 0
        self.wins : int = 0
        self.draws : int = 0
        self.numberOfSets : Dict = {comb : 0 for comb in Combination}


    def __repr__(self) -> str:
        return f'\nPlayer {self.name} \nHand: {self.cards}\n wins|draws|total : {self.wins}|{self.draws}|{self.posibillities} \nsets: {self.numberOfSets}\n'


    def __str__(self) -> str:
        return repr(self)


    def clearStats(self) -> None:
        self.posibillities = 0
        self.wins = 0
        self.draws = 0
        self.numberOfSets : Dict = {comb : 0 for comb in Combination}



def analizeRound(players: List[Player], table: List[Card], deck: List[Card]) -> None:
    '''
    Funkcja sprawdza który gracz ile razy wygra przy dostępnych możliwych brakujących kartach
    '''
    subsetSize = 5 - len(table)
    subsets = kSUB(n = len(deck), p = -1, k = subsetSize)

    if(subsetSize == 0):
        for p in players:
            p.posibillities = 1
        subsetOutcomes = [] * len(players)
        for i in range(len(players)) :
            outComb = analizeSet(players[i].cards + table)
            subsetOutcomes.append(outComb)
            players[i].numberOfSets[outComb] += 1

        winningComb = max(subsetOutcomes, key=lambda item:item.value)
        # print(subsetOutcomes)
        arr = np.array(subsetOutcomes)
        indices = list(np.where(arr == winningComb)[0])

        if len(indices) > 1:
            for id in indices:
                players[id].draws = players[id].draws + 1

        if len(indices) == 1:
            players[indices[0]].wins = players[indices[0]].wins + 1
        return
        

    for p in players:
        p.posibillities = len(subsets)

    for ss in subsets :
        ssCards = [deck[i-1] for i in ss]
        subsetOutcomes = [] * len(players) # lista wyników danych graczy przy danym dobranym subsecie

        for i in range(len(players)) :
            outComb = analizeSet(players[i].cards + table + ssCards)
            subsetOutcomes.append(outComb)
            players[i].numberOfSets[outComb] += 1

        winningComb = max(subsetOutcomes, key=lambda item:item.value)
        # print(subsetOutcomes)
        arr = np.array(subsetOutcomes)
        indices = list(np.where(arr == winningComb)[0])

        if len(indices) > 1:
            for id in indices:
                players[id].draws = players[id].draws + 1

        if len(indices) == 1:
            players[indices[0]].wins = players[indices[0]].wins + 1


def analizeSet(cards: List[Card]) -> Combination:
    '''
    Funkcja znajduje najlepszy 5 kartowy układ w 7 kartowym zbiorze
    '''
    subsets = COM_5_7
    bestComb = 1 # HIGH_CARD
    for ss in subsets:
        ssCards = [cards[i-1] for i in ss]
        comb = analizeSubset(ssCards).value
        bestComb = max([comb, bestComb])
    return Combination(bestComb)



def analizeSubset(cards: List[Card]) -> Combination:
    '''
    Funkcja rozpoznaje układ pokerowy w podanym zbiorze 5 kart
    '''
    combs = [sameRankCombinations, isStraightOrFlush]
    detCombs = []
    for comb in combs:
        detCombs.append(comb(cards))
    return max(detCombs, key=lambda item:item.value)


def isStraightOrFlush(cards: List[Card])-> Combination:
        '''
        Funkcja rozpoznaje czy w podanym zbiorze 5 kart znajduje się poker, kolor lub strit
        '''
        cards.sort(key=lambda card: card.rank.value)
        counterF = sum(card.suit == cards[0].suit for card in cards)
        counterS = sum(cards[i].rank.value == (cards[0].rank.value + i) for i in range(len(cards)))
        if counterF == 5 and counterS == 5:
            return Combination.STRAIGHT_FLUSH
        if counterF == 5:
            return Combination.FLUSH
        if counterS == 5:
            return Combination.STRAIGHT
        
        return Combination.HIGH_CARD


def sameRankCombinations(cards: List[Card]) -> Combination:
        '''
        Funkcja rozpoznaje czy w podanym zbiorze 5 kart znajduje się kareta, full, trójka, dwie pary lub para
        '''
        temp_map = {}
        for card in cards :
            if card.rank.name in temp_map:
                temp_map[card.rank.name] += 1
            else:
                temp_map[card.rank.name] = 1
        rank_map = {}
        for v in temp_map.values():
            if v in rank_map:
                rank_map[v] +=1
            else: 
                rank_map[v] = 1

        if 4 in rank_map.keys():
            return Combination.FOUR_OF_A_KIND

        if 3 in rank_map.keys() and 2 in rank_map.keys():
            return Combination.FULL_HOUSE

        if 3 in rank_map.keys() and 2 not in rank_map.keys():
            return Combination.THREE_OF_A_KIND

        if 2 in rank_map.keys() and rank_map[2] == 2:
            return Combination.TWO_PAIRS

        if 2 in rank_map.keys() and rank_map[2] == 1:
            return Combination.ONE_PAIR
        
        return Combination.HIGH_CARD


def summary(players: List[Player], table: List[Card], burned : List[Card]) -> str:
    text = f"""
Number of players: {len(players)}, Cards on table: {len(table)}, Burned cards: {len(burned)}
Cards on table: {table}
Burned cards: {burned}
{players}
"""
    return text
