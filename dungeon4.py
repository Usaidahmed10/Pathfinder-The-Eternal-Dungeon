'''
Dungeon Version 4: Final version

Author: Usaid Ahmed
'''
import time

MAP_FILES = ['arcadia_map.txt', 'cave_map.txt', 'ghost_town_map.txt', 'midgaard_maptxt']
HELP_FILE = 'help.txt'

def load_map(map_file: str) -> list[list[str]]:
    """
    Loads a map from a file as a grid (list of lists)
    """
    with open (map_file, "r") as file:
        data = file.readlines()
    grid = []
    for line in data:
        row = []
        for character in line.strip():
            row.append(character)
        grid.append(row)
        
    return grid
    

def find_start(grid: list[list[str]]) -> list[int, int]:
    """
    Finds the starting position of the player on the map.
    """
    num_of_rows = len(grid)
    num_of_columns = len(grid[0])
    starting_position = []
    
    for i in range(num_of_rows):
        for j in range(num_of_columns):
            if grid[i][j] == "S":
                starting_position.append(i)
                starting_position.append(j)
                
    return starting_position
    

def get_command() -> str:
    """
    Gets a command from the user.
    """
    command = input("> ").strip()
    
    return command      


def display_map(grid: list[list[str]], player_position: list[int, int]) -> None:
    """
    Displays the map.
    """
    from copy import deepcopy
    new_map = deepcopy(grid)
    
    i = player_position[0]
    j = player_position[1]  
    new_map[i][j] = "@"
    
    start = "🏠"
    finish = "🏺"
    wall = "🧱"
    path = "🟢"
    player = "🧝"    
    
    for row in new_map:
        for character in row:
            if character == "S":
                print(start, end="")
            if character == "F":
                print(finish, end="")
            if character == "-":
                print(wall, end="")
            if character == "*":
                print(path, end="")
            if character == "@":
                print(player, end="")
        print()
        

def get_grid_size(grid: list[list[str]]) -> list[int, int]:
    """
    Returns the size of the grid.
    """
    grid_size = []
    num_of_rows = len(grid)
    num_of_columns = len(grid[0])
    grid_size.append(num_of_rows)
    grid_size.append(num_of_columns)
    
    return grid_size
    

def is_inside_grid(grid: list[list[str]], position: list[int, int]) -> bool:
    """
    Checks if a given position is valid (inside the grid).
    """
    inside_grid = False
    grid_rows, grid_cols = get_grid_size(grid)
    if 0 <= position[0] <= grid_rows-1:
        if 0 <= position[1] <= grid_cols-1:
            inside_grid = True
    return inside_grid
    

def look_around(grid: list[list[str]], player_position: list[int, int]) -> list:
    """
    Returns the allowed directions.
    """
    allowed_objects = ('S', 'F', '*')
    row = player_position[0]
    col = player_position[1]
    directions = []
    if is_inside_grid(grid, [row - 1, col]) and grid[row - 1][col] in allowed_objects:
        directions.append('north')
    if is_inside_grid(grid, [row + 1, col]) and grid[row + 1][col] in allowed_objects:
        directions.append('south')
    if is_inside_grid(grid, [row, col+1]) and grid[row][col+1] in allowed_objects:
        directions.append('east')
    if is_inside_grid(grid, [row, col-1]) and grid[row][col-1] in allowed_objects:
        directions.append('west')
    
    return(directions)
    
    
def move(direction: str, player_position: list[int, int], grid: list[list[str]]) -> bool:
    """
    Moves the player in the given direction.
    """
    
    if direction in look_around(grid, player_position):
        if direction == "north":
            player_position[0] = player_position[0] - 1
        if direction == "south":
            player_position[0] = player_position[0] + 1
        if direction == "east":
            player_position[1] = player_position[1] + 1
        if direction == "west":
            player_position[1] = player_position[1] - 1
        return True  
            
    else:
        return False
    
    
def check_finish(grid: list[list[str]], player_position: list[int, int]) -> bool:
    """
    Checks if the player has reached the exit.
    """
    i = player_position[0]
    j = player_position[1] 
    
    if grid[i][j] == "F":
        return True
    else:
        return False
    

def display_help() -> None:
    """
    Displays a list of commands.
    """
    with open(HELP_FILE, "r") as file:
        instructions = file.read()
    print(instructions)


def play_level(map_file: str) -> float:
    """
    Plays a single level and returns the time taken to complete it.
    """
    grid = load_map(map_file)
    position = find_start(grid)

    start_time = time.time()
    while not check_finish(grid, position):
        print(f"You can go {', '.join(look_around(grid, position))}.")
        command = get_command()
        if command == "escape":
            print("You chose to escape. Goodbye!")
            return -1
        elif command == "show map":
            display_map(grid, position)
        elif command.startswith("go "):
            direction = command.split()[1]
            if move(direction, position, grid):
                print(f"You moved {direction}.")
            else:
                print("There is no way there.")
        elif command == "help":
            display_help()
        else:
            print("Invalid command.")

    end_time = time.time()
    print("Congratulations! You have reached the exit.")
    return end_time - start_time

def main():
    """
    Main entry point for the game.
    """
    for level, map_file in enumerate(MAP_FILES, 1):
        print()
        map_name = map_file.replace("_", " ").replace("map.txt", "").title()
        print(f"Level {level}: {map_name}\n")
        display_help()
        print()
        time_taken = play_level(map_file)

        if time_taken == -1:
            break

        print(f"You completed the level in {time_taken:.2f} seconds.")

        if level < len(MAP_FILES):
            next_action = input("Do you want to proceed to the next level? (yes/no): ").strip().lower()
            if next_action != "yes":
                print("Thanks for playing! Goodbye!")
                break
    else:
        print("Congratulations! You completed all levels.")

if __name__ == '__main__':
    main()