from tictactoe import TicTacToe
import math
import random
import time


#helper function to calculate the score associated with each ending state 
#pass in the board, depth, and the ai_player's X/O and returns the score 
def score_calc(board, depth, ai_player):
    if board.current_winner == ai_player:
        return 1 * (depth + 1) #use depth to choose more immediate winning move
    elif board.current_winner is not None:  #winner is not Ai, and winner is not None, meaning the winner is the opponent (bad score)
        return -1 * (depth + 1)
    return 0 #no winner = draw score

def minimax(board, depth, maximizing_player, ai_player):

    #ai_player = string
    #maximizing_player = bool
    #depth = int of available moves
    #board = class

    #returns a dictionary w/ 'position' being one of the keys (added in score as a key too)

    #AI / maximizing player plays O
    #human / other AI plays X


    #base case in which if depth is reached/no available moves/there is a current winner
    if depth == 0 or not board.empty_squares_available() or board.current_winner:
        return {'position': None, 'score': score_calc(board, depth, ai_player)}

    #if its the turn of the maximizing player...
    if maximizing_player:   
        #initialize the maximizing value of a move
        max_curr_result = {'position': None, 'score': -math.inf}

        #iterate for each available move on the board
        for move in board.available_moves():
            #make the hypothetical move for the AI
            board.make_move(move, ai_player)
            #recursively call minimax , subtracting 1 from depth to indicate 1 less available move
            curr_result = minimax(board, depth - 1, False, ai_player)
            #add to dictionary the current move at 'position' key
            curr_result['position'] = move
            #reset current winner to None to avoid bugs and winner carrying over
            board.current_winner = None
            board.board[move] = ' '  # undo move
            #if the score is higher than the current max, then update 
            if curr_result['score'] > max_curr_result['score']:
                max_curr_result = curr_result
        return max_curr_result
    else: #minimizing player move
        min_curr_result = {'position': None, 'score': math.inf}
        for move in board.available_moves():
            board.make_move(move, 'X' if ai_player == 'O' else 'O')
            curr_result = minimax(board, depth - 1, True, ai_player)
            curr_result['position'] = move
            board.current_winner = None
            board.board[move] = ' ' 
            if curr_result['score'] < min_curr_result['score']:
                min_curr_result = curr_result
        return min_curr_result







def minimax_with_alpha_beta(board, depth, alpha, beta, maximizing_player, ai_player):


    if depth == 0 or not board.empty_squares_available() or board.current_winner:
        return {'position': None, 'score': score_calc(board, depth, ai_player)}

    

    if maximizing_player:
        max_curr_result = {'position': None, 'score': -math.inf}
        for move in board.available_moves():
            board.make_move(move, ai_player)
            curr_result = minimax_with_alpha_beta(board, depth - 1, alpha, beta, False, ai_player)
            curr_result['position'] = move
            board.current_winner = None
            board.board[move] = ' '  

            #same logic as above
            if curr_result['score'] > max_curr_result['score']:
                max_curr_result = curr_result
            #add in alpha calculation: since maximizer turn, it will take the max between alpha and the point value associated with the move
            alpha = max(alpha, max_curr_result['score'])
            #pruning (if beta is less than alpha, no need to continue to check)
            if beta <= alpha:
                break
        return max_curr_result
    else:
        min_curr_result = {'position': None, 'score': math.inf}
        for move in board.available_moves():
            board.make_move(move, 'X' if ai_player == 'O' else 'O')
            curr_result = minimax_with_alpha_beta(board, depth - 1, alpha, beta, True, ai_player)
            curr_result['position'] = move
            board.current_winner = None
            board.board[move] = ' ' 

            if curr_result['score'] < min_curr_result['score']:
                min_curr_result = curr_result
            beta = min(beta, min_curr_result['score'])
            if beta <= alpha:
                break
        return min_curr_result

def play_game_human_moves_first():

    game = TicTacToe()
    print("\nInitial Board:")
    game.print_board()

    letter = 'X'  # Human player starts first.
    while game.empty_squares_available():
        if letter == 'O':  # AI's turn
            square = minimax_with_alpha_beta(game, len(game.available_moves()), -math.inf, math.inf, True, 'O')['position']
            if square is None:
                print("\nGame is a draw!")
                break
            game.make_move(square, letter)
            print(f"\nAI (O) chooses square {square + 1}")
        else:
            valid_square = False
            while not valid_square:
                square = input(f"\n{letter}'s turn. Input move (1-9): ")
                try:
                    square = int(square) - 1
                    if square not in game.available_moves():
                        raise ValueError
                    valid_square = True
                    game.make_move(square, letter)
                except ValueError:
                    print("\nInvalid square. Try again.")

        game.print_board()

        if game.current_winner:
            print(f"\n{letter} wins!")
            break

        letter = 'O' if letter == 'X' else 'X'  # Switch turns.
    else:
        print("\nIt's a draw!")

