import json
import copy  # use it for deepcopy if needed
import math  # for math.inf
import itertools
import logging

logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)

# Global variables in which you need to store player strategies (this is data structure that'll be used for evaluation)
# Mapping from histories (str) to probability distribution over actions
memory_dict = {}
strategy_dict_x = {}
strategy_dict_o = {}


class History:
    def __init__(self, history=None):
        """
        # self.history : Eg: [0, 4, 2, 5]
            keeps track of sequence of actions played since the beginning of the game.
            Each action is an integer between 0-8 representing the square in which the move will be played as shown
            below.
              ___ ___ ____
             |_0_|_1_|_2_|
             |_3_|_4_|_5_|
             |_6_|_7_|_8_|

        # self.board
            empty squares are represented using '0' and occupied squares are either 'x' or 'o'.
            Eg: ['x', '0', 'x', '0', 'o', 'o', '0', '0', '0']
            for board
              ___ ___ ____
             |_x_|___|_x_|
             |___|_o_|_o_|
             |___|___|___|

        # self.player: 'x' or 'o'
            Player whose turn it is at the current history/board

        :param history: list keeps track of sequence of actions played since the beginning of the game.
        """
        if history is not None:
            self.history = history
            self.board = self.get_board()
        else:
            self.history = []
            self.board = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        self.player = self.current_player()

    def current_player(self):
        """ Player function
        Get player whose turn it is at the current history/board
        :return: 'x' or 'o' or None
        """
        total_num_moves = len(self.history)
        if total_num_moves < 9:
            if total_num_moves % 2 == 0:
                return 'x'
            else:
                return 'o'
        else:
            return None

    def get_board(self):
        """ Play out the current self.history and get the board corresponding to the history in self.board.

        :return: list Eg: ['x', '0', 'x', '0', 'o', 'o', '0', '0', '0']
        """
        board = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        for i in range(len(self.history)):
            if i % 2 == 0:
                board[self.history[i]] = 'x'
            else:
                board[self.history[i]] = 'o'
        return board

    def is_win(self):

        # List of all possible winning combinations
        winning_combinations = [ [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6] ]

        # Check if any of the winning combinations are present in the board
        for combination in winning_combinations:
            if self.board[combination[0]] == self.board[combination[1]] == self.board[combination[2]] != '0':
                return self.board[combination[0]]
        return None

    def is_draw(self):
        
        return '0' not in self.board and not self.is_win()

    def get_valid_actions(self):
        
        valid_actions = []
        for i in range(9):
            if self.board[i] == '0':
                valid_actions.append(i)
        return valid_actions

    def is_terminal_history(self):
        
        # Check if the game is won or drawn
        return self.is_win() is not None or self.is_draw()

    def get_utility_given_terminal_history(self):

        # If the game is won by 'x', return 1 and if won by 'o', return -1 else return 0
        if self.is_win() == 'x':
            return 1
        elif self.is_win() == 'o':
            return -1
        else:
            return 0
        

    def update_history(self, action):

        # Deep copy the history and update the action
        new_history = copy.deepcopy(self.history)
        new_history.append(action)
        return History(new_history)

    def get_board_str(self):
        return ''.join(self.board)

def update_strategy_dict(history_obj, history_key, action):
    global strategy_dict_x, strategy_dict_o
    if history_obj.player == 'x':
        if history_key not in strategy_dict_x:
            strategy_dict_x[history_key] = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0}
        strategy_dict_x[history_key][str(action)] = 1
    else:
        if history_key not in strategy_dict_o:
            strategy_dict_o[history_key] = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0}
        strategy_dict_o[history_key][str(action)] = 1

def generate_history_keys(history_str):
    # Determine the length of history_str
    num_moves = len(history_str)

    # Generate all permutations of numbers 0 to 8 of length num_moves
    possible_moves = list(range(9))
    permutations = itertools.permutations(possible_moves, num_moves)

    # Generate history_key for each permutation
    history_keys = []
    for perm in permutations:
        history_key = ''.join(map(str, perm))
        temp_history_str = get_board_str_from_history(history_key)
        if temp_history_str == history_str:
            history_keys.append(history_key)

    return history_keys

def get_board_str_from_history(history_key):
    # Initialize an empty board
    board = ['0'] * 9
    player = 'x'  # Start with player 'x'
    
    # Apply each action from history_key to build the board
    for i, action in enumerate(history_key):
        action = int(action)
        board[action] = 'x' if player == 'x' else 'o'
        player = 'o' if player == 'x' else 'x'  # Switch player

    return ''.join(board)

def backward_induction(history_obj):
    global strategy_dict_x, strategy_dict_o, memory_dict

    # Combine history from a list to str and action to form a key
    history_key = ''.join(map(str, history_obj.history))
    history_str = history_obj.get_board_str()

    # Check if the history_str is already present
    if history_str in memory_dict:
        best_action = memory_dict[history_str][1]
        update_strategy_dict(history_obj, history_key, best_action)
        return memory_dict[history_str][0]

    if history_obj.is_terminal_history():
        memory_dict[history_str] = [history_obj.get_utility_given_terminal_history(), None]
        return history_obj.get_utility_given_terminal_history()

    best_utility = -math.inf if history_obj.player == 'x' else math.inf
    valid_actions = history_obj.get_valid_actions()
    best_action = None

    for action in valid_actions:
        new_history = history_obj.update_history(action)
        utility = backward_induction(new_history)
        if history_obj.player == 'x' and utility > best_utility:
            best_utility = utility
            best_action = action
        elif history_obj.player == 'o' and utility < best_utility:
            best_utility = utility
            best_action = action

    memory_dict[history_str] = [best_utility, best_action]
    update_strategy_dict(history_obj, history_key, best_action)

    return best_utility

def solve_tictactoe():
    print(generate_history_keys('x0ox0o000'))
    backward_induction(History())
    with open('./policy_x.json', 'w') as f:
        json.dump(strategy_dict_x, f)
    with open('./policy_o.json', 'w') as f:
        json.dump(strategy_dict_o, f)
    return strategy_dict_x, strategy_dict_o

if __name__ == "__main__":
    logging.info("Start")
    solve_tictactoe()
    logging.info("End")
