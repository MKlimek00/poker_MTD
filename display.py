import matplotlib.pyplot as plt
import numpy as np

import os
from math import ceil
import copy
from random import shuffle

import matplotlib.pyplot as plt

from poker import Card, Player, Suit, Rank, Combination
from typing import List, Tuple, Final, Generator


PLAYER_NAMES: Final[List[str]] = [
    'Alicja',
    'Bogna',
    'Chwalibog',
    'Drogomir',
    'Eustachy',
    'Falibor',
    'Gościwuj',
    'Himisław',
    'Izybora',
    'Jaropełk',
    'Kazimiera',
    'Ludmiła',
    'Mirogniewa',
    'Niedamir',
    'Osięgniew',
    'Przybywuj',
    'Rzędziwoj',
    'Sławomira',
    'Trzebowit',
    'Uniegost',
    'Wisława',
    'Zawisza',
    'Żelibrat'
]


def generate_unique_names() -> Generator[None, str, None]:
    names = copy.copy(PLAYER_NAMES)
    shuffle(names)
    for n in names:
        yield n


def _suit_as_unicode(suit: Suit) -> str:
    """
    Wyświetla kolor karty jako znaczek
    """
    if suit == Suit.CLUBS:
        return '♣'
    elif suit == Suit.DIAMONDS:
        return '♦'
    elif suit == Suit.HEARTS:
        return '♥'
    elif suit == Suit.SPADES:
        return '♠'

def _rank_as_compact_repr(rank: Rank) -> str:
    """
    Zwraca kartę jako numerek lub literkę
    """
    if rank == Rank._2:
        return '2'
    elif rank == Rank._3:
        return '3'
    elif rank == Rank._4:
        return '4'
    elif rank == Rank._5:
        return '5'
    elif rank == Rank._6:
        return '6'
    elif rank == Rank._7:
        return '7'
    elif rank == Rank._8:
        return '8'
    elif rank == Rank._9:
        return '9'
    elif rank == Rank._10:
        return '10'
    elif rank == Rank.ACE:
        return 'A'
    elif rank == Rank.JACK:
        return 'J'
    elif rank == Rank.QUEEN:
        return 'Q'
    elif rank == Rank.KING:
        return 'K'


def card_as_compact_repr(suit: Suit, rank: Rank) -> str:
    """
    Zwraca kartę jako zwięzły string, np. as karo to A♦
    """
    return f'{_rank_as_compact_repr(rank)}{_suit_as_unicode(suit)}'


def _clear_console() -> None:
    """
    Czyści konsolę zależnie od OS
    """
    if os.name == 'nt': ## WIN
        os.system('cls')
    else:
        os.system('clear')


def enable_ansi() -> None:
    ## Nie pytaj
    if os.name == 'nt':
        os.system('')


def _wrap_with_rect(upper_value: str, lower_value: str = '') -> Tuple[str, str, str, str]:
    """
    Owija dwie wartości (ważne: jednolinijkowe i o długości max. 3) w czterolinijkowy prostokąt unicode

    ┌───┐
    │ Q │
    │ ♠ │
    └───┘
    """
    top = '┌───┐'
    upper = f'│{upper_value.center(3)}│'
    lower = f'│{lower_value.center(3)}│'
    bottom = '└───┘'

    return (top, upper, lower, bottom)


def display_burned(burned_cards: List[Card]) -> List[str]:
    """
    Wyświetla stos kart odrzuconych
    """
    meta_text = 'Karty odrzucone: '
    meta_display_index = 1

    card_rects_parts = [_wrap_with_rect(_rank_as_compact_repr(c.rank), _suit_as_unicode(c.suit)) for c in burned_cards]

    display_lines = []

    for i in range(4):
        display_str = ''
        if i == meta_display_index:
            display_str = meta_text
        else:
            display_str = ' ' * len(meta_text)

        for rect_parts in card_rects_parts:
            current_line_part = rect_parts[i]
            display_str = f'{display_str}{current_line_part} '

        display_lines.append(display_str)

    return display_lines


def _disp_combination(comb: Combination) -> str:
    if comb == Combination.STRAIGHT_FLUSH:
        return "Poker"
    elif comb == Combination.FOUR_OF_A_KIND:
        return "Kareta"
    elif comb == Combination.FULL_HOUSE:
        return "Full"
    elif comb == Combination.FLUSH:
        return "Kolor"
    elif comb == Combination.STRAIGHT:
        return "Strit"
    elif comb == Combination.THREE_OF_A_KIND:
        return "Trójka"
    elif comb == Combination.TWO_PAIRS:
        return "Dwie pary"
    elif comb == Combination.ONE_PAIR:
        return "Para"
    elif comb == Combination.HIGH_CARD:
        return "Wysoka karta"


def _get_player_max_comb(p: Player) -> str:
    combo = max([cname for (cname, cnt) in p.numberOfSets.items() if cnt > 0], key = lambda c: c.value)
    return _disp_combination(combo)


