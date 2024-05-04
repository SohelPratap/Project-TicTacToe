import numpy as np


class Agent:
    def __init__(self):
        self.epsilon = 0.1
        self.alpha = 0.5
        self.state_history = []

    def initialize_V(self, env, state_winner_triples):
        V = np.zeros(env.max_states)
        for state, winner, ended in state_winner_triples:
            if ended:
                if winner == env.x:
                    state_value = 1
                else:
                    state_value = 0
            else:
                state_value = 0.5

            V[state] = state_value
        self.V = V

    def set_symbol(self, symbol):
        self.symbol = symbol

    def reset_history(self):
        self.state_history = []

    def choose_random_action(self, env):
        empty_moves = env.get_empty_moves()
        random_index_from_empty_moves = np.random.choice(len(empty_moves))
        next_random_move = empty_moves[random_index_from_empty_moves]
        return next_random_move

    def choose_best_action_from_states(self, env):
        next_best_move, best_state = env.get_next_best_move(self)
        return next_best_move, best_state

    def get_next_move(self, env):
        next_best_move, best_state = None, None
        random_number = np.random.rand()
        if random_number < self.epsilon:
            next_best_move = self.choose_random_action(env)
        else:
            next_best_move, best_state = self.choose_best_action_from_states(env)
        return next_best_move, best_state

    def take_action(self, env):
        selected_next_move, best_state = self.get_next_move(env)
        env.board[selected_next_move[0], selected_next_move[1]] = self.symbol

    def update_state_history(self, state):
        self.state_history.append(state)

    def update(self, env):
        reward = env.reward(self.symbol)
        target = reward
        for prev in reversed(self.state_history):
            value = self.V[prev] + self.alpha * (target - self.V[prev])
            self.V[prev] = value
            target = value
        self.reset_history()


class Environment:

    def __init__(self):
        self.board = np.zeros((3, 3))
        self.x = -1
        self.o = 1
        self.winner = None
        self.ended = False
        self.max_states = 3 ** (3 * 3)

    def is_empty(self, i, j):
        return self.board[i, j] == 0

    def reward(self, symbol):
        collected_reward = 0
        if self.game_over() and self.winner == symbol:
            collected_reward = 1
        return collected_reward

    def is_draw(self):
        is_draw = False
        if self.ended and self.winner is None:
            is_draw = True
        return is_draw

    def get_state(self):
        state = 0
        loop_index = 0
        for i in range(3):
            for j in range(3):
                if self.board[i, j] == self.x:
                    state_value = 1
                elif self.board[i, j] == self.o:
                    state_value = 2
                else:
                    state_value = 0
                state += (3 ** loop_index) * state_value
                loop_index += 1
        return state

    def game_over(self):
        if self.ended:
            return True

        players = [self.x, self.o]

        for i in range(3):
            for player in players:
                if self.board[i].sum() == player * 3:
                    self.winner = player
                    self.ended = True
                    return True

        for j in range(3):
            for player in players:
                if self.board[:, j].sum() == player * 3:
                    self.winner = player
                    self.ended = True
                    return True

        for player in players:
            if self.board.trace() == player * 3:
                self.winner = player
                self.ended = True
                return True

            if np.fliplr(self.board).trace() == player * 3:
                self.winner = player
                self.ended = True
                return True

        board_with_true_false = self.board == 0
        if np.all(board_with_true_false == False):
            self.winner = None
            self.ended = True
            return True

        self.winner = None
        return False

    def get_empty_moves(self):
        empty_moves = []
        for i in range(3):
            for j in range(3):
                if self.is_empty(i, j):
                    empty_moves.append((i, j))
        return empty_moves

    def get_next_best_move(self, agent):
        best_value = -1
        next_best_move = None
        best_state = None
        for i in range(3):
            for j in range(3):
                if self.is_empty(i, j):
                    self.board[i, j] = agent.symbol
                    state = self.get_state()
                    self.board[i, j] = 0
                    if agent.V[state] > best_value:
                        best_value = agent.V[state]
                        best_state = state
                        next_best_move = (i, j)

        return next_best_move, best_state

    def draw_board(self):
        def __print(to_print, j):
            if j == 0:
                print(f"|  {to_print}  ", end="|")
            else:
                print(f"{to_print}  ", end="|")

        for i in range(3):
            print(" ---------------------")
            for j in range(3):
                print("  ", end="")
                if self.board[i, j] == self.x:
                    __print('x', j)
                elif self.board[i, j] == self.o:
                    __print('o', j)
                else:
                    __print(' ', j)
            print("")
        print(" ---------------------")
        print("\n")


class Human:

    def set_symbol(self, symbol):
        self.symbol = symbol

    def take_action(self, env):
        while True:
            try:
                move = input("Enter box location to make your move in format of i,j : ")
                i, j = [int(item.strip()) for item in move.split(',')]
                if env.is_empty(i, j):
                    env.board[i, j] = self.symbol
                    break
                else:
                    print("Please enter valid move")
            except:
                print("Please enter valid move")


def get_state_hash_and_winner(env, i=0, j=0):
    results = []
    for v in [0, env.x, env.o]:
        env.board[i, j] = v
        if j == 2:
            if i == 2:
                state = env.get_state()
                ended = env.game_over()
                winner = env.winner
                results.append((state, winner, ended))
            else:
                results += get_state_hash_and_winner(env, i + 1, 0)
        else:
            results += get_state_hash_and_winner(env, i, j + 1)
    return results


def play_game(agent, human, env, print_board=True):
    current_player = None
    continue_game = True
    while continue_game:
        if current_player == agent:
            current_player = human
        else:
            current_player = agent

        current_player.take_action(env)

        if current_player == agent:
            state = env.get_state()
            agent.update_state_history(state)
            agent.update(env)
            if print_board:
                env.draw_board()

        if env.game_over():
            continue_game = False


def main(should_learn_before_playing):
    print("Starting the game...")
    print("Agent -> x")
    print("Human -> o")

    env = Environment()

    state_winner_triples = get_state_hash_and_winner(env)

    agent = Agent()
    agent.set_symbol(env.x)
    agent.initialize_V(env, state_winner_triples)

    if should_learn_before_playing:
        print("Agent is playing with himself to learn...")
        agent_to_learn = Agent()
        agent_to_learn.set_symbol(env.o)
        agent_to_learn.initialize_V(env, state_winner_triples)

        for i in range(10000):
            if i > 0 and i % 1000 == 0:
                print(f"Agent has played {i} times")
            play_game(agent, agent_to_learn, Environment(), print_board=False)
        print("")
        print("Agent has learned by playing with himself 10,000 times...")

    human = Human()
    human.set_symbol(env.o)
    total_game_played = 0
    while True:
        env = Environment()
        play_game(agent, human, env=env)

        total_game_played += 1
        print(f"Game number: {total_game_played}")
        if env.winner == env.x:
            print(f"Agent won the game")
        elif env.winner == env.o:
            print(f"You won the game")
        else:
            print(f"Game is draw")

        answer = input("Do you want to play again? [y/n]: ")
        if answer and answer.lower()[0] == 'n':
            break


if __name__ == '__main__':
    main(should_learn_before_playing=True)
