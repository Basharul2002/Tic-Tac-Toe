from tkinter import *

root = Tk()
root.geometry("500x800")
root.title("Tic Tac Toe")
root.config(bg="#2c3e50")
root.resizable(0, 0)


# Center the window on the screen
window_width = 500
window_height = 800

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))

root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

frame1 = Frame(root, bg="#34495e")
frame1.pack(pady=20)
titleLabel = Label(frame1, text="Tic Tac Toe", font=("Arial", 30, "bold"), bg="#e67e22", fg="white", width=16, relief=RAISED, borderwidth=10)
titleLabel.grid(row=0, column=0, pady=10)

optionFrame = Frame(root, bg="#2c3e50")
optionFrame.pack(pady=20)

frame2 = Frame(root, bg="#34495e", relief=RIDGE, borderwidth=10)
frame2.pack()

board = {1: " ", 2: " ", 3: " ",
         4: " ", 5: " ", 6: " ",
         7: " ", 8: " ", 9: " "}

turn = "x"
game_end = False
mode = "singlePlayer"

def changeModeToSinglePlayer(): 
    global mode 
    mode = "singlePlayer"
    singlePlayerButton["bg"] = "#1abc9c"
    multiPlayerButton["bg"] = "#bdc3c7"
    restartGame()

def changeModeToMultiplayer():
    global mode 
    mode = "multiPlayer"
    multiPlayerButton["bg"] = "#1abc9c"
    singlePlayerButton["bg"] = "#bdc3c7"
    restartGame()

def updateBoard():
    for key in board.keys():
        buttons[key - 1]["text"] = board[key]

def checkForWin(player):
    winning_combinations = [
        [1, 2, 3], [4, 5, 6], [7, 8, 9],  # rows
        [1, 4, 7], [2, 5, 8], [3, 6, 9],  # columns
        [1, 5, 9], [3, 5, 7]  # diagonals
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
            return True
    return False

def checkForDraw():
    return all(value != " " for value in board.values())

def restartGame():
    global game_end
    game_end = False
    for button in buttons:
        button["text"] = " "
    for i in board.keys():
        board[i] = " "
    titleLabel.config(text="Tic Tac Toe")

def minimax(board, isMaximizing):
    if checkForWin("o"):
        return 1
    if checkForWin("x"):
        return -1
    if checkForDraw():
        return 0

    if isMaximizing:
        bestScore = -float('inf')
        for key in board.keys():
            if board[key] == " ":
                board[key] = "o"
                score = minimax(board, False)
                board[key] = " "
                bestScore = max(score, bestScore)
        return bestScore
    else:
        bestScore = float('inf')
        for key in board.keys():
            if board[key] == " ":
                board[key] = "x"
                score = minimax(board, True)
                board[key] = " "
                bestScore = min(score, bestScore)
        return bestScore

def playComputer():
    bestScore = -float('inf')
    bestMove = None
    for key in board.keys():
        if board[key] == " ":
            board[key] = "o"
            score = minimax(board, False)
            board[key] = " "
            if score > bestScore:
                bestScore = score
                bestMove = key
    if bestMove is not None:
        board[bestMove] = "o"

def play(event):
    global turn, game_end
    if game_end:
        return

    button = event.widget
    grid_info = button.grid_info()
    clicked = grid_info["row"] * 3 + grid_info["column"] + 1

    if board[clicked] == " ":
        if turn == "x":
            board[clicked] = turn
            updateBoard()
            if checkForWin(turn):
                titleLabel.config(text=f"{turn} wins!")
                game_end = True
            else:
                turn = "o"
                if mode == "singlePlayer":
                    playComputer()
                    updateBoard()
                    if checkForWin(turn):
                        titleLabel.config(text=f"{turn} wins!")
                        game_end = True
                    turn = "x"

        else:
            board[clicked] = turn
            updateBoard()
            if checkForWin(turn):
                titleLabel.config(text=f"{turn} wins!")
                game_end = True
            turn = "x"

        if checkForDraw() and not game_end:
            titleLabel.config(text="It's a Draw!")
            game_end = True

# UI setup
singlePlayerButton = Button(optionFrame, text="Single Player", width=13, height=2, font=("Arial", 15), bg="#1abc9c", relief=RAISED, borderwidth=5, command=changeModeToSinglePlayer)
singlePlayerButton.grid(row=0, column=0, padx=10, pady=5)

multiPlayerButton = Button(optionFrame, text="Multiplayer", width=13, height=2, font=("Arial", 15), bg="#bdc3c7", relief=RAISED, borderwidth=5, command=changeModeToMultiplayer)
multiPlayerButton.grid(row=0, column=1, padx=10, pady=5)

# Tic Tac Toe Board
buttons = []
for row in range(3):
    for col in range(3):
        button = Button(frame2, text=" ", width=4, height=2, font=("Arial", 30, "bold"), bg="#ecf0f1", relief=RAISED, borderwidth=8, fg="#2c3e50")
        button.grid(row=row, column=col, padx=5, pady=5)
        button.bind("<Button-1>", play)
        buttons.append(button)

root.mainloop()
