import tkinter as tk
from tkinter import messagebox
import random

# Global variables for ship placement
player_ships = []
selected_ship_type = ""
selected_orientation = "horizontal"
player_grid = []
computer_grid = []
ship_counts = {"porte-avions": 1, "croiseur": 1, "destroyer": 2, "sous-marin": 2}
ship_lengths = {"porte-avions": 5, "croiseur": 4, "destroyer": 3, "sous-marin": 2}
computer_ships = []
sunk_ships_count = {"porte-avions": 0, "croiseur": 0, "destroyer": 0, "sous-marin": 0}

# Function to create the main window
def create_main_window():
    window = tk.Tk()
    window.title("Battleship Game")
    
    # Create the grids
    global player_grid, computer_grid
    player_grid = create_grid(window, "Player", 0)
    computer_grid = create_grid(window, "Computer", 1)
    
    # Create the control panel
    create_control_panel(window)
    
    # Initialize computer ships
    initialize_ships(computer_grid, player=False)
    
    return window

# Function to create a single grid
def create_grid(window, label_text, row):
    frame = tk.Frame(window)
    frame.grid(row=row, column=0, padx=10, pady=10)
    label = tk.Label(frame, text=label_text)
    label.grid(row=0, column=0, columnspan=10)

    buttons = []
    for i in range(10):
        row_buttons = []
        for j in range(10):
            if label_text == "Player":
                button = tk.Button(frame, width=2, height=1, bg="blue", command=lambda r=i, c=j: place_ship(r, c))
            else:
                button = tk.Button(frame, width=2, height=1, bg="blue", command=lambda r=i, c=j: player_turn(r, c))
            button.grid(row=i+1, column=j, padx=1, pady=1)
            row_buttons.append(button)
        buttons.append(row_buttons)
    
    return buttons

# Function to create the control panel
def create_control_panel(window):
    frame = tk.Frame(window)
    frame.grid(row=2, column=0, padx=10, pady=10)
    
    new_game_button = tk.Button(frame, text="New Game", command=new_game)
    new_game_button.grid(row=0, column=0, padx=5, pady=5)
    
    replay_button = tk.Button(frame, text="Replay", command=replay_game)
    replay_button.grid(row=0, column=1, padx=5, pady=5)
    
    global turn_indicator
    turn_indicator = tk.Label(frame, text="Player's Turn")
    turn_indicator.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
    
    # Ship selection
    ship_selection_label = tk.Label(frame, text="Select Ship Type:")
    ship_selection_label.grid(row=2, column=0, padx=5, pady=5)
    
    for ship_type in ship_counts:
        ship_button = tk.Button(frame, text=ship_type, command=lambda t=ship_type: select_ship(t))
        ship_button.grid(row=3, column=len(ship_counts)-len(ship_counts)+list(ship_counts.keys()).index(ship_type), padx=5, pady=5)
    
    # Orientation selection
    orientation_label = tk.Label(frame, text="Select Orientation:")
    orientation_label.grid(row=4, column=0, padx=5, pady=5)
    
    horizontal_button = tk.Button(frame, text="Horizontal", command=lambda: select_orientation("horizontal"))
    horizontal_button.grid(row=5, column=0, padx=5, pady=5)
    
    vertical_button = tk.Button(frame, text="Vertical", command=lambda: select_orientation("vertical"))
    vertical_button.grid(row=5, column=1, padx=5, pady=5)

    # Sunk ships display
    global sunk_ships_label
    sunk_ships_label = tk.Label(frame, text="Sunk Ships:\nPorte-avions: 0\nCroiseur: 0\nDestroyer: 0\nSous-marin: 0")
    sunk_ships_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Function to select a ship
def select_ship(ship_type):
    global selected_ship_type
    if ship_counts[ship_type] > 0:
        selected_ship_type = ship_type
        messagebox.showinfo("Ship Selection", f"Selected ship: {ship_type}")
    else:
        messagebox.showwarning("Warning", f"No more {ship_type}s left to place!")

# Function to select orientation
def select_orientation(orientation):
    global selected_orientation
    selected_orientation = orientation
    messagebox.showinfo("Orientation Selection", f"Selected orientation: {orientation}")

