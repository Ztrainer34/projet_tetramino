'''
Prénom : Zia
Nom: Gulzar
matricule:000595624
'''


import os
from getkey import getkey
import sys


def import_card(file_path: str):
    """
       Reads a file containing the dimensions of the grid and details for the different tetraminos which includes there
       initial coordinates and their colors


       Args:
       file_path (str): The path to the file containing tetramino configurations.

       Returns:
       tuple: A tuple where the first element is the dimensions of the grid and the second element is a list of tetraminos.
              Each tetramino is represented as a list containing coordinates, color, and initial position.
       """
    with open(file_path, 'r') as file:
        lines = file.readlines()
        dimensions = tuple(map(int, lines[0].split(','))) #methode that changes the dimenions from a string to a tuple

    tetramino = []
    for line in lines[1:]:
        if line.strip():
            cordonnees, couleur = map(str.strip, line.split(';;'))
            coords = [tuple(map(int, pair.strip('()').split(','))) for pair in cordonnees.split(';')] #methode that changes the initial coordinates from a string to a tuple
            color = couleur
            tetramino.append(([coords, color, (0, 0)]))

    return dimensions, tetramino





def create_grid(w: int, h: int):
    """
        Creates a grid of specified width and height.

        Args:
        w (int): The width of the grid.
        h (int): The height of the grid.

        Returns:
        list: A two-dimensional list representing the grid.
        """

    grid_width = 3 * w + 2#Formula of the width of the grid given in the instructions
    grid_height = 3 * h + 2#Formula of the height of the grid given in the instructions
    grid = [['  ' for i in range(grid_width)] for j in range(grid_height)]
    for i in range(w):
        grid[h][w+1+i] = "--" 
        grid[2*h+1][w+1+i] = "--"
    for i in range(h):
        grid[h+1+i][w] = " |"
        grid[h+1+i][(2*w)+1] = "| "

    return grid



def setup_tetraminos(tetraminos: list , grid: list):
    """
           Sets up tetraminos on the grid with their initial positions.

           Args:
           tetraminos (list): A list of tetraminos to set up.
           grid (list): The grid on which to set up the tetraminos.

           Returns:
           tuple: A tuple containing the updated grid and the tetraminos list with their new initial decalage.
           """
    offset = [(0, 0), (6, 0), (12, 0), (0, 5), (12, 5), (0, 10), (6, 16), (12, 16)]
    for i in range(len(tetraminos)):
        tetraminos[i][2] = offset[i]
        for coord in tetraminos[i][0]:
            x = coord[0] + tetraminos[i][2][0]
            y = coord[1] + tetraminos[i][2][1]

            grid[y][x] = f'\x1b[{tetraminos[i][1]}m{i + 1} \x1b[0m'
    return grid, tetraminos




