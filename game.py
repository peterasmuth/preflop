from treys import Card, Deck, Evaluator
import random
import itertools
import pandas as pd

class Game():
    def __init__(self, p1_cards, p2_cards, stub):
        self.p1_cards = p1_cards
        self.p2_cards = p2_cards
        self.stub = stub
        self.evaluator = Evaluator()

        self.p1_eq, self.p2_eq = self.equity()

    def play_games(self):
        results = []
        for a in ['all-in', 'fold']:
            if a == 'all-in':
                for b in ['call', 'fold']:
                    if b == 'call':
                        # split pot based on equity
                        result = [self.p1_cards, self.p2_cards, a, b, self.p1_eq, self.p2_eq]
                        results.append(result)
                    else:
                        # pot goes to player 1
                        result = [self.p1_cards, self.p2_cards, a, b, 1, 0]
                        results.append(result)
            else:
                # pot goes to player 2
                result = [self.p1_cards, self.p2_cards, a,'call', 0, 1]
                results.append(result)
        return results

    def equity(self):
        p1_wins = 0
        p1_ties = 0
        for n in range(0,100):
            board = random.sample(self.stub, 5)
            p1_score = self.evaluator.evaluate(board, self.p1_cards)
            p2_score = self.evaluator.evaluate(board, self.p2_cards)
            if p1_score < p2_score:
                p1_wins += 1
            elif p1_score == p2_score:
                p1_ties += 1
        p1_equity = (p1_wins + p1_ties/2)/100
        p2_equity = 1 - p1_equity

        return [round(p1_equity, 2), round(p2_equity, 2)]


def get_equivalent_combos(cards):
    try:
        c1, c2 = cards
    except ValueError:
        return []
    
    # create a deck
    deck = Deck.GetFullDeck()

    # check for pair
    if Card.get_rank_int(c1) == Card.get_rank_int(c2):
        same_rank = [c for c in deck if Card.get_rank_int(c) == Card.get_rank_int(c1)]
        # return a list of pocket pairs of the same rank
        combos = list(itertools.combinations(same_rank,2))
        sets = []
        for c in combos:
            sets.append(set(c))
        return sets
    # check for suitedness
    elif Card.get_suit_int(c1) == Card.get_suit_int(c2):
        c1_same_rank = [c for c in deck if Card.get_rank_int(c) == Card.get_rank_int(c1)]
        c2_same_rank = [c for c in deck if Card.get_rank_int(c) == Card.get_rank_int(c2)]
        combos = []
        for a in c1_same_rank:
            for b in c2_same_rank:
                if Card.get_suit_int(a) == Card.get_suit_int(b):
                    combos.append(set([a,b]))
        return combos
    # unsuited unpaired
    else:
        c1_same_rank = [c for c in deck if Card.get_rank_int(c) == Card.get_rank_int(c1)]
        c2_same_rank = [c for c in deck if Card.get_rank_int(c) == Card.get_rank_int(c2)]
        combos = []
        for a in c1_same_rank:
            for b in c2_same_rank:
                if Card.get_suit_int(a) != Card.get_suit_int(b):
                    combos.append(set([a,b]))
        return combos

def print_list_of_combos(combos):
    for c in combos:
        print(Card.print_pretty_cards(list(c)))

def load_equity_table():
    return pd.read_csv('equity_table.csv')


def filter_equity_table(hand, table):
    return table[table.p1_c1.isin(hand) & table.p1_c2.isin(hand)]

def test_equivalent_combos():
    first_combo = [Card.new('Ah'),Card.new('Kh')]
    second_combo = [Card.new('Ah'),Card.new('Kd')]
    third_combo = [Card.new('Ah'),Card.new('As')]

    print_list_of_combos(get_equivalent_combos(first_combo))
    print_list_of_combos(get_equivalent_combos(second_combo))
    print_list_of_combos(get_equivalent_combos(third_combo))


def data_cleaning():
    with open('equity_table.csv','r') as file, open('new_equity_table.csv','w') as new_file:
        data = file.read()
        data = data.replace('[','')
        data = data.replace(']','')
        data = data.replace('\"','')
        new_file.write(data)


hand = {Card.new('As'),Card.new('8c')}
table = load_equity_table()
import code; code.interact(local = locals())