# Function to place ship on the player's grid
def place_ship(row, col):
    global player_ships, selected_ship_type, selected_orientation
    if selected_ship_type == "":
        messagebox.showwarning("Warning", "Select a ship type first!")
        return
    
    ship_length = ship_lengths[selected_ship_type]
    
    # Check if the ship can be placed
    if selected_orientation == "horizontal":
        if col + ship_length > 10 or any(player_grid[row][c]['bg'] != "blue" for c in range(col, col + ship_length)):
            messagebox.showwarning("Warning", "Cannot place ship here!")
            return
        for c in range(col, col + ship_length):
            player_grid[row][c].config(bg="grey")
            player_ships.append((row, c))
    else:
        if row + ship_length > 10 or any(player_grid[r][col]['bg'] != "blue" for r in range(row, row + ship_length)):
            messagebox.showwarning("Warning", "Cannot place ship here!")
            return
        for r in range(row, row + ship_length):
            player_grid[r][col].config(bg="grey")
            player_ships.append((r, col))
    
    ship_counts[selected_ship_type] -= 1  # Decrease the count of the selected ship type
    selected_ship_type = ""  # Reset the selected ship type

    if all(count == 0 for count in ship_counts.values()):
        messagebox.showinfo("Info", "All ships placed!")

# Function to initialize ship placement for the computer
def initialize_ships(grid, player):
    ship_counts_computer = {"porte-avions": 1, "croiseur": 1, "destroyer": 2, "sous-marin": 2}
    ships = []
    for ship_type, count in ship_counts_computer.items():
        for _ in range(count):
            length = ship_lengths[ship_type]
            placed = False
            while not placed:
                direction = random.choice(["horizontal", "vertical"])
                if direction == "horizontal":
                    row = random.randint(0, 9)
                    col = random.randint(0, 10 - length)
                    if all(grid[row][c]['bg'] == "blue" for c in range(col, col + length)):
                        for c in range(col, col + length):
                            if player:
                                grid[row][c].config(bg="grey")
                            ships.append((row, c, ship_type))
                        placed = True
                else:
                    row = random.randint(0, 10 - length)
                    col = random.randint(0, 9)
                    if all(grid[r][col]['bg'] == "blue" for r in range(row, row + length)):
                        for r in range(row, row + length):
                            if player:
                                grid[r][col].config(bg="grey")
                            ships.append((r, col, ship_type))
                        placed = True
    if not player:
        global computer_ships
        computer_ships = ships

# Function to reset the game
def reset_game():
    global player_ships, selected_ship_type, selected_orientation, ship_counts, player_grid, computer_grid, sunk_ships_count
    player_ships = []
    selected_ship_type = ""
    selected_orientation = "horizontal"
    ship_counts = {"porte-avions": 1, "croiseur": 1, "destroyer": 2, "sous-marin": 2}
    sunk_ships_count = {"porte-avions": 0, "croiseur": 0, "destroyer": 0, "sous-marin": 0}
    
    for row in player_grid:
        for button in row:
            button.config(bg="blue")
    
    for row in computer_grid:
        for button in row:
            button.config(bg="blue")
    
    initialize_ships(computer_grid, player=False)
    update_sunk_ships_label()

# Function to start a new game
def new_game():
    reset_game()
    messagebox.showinfo("New Game", "Start a new game!")

def player_turn(row, col):
    global computer_grid, computer_ships
    if (row, col) in [(x, y) for x, y, _ in computer_ships]:
        computer_grid[row][col].config(bg="red")
        ship_type = next(ship for x, y, ship in computer_ships if x == row and y == col)
        computer_ships = [(x, y, ship) for x, y, ship in computer_ships if not (x == row and y == col)]
        sunk_ships_count[ship_type] += 1
        update_sunk_ships_label()
        if not computer_ships:
            messagebox.showinfo("Game Over", "You win!")
            return
    else:
        computer_grid[row][col].config(bg="green")
    
    turn_indicator.config(text="Computer's Turn")
    window.after(1000, computer_turn)  # Wait 1 second before computer's turn

def computer_turn():
    global player_grid, player_ships
    row, col = random.randint(0, 9), random.randint(0, 9)
    while player_grid[row][col]['bg'] in ["red", "green"]:
        row, col = random.randint(0, 9), random.randint(0, 9)
    
    if player_grid[row][col]['bg'] == "grey":
        player_grid[row][col].config(bg="red")
        player_ships.remove((row, col))
        if not player_ships:
            messagebox.showinfo("Game Over", "Computer wins!")
            return
    else:
        player_grid[row][col].config(bg="green")
    
    turn_indicator.config(text="Player's Turn")

def update_sunk_ships_label():
    global sunk_ships_label, sunk_ships_count
    sunk_ships_label.config(text=f"Sunk Ships:\nPorte-avions: {sunk_ships_count['porte-avions']}\nCroiseur: {sunk_ships_count['croiseur']}\nDestroyer: {sunk_ships_count['destroyer']}\nSous-marin: {sunk_ships_count['sous-marin']}")

def replay_game():
    messagebox.showinfo("Replay Game", "Replay the game!")

# Main function to run the application
def main():
    global window
    window = create_main_window()
    window.mainloop()

if __name__ == "__main__":
    main()