def _disp_player(player: Player, emphasise_wins: bool, emphasise_draws: bool, is_upper_row: bool, max_width: int = 15) -> Tuple[str, str, str, str]:
    """
    Wyświetla gracza w czterolinijkowej reprezentacji
    """
    name = player.name.center(max_width)

    cards = [card_as_compact_repr(c.suit, c.rank) for c in player.cards]
    cards = ' '.join(cards).center(max_width)

    wins = f'W: {player.wins / player.posibillities * 100:.1f}%'.center(max_width)
    draws = f'R: {player.draws / player.posibillities * 100:.1f}%'.center(max_width)
    combo = _get_player_max_comb(player).center(max_width)
    if emphasise_wins:
        wins = f'\033[95m{wins}\033[0m'
        combo = f'\033[95m{combo}\033[0m'
    elif emphasise_draws:
        draws = f'\033[95m{draws}\033[0m'
        combo = f'\033[95m{combo}\033[0m'

    if is_upper_row:
        return (draws, wins, combo, cards, name)
    else:
        return (name, cards, combo, wins, draws)


def display_players_with_table(players: List[Player], table_cards: List[Card]) -> List[str]:
    """
    Wyświetla graczy i stół
    """
    player_disp_lines = 4
    player_max_width = 15
    padding_lines = 2

    display_lines = []

    max_win_chances = max([p.wins for p in players])
    has_winner = True
    if max_win_chances == 0:
        max_win_chances = max([p.draws for p in players])
        has_winner = False

    split_index = ceil(len(players) / 2)

    player_lines = [
        _disp_player(
            player,
            has_winner and player.wins == max_win_chances,
            not has_winner and player.draws == max_win_chances,
            i < split_index,
            player_max_width
        )
        for i, player in enumerate(players)
    ]

    upper_player_lines = player_lines[:split_index]
    lower_player_lines = player_lines[split_index:]

    for i in range(5):
        display_str = ' '.join([line[i] for line in upper_player_lines])
        display_lines.append(display_str)

    for _ in range(padding_lines):
        display_lines.append('')

    table_cards_parts = [_wrap_with_rect(_rank_as_compact_repr(c.rank), _suit_as_unicode(c.suit)) for c in table_cards]

    for i in range(4):
        display_str = ' '.join([card_parts[i] for card_parts in table_cards_parts])
        display_lines.append(display_str)

    for _ in range(padding_lines):
        display_lines.append('')

    for i in range(5):
        display_str = ' '.join([line[i] for line in lower_player_lines])
        display_lines.append(display_str)

    max_line_width = max([len(line) for line in display_lines])
    padded_lines = [line.center(max_line_width) for line in display_lines]

    return padded_lines


def _show_win_plots(players: List[Player]) -> None:
    """
    Wyświetla wykresy kołowe z p. wygranych, remisów i przegranych
    """
    cols = 4
    rows = ceil(len(players) / cols)

    for i in range(rows):
        for j in range(cols):
            plot_idx = i*cols + j
            if plot_idx >= len(players):
                break
            
            player = players[plot_idx]

            win_proba = player.wins / player.posibillities
            draw_proba = player.draws / player.posibillities
            loss_proba = 1 - (win_proba + draw_proba)

            probas = [win_proba, draw_proba, loss_proba]
            labels = ['Wygrywa', 'Remis', 'Przegrywa']
            colors = ['green', 'gray', 'red']

            labels = list(map(lambda v: v[1], filter(lambda v: probas[v[0]] > 0., enumerate(labels))))
            colors = list(map(lambda v: v[1], filter(lambda v: probas[v[0]] > 0., enumerate(colors))))
            probas = list(filter(lambda v: v > 0., probas))

            plt.subplot(rows, cols, plot_idx + 1)
            plt.pie(
                probas,
                labels=labels,
                colors=colors,
                labeldistance=0.4
            )
            plt.title(player.name)

    plt.show()


def _print_winner(players: List[Player]) -> None:
    """
    Wyświetla zwycięzcę lub remis
    """
    max_wins = max([p.wins for p in players])
    if max_wins > 0:
        winner = [p.name for p in players if p.wins == max_wins][0]
        print(f'Wygrywa: {winner}')
        return

    max_draws = max([p.draws for p in players])
    draw_players = [p.name for p in players if p.draws == max_draws]
    first_players = draw_players[:-1]
    print(f'Remis: {", ".join(first_players)} i {draw_players[-1]}')



def display_configuration(
    players: List[Player],
    table_cards: List[Card],
    burned_cards: List[Card],
    is_last_round: bool = False) -> None:
    """
    Wyświetlenie układu gry
    """
    _clear_console()
    burned_lines = display_burned(burned_cards)
    table_lines = display_players_with_table(players, table_cards)

    lines_merged = [*table_lines, '', *burned_lines]

    max_line_width = max([len(line) - int(line.count('\033')*4.5) for line in lines_merged])
    lines_padded = [line.center(max_line_width + int(line.count('\033')*4)) for line in lines_merged]

    print('┌' + '─'*max_line_width + '┐')

    for line in lines_padded:
        extra_padding = ' ' * (line.count('\033') // 2)
        print(f'│{line}{extra_padding}│')

    print('└' + '─'*max_line_width + '┘')

    if is_last_round:
        _print_winner(players)
    else:
        _show_win_plots(players)
        input('Wciśnij <Enter> aby przejść do kolejnej rundy...')
