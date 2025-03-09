import json
import sys

'''If neede to create independent javascript file, use the following code 
but we integrated this whole code into html only using pyscript '''

def ConstBoard(board):
    board_str = ""
    for i in range(9):
        if board[i] == 0:
            board_str += "_ " + "\t"
        elif board[i] == -1:
            board_str += "X " + "\t"
        elif board[i] == 1:
            board_str += "O " + "\t"
        if (i + 1) % 3 == 0:
            board_str += "\n"
    return board_str

def User1Turn(board, pos):
    if board[pos-1] != 0:
        return False
    board[pos-1] = -1
    return True

def User2Turn(board, pos):
    if board[pos-1] != 0:
        return False
    board[pos-1] = 1
    return True

def UserTurn(board, sym, pos):
    if board[pos-1] != 0:
        return False
    if sym == 'X':
        board[pos-1] = -1
    else:
        board[pos-1] = 1
    return True

def analyseboard(board):
    cb = [[0,1,2], [3,4,5], [6,7,8],
          [0,3,6], [1,4,7], [2,5,8],
          [0,4,8], [2,4,6]]
    for i in range(8):
        if board[cb[i][0]] != 0 and board[cb[i][0]] == board[cb[i][1]] == board[cb[i][2]]:
            return board[cb[i][0]]
    return 0

def minmax(board, player):
    x = analyseboard(board)
    if x != 0:
        return x * player
    pos = -1
    value = -2  # least value (like INT_MIN)
    for i in range(9):
        if board[i] == 0:
            board[i] = player
            score = -minmax(board, -player)
            board[i] = 0
            if score > value:
                value = score
                pos = i
    if pos == -1:
        return 0
    return value

def CompTurn(board, sym):
    pos = -1
    if sym == 'O':
        value = -2
        for i in range(9):
            if board[i] == 0:
                board[i] = 1
                score = -minmax(board, -1)
                board[i] = 0
                if score > value:
                    value = score
                    pos = i
        board[pos] = 1
    else:
        value = -2
        for i in range(9):
            if board[i] == 0:
                board[i] = -1
                score = -minmax(board, 1)
                board[i] = 0
                if score > value:
                    value = score
                    pos = i
        board[pos] = -1

def main():
    """CLI version of the game."""
    choice = int(input("Enter 1 for Single-Player game or 2 for Multi-Player Game: \n"))
    board = [0] * 9
    if choice == 1:
        symbol = input("\nWhat do you want to choose X or O: ")
        compSymbol = 'O' if symbol == 'X' else 'X'
        print("\nComputer:", compSymbol, "Vs. You:", symbol)
        player = int(input("Enter 1 to play 1(st) or 2 to play 2(nd): "))
        for i in range(9):
            if analyseboard(board) != 0:
                break
            if (i + player) % 2 == 0:
                CompTurn(board, compSymbol)
            else:
                print(ConstBoard(board))
                pos = int(input(f"\nEnter {symbol}'s position [1-9]: "))
                UserTurn(board, symbol, pos)
        print(ConstBoard(board))
        res = analyseboard(board)
        if res == 0:
            print("Draw!")
        elif res == -1:
            print("You Won!" if symbol == 'X' else "You Lost :( !")
        else:
            print("You Lost :( !" if symbol == 'X' else "You Won!")
    elif choice == 2:
        for i in range(9):
            if analyseboard(board) != 0:
                break
            print(ConstBoard(board))
            if i % 2 == 0:
                pos = int(input("\nEnter X's position [1-9]: "))
                User1Turn(board, pos)
            else:
                pos = int(input("\nEnter O's position [1-9]: "))
                User2Turn(board, pos)
        print(ConstBoard(board))
        res = analyseboard(board)
        if res == 0:
            print("Draw!")
        elif res == -1:
            print("Player 1 Won!")
        else:
            print("Player 2 Won!")

# We store the game state in a global dictionary for the GUI version.
game_state = {}

def start_game():
    try:
        data = json.loads(sys.stdin.read())
    except Exception as e:
        data = {}
    mode = int(data.get("mode", 1))       # 1 = Single-Player, 2 = Multiplayer
    symbol = data.get("symbol", "X")        # User’s symbol
    board = [0] * 9
    game_state["board"] = board
    game_state["mode"] = mode
    game_state["player_symbol"] = symbol
    if mode == 1:
        game_state["compSymbol"] = 'O' if symbol == 'X' else 'X'
    else:
        game_state["compSymbol"] = None
        game_state["turn"] = "player1"   
    response = {"board": board, "next_player": symbol}
    print(json.dumps(response))
    sys.stdout.flush()

def make_move():
    data = json.loads(sys.stdin.read())
    pos = int(data.get("pos"))
    board = game_state.get("board", [0]*9)
    mode = game_state.get("mode", 1)
    symbol = game_state.get("player_symbol", "X")
    
    if board[pos-1] != 0:
        response = {"error": "Invalid Move", "board": board}
        print(json.dumps(response))
        sys.stdout.flush()
        return
    
    if mode == 1:
        UserTurn(board, symbol, pos)   # Player makes a move
        if analyseboard(board) == 0:     # If no win/draw, let computer move
            CompTurn(board, game_state["compSymbol"])
    else:
        turn = game_state.get("turn", "player1")
        if turn == "player1":
            if not User1Turn(board, pos):
                response = {"error": "Invalid Move", "board": board}
                print(json.dumps(response))
                sys.stdout.flush()
                return
            game_state["turn"] = "player2"
        else:
            if not User2Turn(board, pos):
                response = {"error": "Invalid Move", "board": board}
                print(json.dumps(response))
                sys.stdout.flush()
                return
            game_state["turn"] = "player1"
    
    response = {"board": board, "next_player": symbol}
    print(json.dumps(response))
    sys.stdout.flush()

def reset_game():
    board = [0] * 9
    game_state["board"] = board
    response = {"board": board, "next_player": game_state.get("player_symbol", "X")}
    print(json.dumps(response))
    sys.stdout.flush()

# --- DISPATCHER ---
# This block chooses which function to run.
if __name__ == "__main__":
    # If running interactively (from terminal), sys.stdin.isatty() is True: run CLI.
    if sys.stdin.isatty():
        main()
    else:
        # When called by the GUI, I expect JSON input with an "action" field.
        try:
            data = json.loads(sys.stdin.read())
            action = data.get("action", "start")
        except Exception as e:
            action = "start"
        # Depending on the action, I am call the appropriate function.
        if action == "start":
            start_game()
        elif action == "move":
            make_move()
        elif action == "reset":
            reset_game()