def place_tetraminos(tetraminos: list , grid: list):
    """
        Places the tetraminos on the grid once a movement has been called by the player, initialize a new grid each time
        a movement of the tetraminos is called.

        Args:
        tetraminos (list): A list of tetraminos to place on the grid.
        grid (list): The grid on which to place the tetraminos.

        Returns:
        list: The updated grid with tetraminos placed and with their new decalage.
        """

    placed_correctly = True#laced_correctly is always True when the tetramino is in a valid position
    grid = create_grid((len(grid[0])-2)//3, (len(grid)-2)//3)
    for i in range(len(tetraminos)):

        for coord in tetraminos[i][0]:

            x = coord[0] + tetraminos[i][2][0]
            y = coord[1] + tetraminos[i][2][1]
            if grid[y][x] != ' '*2:
               placed_correctly = False # place_correctly turns false if it the tetramino is in a invalid position

               if not placed_correctly:#to mark the invalidity of the the tetramino a XX is placed on the problematique tetramino
                  inside_marker = "XX"
                  grid[y][x] = f'\x1b[{tetraminos[i][1]}m{inside_marker}\x1b[0m'
            else:
                grid[y][x] = f'\x1b[{tetraminos[i][1]}m{i+1} \x1b[0m'

    return grid


def rotate_tetramino(tetramino, clockwise : bool =True):
    """
        Rotates a single tetramino either clockwise or counter-clockwise.

        Args:
        tetramino: The tetramino to rotate.
        clockwise (bool, optional): Determines the direction of rotation. Defaults to True for clockwise rotation and
        False for the counter-clockwise rotation

        Returns:
        list: The rotated tetramino.
        """
    new_coords = []
    for coordinates in tetramino[0]:

        if clockwise:
            new_coords.append((-coordinates[1], coordinates[0]))
        else:
            new_coords.append((coordinates[1], -coordinates[0]))
    new_tetramino = [new_coords, tetramino[1], tetramino[2]]
    return new_tetramino


def verification(tetramino, grid):
    """
        Verifies if a tetramino is going out of bounds.

        Args:
        tetramino: The tetramino to verify.
        grid (list): The grid to verify against.

        Returns:
        bool: True if the tetramino is not going out of bounds so the tetramino can be placed, False otherwise which
        means it can not be placed.
        """
    for coord in tetramino[0]:
        x, y = coord[0] + tetramino[2][0], coord[1] + tetramino[2][1]
        if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
            return False
    return True
def check_move(tetramino, grid: list):
    """
        Checks if a tetramino is actually in a valid position or not.

        Args:
        tetramino: The tetramino to check.
        grid (list): The grid to check against.

        Returns:
        bool: True if the actual position of the tetramino is valid , otherwise False.
        """
    for coord in tetramino[0]:
        x, y = coord[0] + tetramino[2][0], coord[1] + tetramino[2][1]
        if "XX" in grid[y][x]:
            return False
    return True




def check_win(grid: list):
    """
        Checks if the game has been won, i.e., all the playable grid cells are filled.

        Args:
        grid (list): The grid to check for a win.

        Returns:
        bool: True if the game is won, False otherwise and the game continues.
        """
    playable_area_min_x = int((len(grid) - 2) / 3) + 1  # 5
    playable_area_min_y = int((len(grid[0]) - 2) / 3) + 1  # 6
    playable_area_max_x = 2 * playable_area_min_x - 2  # 8
    playable_area_max_y = 2 * playable_area_min_y - 2  # 10
    for i in range(playable_area_min_x, playable_area_max_x + 1):
        for j in range(playable_area_min_y, playable_area_max_y + 1):
            if grid[i][j] == ' ' * 2:
                return False

    return True


def print_grid(grid : list, no_number : bool):
    """
        Prints the current state of the grid, optionally omitting tetramino numbers and it also removes the number on
        the tetraminos while a single tetraminos is selected.

        Args:
        grid (list): The grid to be printed, where each sublist represents a row.
        no_number (bool, optional): If True, prints the grid without tetramino numbers. Defaults to False.
        """

    if os.name == 'posix':
       os.system('clear')
    else:
       os.system('cls')

       grid_width = len(grid[0])
       print('--' * (grid_width+1))

       for row in grid:
           new_row = []
           for cell in row:
               position_of_m = cell.find('m')
               if no_number and position_of_m >= 0:
                   new_cell = cell[:position_of_m+1] + ' ' + cell[position_of_m+2:]
                   new_row.append(new_cell)
               else:
                   new_row.append(cell)
           print('|' + ''.join(cell + '' for cell in new_row)[:-1] + ' |')
       print('--' * (grid_width + 1))


def main():
    """
        Main function to run the game. Handles game initialization, user input, and game loop.
        returns:
        bool: True if the game is won
        """
    if len(sys.argv) > 1:
        file_path= sys.argv[1]
    else:
        filename = "carte_1.txt"
        sys.exit(1)
    dimensions, tetramino = import_card(file_path)
    grid = create_grid(dimensions[0], dimensions[1])
    grid, tetramino = setup_tetraminos(tetramino, grid)
    print_grid(grid,False)

    while not check_win(grid): #verifies if the the grid is a winning if not the game continues

        print("enter the tetramino number")
        number = getkey()#user input for selecting a tetramino
        if number == '9':
            break
        elif number.isdigit() and 1 <= int(number) <= 8:
            play = int(number) - 1

            hide_numbers = False
            while True:
                hide_numbers = True
                print("enter direction, rotation or validate your position")
                try:# user input for the movement
                    key = getkey().decode('utf-8')
                except AttributeError:# ensure that this code can be run on mac or linux
                    key = getkey()
                if key == 'v' and check_move(tetramino[play], grid):
                    print_grid(grid, False)
                    break
                elif key == 'i': #moving the tetramino upwards
                    new_coord = (tetramino[play][2][0], tetramino[play][2][1] - 1)
                    tetramino[play][2] = new_coord
                    ok = verification(tetramino[play], grid)
                    if ok:#verifies if the grid is not out of bounds
                        grid = place_tetraminos(tetramino, grid)
                    else:
                        tetramino[play][2] = (tetramino[play][2][0], tetramino[play][2][1] + 1)
                elif key == 'j':#moving the tetramino left
                    new_coord = (tetramino[play][2][0] - 1, tetramino[play][2][1])
                    tetramino[play][2] = new_coord
                    ok = verification(tetramino[play], grid)
                    if ok:
                        grid = place_tetraminos(tetramino, grid)
                    else:
                        tetramino[play][2] = (tetramino[play][2][0] + 1, tetramino[play][2][1])
                elif key == 'k':#moving the tetramino downwards
                    new_coord = (tetramino[play][2][0], tetramino[play][2][1] + 1)
                    tetramino[play][2] = new_coord
                    ok = verification(tetramino[play], grid)
                    if ok:
                        grid = place_tetraminos(tetramino, grid)
                    else:
                        tetramino[play][2] = (tetramino[play][2][0], tetramino[play][2][1] - 1)
                elif key == 'l':#moving the tetramino right
                    new_coord = (tetramino[play][2][0] + 1, tetramino[play][2][1])
                    tetramino[play][2] = new_coord
                    ok = verification(tetramino[play], grid)
                    if ok:
                        grid = place_tetraminos(tetramino, grid)
                    else:
                        tetramino[play][2] = (tetramino[play][2][0] - 1, tetramino[play][2][1])
                elif key == 'o':# clockwise roation
                    sauvegarder = rotate_tetramino(tetramino[play], True)
                    ok = verification(tetramino[play], grid)
                    if ok:
                        tetramino[play] = sauvegarder
                        grid = place_tetraminos(tetramino, grid)
                elif key == 'u':#anticlockwise rotation
                    sauvegarder = rotate_tetramino(tetramino[play], False)
                    ok = verification(tetramino[play], grid)
                    if ok:
                        tetramino[play] = sauvegarder
                        grid = place_tetraminos(tetramino, grid)
                print_grid(grid, True)
    if check_win(grid):# gives the winning message if the game is won
        print_grid(grid, True)
        print("Congratulations! You have successfully completed the game!")
        return True

if __name__ == '__main__':
   main()
