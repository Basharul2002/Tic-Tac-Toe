from tkinter import *

# Initialize the main application window
root = Tk()
root.geometry("500x800")   # Set the window size
root.title("Tic Tac Toe")  # Set the window title
root.config(bg="#2c3e50")  # Set the background color
root.resizable(0, 0)       # Disable window resizing

# Center the window on the screen
window_width = 500
window_height = 800

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the coordinates to center the window
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))

# Apply the calculated geometry to the window
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Frame for the title
frame1 = Frame(root, bg="#34495e")
frame1.pack(pady=20)

# Title label for the game
titleLabel = Label(frame1, text="Tic Tac Toe", font=("Arial", 30, "bold"), bg="#e67e22", fg="white", width=16, relief=RAISED, borderwidth=10)
titleLabel.grid(row=0, column=0, pady=10)

# Frame for option buttons
optionFrame = Frame(root, bg="#2c3e50")
optionFrame.pack(pady=20)

# Frame for difficulty selection
difficulty_frame = Frame(optionFrame, bg="#2c3e50")
difficulty_frame.grid(row=1, column=0, columnspan=2, pady=10)

# Label for difficulty selection
difficulty_label = Label(difficulty_frame, text="Select Difficulty:", font=("Arial", 15), bg="#2c3e50", fg="white")
difficulty_label.pack(side=LEFT)

# Variable to hold the difficulty level
difficulty_level = StringVar(value="1")  # Default difficulty level

# Dropdown menu for selecting difficulty level
difficulty_menu = OptionMenu(difficulty_frame, difficulty_level, "1", "2", "3", "4", "5")
difficulty_menu.config(font=("Arial", 15))
difficulty_menu.pack(side=LEFT)

# Frame for the Tic Tac Toe board
frame2 = Frame(root, bg="#34495e", relief=RIDGE, borderwidth=10)
frame2.pack()

# Dictionary to represent the game board
board = {1: " ", 2: " ", 3: " ",
         4: " ", 5: " ", 6: " ",
         7: " ", 8: " ", 9: " "}

turn = "x" # Variable to track the current player's turn
game_end = False # Flag to check if the game has ended
mode = 1 # Variable to determine the game mode (single player or multiplayer)

# Function to change to single-player mode
def changeModeToSinglePlayer(): 
    global mode 
    mode = 1 # Set mode to single player
    singlePlayerButton["bg"] = "#1abc9c"
    multiPlayerButton["bg"] = "#bdc3c7"
    difficulty_label.pack(side=LEFT)  # Show difficulty label
    difficulty_menu.pack(side=LEFT)  # Show difficulty menu
    restartGame()  # Restart the game
 
# Function to change to multiplayer mode
def changeModeToMultiplayer():
    global mode 
    mode = 2 # Set mode to multiplayer
    multiPlayerButton["bg"] = "#1abc9c" # Highlight multiplayer button
    singlePlayerButton["bg"] = "#bdc3c7" # Reset single player button color
    difficulty_label.pack_forget()  # Hide difficulty label
    difficulty_menu.pack_forget()  # Hide difficulty menu
    restartGame() # Restart the game

# Function to update the board UI based on the game state
def updateBoard():
    for key in board.keys():
        buttons[key - 1]["text"] = board[key] # Update button text

# Function to check if a player has won
def checkForWin(player):
    winning_combinations = [
        [1, 2, 3], [4, 5, 6], [7, 8, 9],  # rows
        [1, 4, 7], [2, 5, 8], [3, 6, 9],  # columns
        [1, 5, 9], [3, 5, 7]  # diagonals
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
            return True # Winning combination found
    return False # No winning combination found


# Function to check if the game has ended in a draw
def checkForDraw():
    return all(value != " " for value in board.values())  # All spaces filled

# Function to restart the game
def restartGame():
    global game_end
    game_end = False # Reset game end flag
    for button in buttons:
        button["text"] = " "  # Clear button text
    for i in board.keys():
        board[i] = " " # Reset board
    titleLabel.config(text="Tic Tac Toe") # Reset title


# Minimax algorithm for optimal move selection for the computer
def minimax(board, isMaximizing):
    if checkForWin("o"): 
        return 1 # Computer wins
    if checkForWin("x"):
        return -1 # Player wins
    if checkForDraw():
        return 0 # Draw

    if isMaximizing:
        bestScore = -float('inf')
        for key in board.keys():
            if board[key] == " ":
                board[key] = "o" # Computer's turn
                score = minimax(board, False) # Minimax call
                board[key] = " "  # Undo move
                bestScore = max(score, bestScore) # Update best score
        return bestScore # Return best score for maximizing player
    else:
        bestScore = float('inf')
        for key in board.keys():
            if board[key] == " ":
                board[key] = "x"  # Player's turn
                score = minimax(board, True) # Minimax call
                board[key] = " " # Undo move
                bestScore = min(score, bestScore) # Update best score
        return bestScore # Return best score for minimizing player

# Function for computer to play its turn
def playComputer():
    level = int(difficulty_level.get()) # Get selected difficulty level
    bestScore = -float('inf')
    bestMove = None
    
    # If level is 1, random move; higher levels make smarter choices
    for key in board.keys():
        if board[key] == " ":
            board[key] = "o" # Try move for computer
            score = minimax(board, False) if level > 1 else 0
            board[key] = " "
            if (level > 1 and score > bestScore) or (level == 1 and score >= 0): # Update best move based on score
                bestScore = score # Undo move
                bestMove = key
    
    # Make the best move found         
    if bestMove is not None:
        board[bestMove] = "o"

# Function to handle player moves
def play(event):
    global turn, game_end
    if game_end: # If game has ended, do nothing
        return

    button = event.widget # Get the clicked button
    grid_info = button.grid_info() # Get grid information
    clicked = grid_info["row"] * 3 + grid_info["column"] + 1  # Calculate clicked position

    if board[clicked] == " ": # Check if the space is empty
        if turn == "x": # Player's turn (X)
            board[clicked] = turn # Update board
            updateBoard() # Update UI
            if checkForWin(turn): # Check for win
                titleLabel.config(text=f"{turn} wins!") # Update title
                game_end = True # End the game
            else:
                turn = "o" # Switch turn to computer
                if mode == 1:
                    playComputer() # Computer makes a move
                    updateBoard() # Update UI
                    if checkForWin(turn):  # Check for win
                        titleLabel.config(text=f"{turn} wins!") # Update title
                        game_end = True # End the game
                    turn = "x" # Switch back to player

        else: # Computer's turn (O)
            board[clicked] = turn # Update board
            updateBoard() # Update UI
            if checkForWin(turn):  # Check for win
                titleLabel.config(text=f"{turn} wins!") # Update title
                game_end = True # End the game
            turn = "x" # Switch turn to player


        # Check for draw
        if checkForDraw() and not game_end:
            titleLabel.config(text="It's a Draw!") # Update title
            game_end = True # End the game

# UI setup
# Button for single player mode
singlePlayerButton = Button(optionFrame, text="Single Player", width=13, height=2, font=("Arial", 15), bg="#1abc9c", relief=RAISED, borderwidth=5, command=changeModeToSinglePlayer)
singlePlayerButton.grid(row=0, column=0, padx=10, pady=5)

# Button for multiplayer mode
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

root.mainloop() # Start the application