def play_game_ai_moves_first():

    game = TicTacToe()
    print("\nInitial Board:")
    game.print_board()

    first_move = True

    letter = 'O'  # AI player starts first.
    while game.empty_squares_available():
        if letter == 'O':  # AI's turn
            if first_move:
                square = random.randint(0, 8)
                first_move = False
            else:
                square = minimax_with_alpha_beta(game, len(game.available_moves()), -math.inf, math.inf, True, 'O')['position']
            if square is None:
                print("\nGame is a draw!")
                break
            game.make_move(square, letter)
            print(f"\nAI (O) chooses square {square + 1}")
        else:
            valid_square = False
            while not valid_square:
                square = input(f"\n{letter}'s turn. Input move (1-9): ")
                try:
                    square = int(square) - 1
                    if square not in game.available_moves():
                        raise ValueError
                    valid_square = True
                    game.make_move(square, letter)
                except ValueError:
                    print("\nInvalid square. Try again.")

        game.print_board()

        if game.current_winner:
            print(f"\n{letter} wins!")
            break

        letter = 'O' if letter == 'X' else 'X'  # Switch turns.
    else:
        print("\nIt's a draw!")

def play_game_human_vs_human():

    game = TicTacToe()
    print("\nInitial Board:")
    game.print_board()

    letter = 'O'  # Human (O) player starts first.
    while game.empty_squares_available():
        if letter == 'O':  # Human (O)'s turn
            valid_square = False
            while not valid_square:
                square = input(f"\n{letter}'s turn. Input move (1-9): ")
                try:
                    square = int(square) - 1
                    if square not in game.available_moves():
                        raise ValueError
                    valid_square = True
                    game.make_move(square, letter)
                except ValueError:
                    print("\nInvalid square. Try again.")

                if square is None:
                    print("\nGame is a draw!")
                    break
                game.make_move(square, letter)
                print(f"\nAI (O) chooses square {square + 1}")
        else:
            valid_square = False
            while not valid_square:
                square = input(f"\n{letter}'s turn. Input move (1-9): ")
                try:
                    square = int(square) - 1
                    if square not in game.available_moves():
                        raise ValueError
                    valid_square = True
                    game.make_move(square, letter)
                except ValueError:
                    print("\nInvalid square. Try again.")

        game.print_board()

        if game.current_winner:
            print(f"\n{letter} wins!")
            break

        letter = 'O' if letter == 'X' else 'X'  # Switch turns.
    else:
        print("\nIt's a draw!")

def play_game_ai_vs_ai():

    game = TicTacToe()
    print("\nInitial Board:")
    game.print_board()

    first_move = True

    letter = 'O'  # AI (O) player starts first.
    while game.empty_squares_available():
        if letter == 'O':  # AI (O)'s turn
            if first_move:
                square = random.randint(0, 8)
                first_move = False
            else:
                square = minimax_with_alpha_beta(game, len(game.available_moves()), -math.inf, math.inf, True, 'O')['position']
            if square is None:
                print("\nGame is a draw!")
                break
            game.make_move(square, letter)
            print(f"\nAI (O) chooses square {square + 1}")
            time.sleep(0.75)
        else:
            square = minimax_with_alpha_beta(game, len(game.available_moves()), -math.inf, math.inf, True, 'O')['position']
            if square is None:
                print("\nGame is a draw!")
                break
            game.make_move(square, letter)
            print(f"\nAI (X) chooses square {square + 1}")
            time.sleep(0.75)

        game.print_board()

        if game.current_winner:
            print(f"\n{letter} wins!")
            break

        letter = 'O' if letter == 'X' else 'X'  # Switch turns.
    else:
        print("\nIt's a draw!")


if __name__ == '__main__':

    print("""
Modes of play available:

    hh: Hooman vs. hooman
    ha: Hooman vs. AI
    ah: AI vs. Hooman - AI makes first move
    aa: AI vs. AI""")

    valid_move = False
    while not valid_move:
        mode = input("\nEnter preferred mode of play (e.g., aa): ")
        try:
            if mode not in ["hh", "ha", "ah", "aa"]:
                raise ValueError
            valid_move = True
            if mode == "hh":
                play_game_human_vs_human()
            elif mode == "ha":
                play_game_human_moves_first()
            elif mode == "ah":
                play_game_ai_moves_first()
            else:
                play_game_ai_vs_ai()
        except ValueError:
            print("\nInvalid option entered. Try again.")

