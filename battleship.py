"CS 021 ALEX CARPENTER, BATTLESHIP FINAL PROJECT"
import random
import time

CARRIER_SIZE     = 5
BATTLESHIP_SIZE  = 4
DESTROYER_SIZE   = 3
SUBMARINE_SIZE   = 3
PATROL_BOAT_SIZE = 2
MIN_ROW          = 0
MIN_COL          = 9
MAX_ROW          = 9
MAX_COL          = 9

def setup_board():
    ocean_board = [[]]

    # Ocean board starts with just 10 blank rows
    ocean_board = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
    
    return ocean_board


def randomize_placement(board, size):
    # Decrement the size by 1 to incorporate start position
    size -= 1

    # Randomize the starting location
    start_row_index = random.randint(0, 9)
    start_col_index = random.randint(0, 9)

    # Randomly choose either vertical or horizontal placement
    is_vertical = random.randint(0, 1)

    # Compute the ending row or column
    # Ensure we don't place the ship out of bounds of the board
    if is_vertical == True:
        end_col_index = start_col_index
        if start_row_index + size <= MAX_ROW:
            end_row_index = start_row_index + size
        else:
            end_row_index = start_row_index
            start_row_index = end_row_index - size
    else:
        end_row_index = start_row_index
        if start_col_index + size <= MAX_COL:
            end_col_index = start_col_index + size
        else:
            end_col_index = start_col_index
            start_col_index = end_col_index - size

    return start_col_index, start_row_index, end_col_index, end_row_index


def setup_opponent():
    # Hits is a dictionary with keys as the opponent ship abbreviation and value as size
    # which will decrement each time the opponent ship is hit
    hits = {'C': CARRIER_SIZE, 'B': BATTLESHIP_SIZE, 'D': DESTROYER_SIZE,
            'S': SUBMARINE_SIZE, 'P': PATROL_BOAT_SIZE}
    opponent_hits = {'C': CARRIER_SIZE, 'B': BATTLESHIP_SIZE, 'D': DESTROYER_SIZE,
                     'S': SUBMARINE_SIZE, 'P': PATROL_BOAT_SIZE}
    
    # Opponent board starts with just 10 blank rows
    opponent_board = [[]]
    opponent_board = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
    
    opponent_firing_board = [[]]
    opponent_firing_board = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]

    # Now randomize the opponent's ship positions and place ships.
    start_col_index, start_row_index, end_col_index, end_row_index = randomize_placement(opponent_board, CARRIER_SIZE)
    place_ship(opponent_board, 'C',
               start_col_index, start_row_index, end_col_index, end_row_index)

    # Assume a collision will happen with the 2nd ship.
    collision = True
    while collision == True:
        start_col_index, start_row_index, end_col_index, end_row_index = randomize_placement(opponent_board, BATTLESHIP_SIZE)
        collision = collision_check(opponent_board, start_row_index, end_row_index, start_col_index, end_col_index)

    place_ship(opponent_board, 'B',
               start_col_index, start_row_index, end_col_index, end_row_index)

    collision = True
    while collision == True:
        start_col_index, start_row_index, end_col_index, end_row_index = randomize_placement(opponent_board, DESTROYER_SIZE)
        collision = collision_check(opponent_board, start_row_index, end_row_index, start_col_index, end_col_index)
        
    place_ship(opponent_board, 'D',
               start_col_index, start_row_index, end_col_index, end_row_index)

    collision = True
    while collision == True:
        start_col_index, start_row_index, end_col_index, end_row_index = randomize_placement(opponent_board, SUBMARINE_SIZE)
        collision = collision_check(opponent_board, start_row_index, end_row_index, start_col_index, end_col_index)

    place_ship(opponent_board, 'S',
               start_col_index, start_row_index, end_col_index, end_row_index)

    collision = True
    while collision == True:
        start_col_index, start_row_index, end_col_index, end_row_index = randomize_placement(opponent_board, PATROL_BOAT_SIZE)
        collision = collision_check(opponent_board, start_row_index, end_row_index, start_col_index, end_col_index)

    place_ship(opponent_board, 'P',
               start_col_index, start_row_index, end_col_index, end_row_index)

    return opponent_board, opponent_firing_board, hits, opponent_hits


def display_board(board):
    # Displaying o (ocean) board
    o = board

    print('      A    B    C    D    E    F    G    H    I    J')
    print('------------------------------------------------------')
    print(' 1', end = '')
    for i in range(0, 10):
        print(f"{o[0][i]: >5}", end = '')

    print('\n 2', end = '')
    for i in range(0, 10):
        print(f"{o[1][i]: >5}", end = '')

    print('\n 3', end = '')
    for i in range(0, 10):
        print(f"{o[2][i]: >5}", end = '')

    print('\n 4', end = '')
    for i in range(0, 10):
        print(f"{o[3][i]: >5}", end = '')

    print('\n 5', end = '')
    for i in range(0, 10):
        print(f"{o[4][i]: >5}", end = '')

    print('\n 6', end = '')
    for i in range(0, 10):
        print(f"{o[5][i]: >5}", end = '')

    print('\n 7', end = '')
    for i in range(0, 10):
        print(f"{o[6][i]: >5}", end = '')

    print('\n 8', end = '')
    for i in range(0, 10):
        print(f"{o[7][i]: >5}", end = '')

    print('\n 9', end = '')
    for i in range(0, 10):
        print(f"{o[8][i]: >5}", end = '')
    
    print('\n10', end = '')
    for i in range(0, 10):
        print(f"{o[9][i]: >5}", end = '')
        
    print('\n')


def display_ship_classes():
    print("You have 5 ships as follows:\n")
    print(f'CLASS                 SIZE')
    print('Carrier               5')
    print('Battleship            4')
    print('Destroyer             3')
    print('Submarine             3')
    print('Patrol Boat           2\n')


def display_menu():

    print('\nMenu:')
    print('C    Place Carrier')
    print('B    Place Battleship')
    print('D    Place Destroyer')
    print('S    Place Submarine')
    print('P    Place Patrol Boat')
    print('O    View Ocean Board')
    print('F    View Firing Board')
    print('T    Target Shot')
    print('Q    Quit Game\n')


def validate_starting_position(board, column, row):
    # Convert row and column to list indices
    column_index = ord(column) - 65
    row_index = row - 1
    
    if ord(column) < 65 or ord(column) > 74:
        print('\nInvalid position, must between A1 and J10, try again\n')
        return False
    elif row < 1 or row > 10:
        print('\nInvalid position, must between A1 and J10, try again\n')
        return False
    elif board[row_index][column_index] != ' ':
        print('\nInvalid position, collides with other ship\n')
        return False
    else:
        return True


def collision_check(board, start_row, end_row, start_column, end_column):
    if start_column == end_column:
        # Check for collisions
        for i in range(start_row, end_row+1):
            if board[i][start_column] != ' ':
                return True
    else:
        # Check for collisions
        for i in range(start_column, end_column+1):
            if board[start_row][i] != ' ':
                return True

    return False


def validate_ending_position(board, start_row, end_row, start_column, end_column, size):
    start_column = ord(start_column) - 65
    end_column   = ord(end_column) - 65
    start_row = start_row - 1
    end_row   = end_row - 1


    if end_column < 0 or end_column > MAX_COL:
        print('\nInvalid position, must between A1 and J10, try again\n')
        return False
    elif end_row < 0 or end_row > MAX_ROW:
        print('\nInvalid position, must between A1 and J10, try again\n')
        return False
    elif end_row < start_row:
        print('\nInvalid, end row must be >= start row, try again\n')
        return False
    elif end_column < start_column:
        print('\nInvalid, end column must be >= start column, try again\n')
        return False
    elif end_column != start_column and end_row != start_row:
        print('\nInvalid, cannot be placed diagonally, try again\n')
        return False
    elif start_column == end_column:
        if (end_row - start_row) != size - 1:
            print(f'\nInvalid position, must be size {size}, try again\n')
            return False
        else:
            # Check for collisions
            if collision_check(board, start_row, end_row, start_column, end_column) == True:
                print('\nInvalid position, collides with other ship\n')
                return False
    elif start_row == end_row:
        if abs(start_column - end_column)!= size - 1:
            print('\nInvalid ending position, try again\n')
            return False
        else:
            # Check for collisions
            if collision_check(board, start_row, end_row, start_column, end_column) == True:
                print('\nInvalid position, collides with other ship\n')
                return False
    else:
        return True
    
    return True


def place_ship(board, ship_abbrev, start_column_index, start_row_index, end_column_index, end_row_index):

    # Ship placed horizontally in same row
    if start_row_index == end_row_index:
        if start_column_index < end_column_index:
            for i in range(start_column_index, end_column_index + 1):
                board[start_row_index][i] = ship_abbrev
        else:
            for i in range(start_column_index, end_column_index - 1, -1):
                board[start_row_index][i] = ship_abbrev            

    # Ship placed vertically in same column
    else:
        if start_row_index < end_row_index:
            for i in range(start_row_index, end_row_index + 1):
                board[i][start_column_index] = ship_abbrev
        else:
            for i in range(start_row_index, end_row_index - 1, -1):
                board[i][start_column_index] = ship_abbrev


def query_and_place_ship(board, ship_abbrev, ships):
    match ship_abbrev:
        case 'C':
            ship = 'Carrier (size 5)'
            size = CARRIER_SIZE
        case 'B':
            ship = 'Battleship (size 4)'
            size = BATTLESHIP_SIZE
        case 'D':
            ship = 'Destroyer (size 3)'
            size = DESTROYER_SIZE
        case 'S':
            ship = 'Submarine (size 3)'
            size = SUBMARINE_SIZE
        case 'P':
            ship = 'Patrol Boat (size 2)'
            size = PATROL_BOAT_SIZE

    valid = False
    while valid == False:
        start = input(f'Place {ship} starting position: ')
        start_column = start[0].capitalize()
        try:
            start_row = int(start[1:])
        except ValueError:
            print('\nInvalid position, must between A1 and J10, try again')
            continue
        
        # Validate starting position
        valid = validate_starting_position(board, start_column, start_row)
        if valid == False:
            continue

        end   = input(f'Place {ship} ending position: ')
        end_column = end[0].capitalize()
        try:
            end_row = int(end[1:])
        except ValueError:
            print('\nInvalid position, must between A1 and J10, try again')
            continue

        # Validate ending position
        valid = validate_ending_position(board, start_row, end_row, start_column, end_column, size)

    # Place in Ocean Board
    # Note that ord('A') = 65
    start_column_index = ord(start_column) - 65
    end_column_index = ord(end_column) - 65
    start_row_index = start_row - 1
    end_row_index = end_row - 1
    
    place_ship(board, ship_abbrev, start_column_index, start_row_index, end_column_index, end_row_index)
    
    # Append ship placements in dictionary as follows:
    # [start_row, start_column, end_row, end_column]
    ships[ship_abbrev].append(start_row_index)
    ships[ship_abbrev].append(start_column_index)
    ships[ship_abbrev].append(end_row_index)
    ships[ship_abbrev].append(end_column_index)

    print(f'\nYour {ship} is placed in position {start}-{end}\n')
    return True


def check_win(hits):
    results = 0
    for v in hits.values():
        results = results + v

    if results == 0:
        return True
    else:
        return False


def find_target(board):
    found_hit    = False
    is_vertical  = False

    # PRECISION MODE
    # Some AI to make the computer intelligent about finding a target.
    # Determine target position by searching for a hit H and firing
    # at a neighboring row or column.
    for row in range(0, MAX_ROW + 1):
        for col in range(0, MAX_COL + 1):
            # Found a hit, check if vertical or horizontal
            if board[row][col] == 'H':
                found_hit = True
                print('\nFound a hit\n')
                # Now let's see if this ship is vertical
                target_row_up   = row + 1
                target_row_down = row - 1
                target_col = col
                if target_row_up <= MAX_ROW and board[target_row_up][target_col] == 'H':
                    print('\nWe have a vertical ship\n')
                    is_vertical = True
                elif target_row_down >= 0 and board[target_row_down][target_col] == 'H':
                    print('\nWe have a vertical ship\n')
                    is_vertical = True
                else:
                    print('\nWe guess a horizontal ship\n')
                    is_vertical = False

            # Assuming horizontal, try one column right from last hit
            elif found_hit == True and is_vertical == False and board[row][col] == ' ':
                target_row = row
                target_col = col
                print('\nFound horizontal target by moving right\n')
                return target_row, target_col

            # Found a hit and a neighboring miss
            elif found_hit == True and board[row][col] == 'M':
                # Assume horizontal placement and try the other direction (move left)
                # by decrementing the column number
                target_col = col - 1
                target_row = row
                while target_col >= 0 and is_vertical == False:
                    if board[target_row][target_col] == 'H':
                        target_col = target_col - 1
                    elif board[target_row][target_col] == ' ':
                        # Found a target
                        print('\nFound horizontal target by moving left\n')
                        return target_row, target_col
                    elif board[target_row][target_col] == 'M':
                        # No more hits on this row.
                        # Break out of this while loop and try vertical placement
                        print('\nNo more hits on this row, try vertical placement\n')
                        is_vertical = True
                        break

                # If trying vertical placement, move down first until we find a miss.
                # If we find a miss, switch direcions, move up and look for an empty slot.
                target_row = row + 1
                target_col = col - 1
                move_down = True # Try moving down first
                while target_row >= 0 and target_row <= MAX_ROW and target_col >= 0:
                    # Found a hit so move down a row unless we reversed direction
                    if board[target_row][target_col] == 'H':
                        print('\nFound a hit in vertical direction\n')
                        pass
                    # Found a miss so switch directions (move up)
                    elif board[target_row][target_col] == 'M':
                        move_down = False
                    elif board[target_row][target_col] == ' ':
                        # Found a target
                        print('\nFound vertical target\n')
                        return target_row, target_col
                    else:
                        break

                    if move_down == True:
                        print('\nMove down\n')
                        target_row = target_row + 1
                    else:
                        print('\nMove up\n')
                        target_row = target_row - 1

    # RANDOM MODE
    # Didn't find an X, so fire random shot.
    found_empty_target = False
    while found_empty_target == False:
        # Generate new random position
        target_row = random.randint(0, 9)
        target_col = random.randint(0, 9)
        print(target_row, target_col)
        if board[target_row][target_col] == ' ':
            print('\nFound random target\n')
            found_empty_target = True
            
    return target_row, target_col


def opponent_shot(user_board, opponent_firing_board, opponent_hits, ship_positions):
    ships = {'C': 'Carrier', 'B': 'Battleship', 'D': 'Destroyer', 'S': 'Submarine', 'P': 'Patrol Boat'}

    print('\nOpponent firing shot...')
    time.sleep(1)

    u  = user_board
    of = opponent_firing_board

    target_row, target_col = find_target(of)

    # Fire shot and mark board appropriately
    ship = u[target_row][target_col]
    # Hit!
    if ship in ships:
        u[target_row][target_col] = 'X'
        of[target_row][target_col] = 'H'
        opponent_hits[ship] -= 1
        if opponent_hits[ship] <= 0:
            print(f'Opponent sunk your {ships[ship]}!\n')

            # Pop ship position from dictonary
            start_row = ship_positions[ship].pop(0)
            start_col = ship_positions[ship].pop(0)
            end_row   = ship_positions[ship].pop(0)
            end_col   = ship_positions[ship].pop(0)

            print(start_row, start_col, end_row, end_col)

            # Now mark of board with the letter instead of 'H'
            if start_col == end_col:
                for i in range(start_row, end_row + 1):
                    of[i][start_col] = ship
            else:
                for i in range(start_col, end_col + 1):
                    of[start_row][i] = ship                
            
        else:
            print(f'\nOpponent hit your {ships[ship]}!\n')

        display_board(user_board)
        if check_win(opponent_hits) == True:
            print(f'OPPONENT WINS (sunk all your ships)!!!\n')
            time.sleep(2)
            exit()

    # Miss!
    else:
        of[target_row][target_col] = 'M'
        print('\nOpponent missed!\n')
        print(f'Opponent fired at column {target_col}, row {target_row}\n')


def target_shot(board, firing_board, hits):
    ships = {'C': 'Carrier', 'B': 'Battleship', 'D': 'Destroyer', 'S': 'Submarine', 'P': 'Patrol Boat'}

    # Validate input first
    valid = False
    while valid == False:
        target = input(f'\nFire shot at opponent position: ')
        target_column = target[0].capitalize()
        try:
            target_row = int(target[1:])
            target_column_index = ord(target_column) - 65
            target_row_index = target_row - 1
            if target_column_index > MAX_COL or target_column_index < 0:
                print('\nInvalid position, must between A1 and J10, try again')
                valid = False
            elif target_row_index > MAX_ROW or target_row_index < 0:
                print('\nInvalid position, must between A1 and J10, try again')
                valid = False
            else:
                valid = True
        except ValueError:
            print('\nInvalid position, must between A1 and J10, try again')
            continue


    # Did shot hit or miss the opponent?
    # If shot hit, mark both the firing board and opponent's board position with an X
    ship = board[target_row_index][target_column_index]
    if ship == 'H':
        print("\nYou already hit a ship at this position")
        print('\nFIRING BOARD')
        print('H: Hit, M: Miss\n')
        display_board(firing_board)
    elif ship == 'M':
        print("\nYou already missed a ship at this position")
        print('\nFIRING BOARD')
        print('H: Hit, M: Miss\n')
        display_board(firing_board)        
    elif ship != ' ':
        board[target_row_index][target_column_index] = 'H'
        firing_board[target_row_index][target_column_index] = 'H'
        print("\nTarget HIT!")
        print('\nFIRING BOARD')
        print('H: Hit, M: Miss\n')
        display_board(firing_board)
        hits[ship] -= 1
        if hits[ship] <= 0:
            print(f'You sunk my {ships[ship]}!\n')
        if check_win(hits) == True:
            print(f'YOU WIN (sunk all ships)!!!\n')
            time.sleep(2)
            exit()
    else:
        board[target_row_index][target_column_index] = 'M'
        firing_board[target_row_index][target_column_index] = 'M'
        print("\nTarget miss!")
        print('\nFIRING BOARD')
        print('H: Hit, M: Miss\n')
        display_board(firing_board)


if __name__ == '__main__':
    
    print("                         Welcome to BATTLESHIP!")
    print('\n')
    print('                                     |__')
    print('                                     |\/')
    print('                                     ---')
    print('                                     / | [')
    print('                              !      | |||')
    print('                            _/|     _/|-++')
    print('                        +  +--|    |--|--|_ |-')
    print("                     { /|__|  |/\__|  |--- |||__/")
    print("                    +---------------___[}-_===_.'____               /")
    print("                ____`-' ||___-{]_| _[}-  |     |_[___\==--          \/   _")
    print(" __..._____--==/___]_|__|_____________________________[___\==--___,-----' .7")
    print("|                                                                   BB-61/")
    print(" \_______________________________________________________________________|")
    print("  ASCII art by Matthew Bace\n\n")

    carrier     = False
    battleship  = False
    destroyer   = False
    submarine   = False
    patrol_boat = False

    display_ship_classes()
    display_menu()

    # User's ocean board
    ocean_board = setup_board()

    # User's firing board
    firing_board = setup_board()

    # Computer's boards
    opponent_board, opponent_firing_board, hits, opponent_hits = setup_opponent()
    
    # Ship positions
    ships = {"C": [], "B": [], "D": [], "S": [], "P": []}

    while True:
        choice = input('# ')
        match choice:
            case '?':
                display_menu()
            case '\n':
                display_menu()
            case 'c':
                if carrier == False:
                    carrier = query_and_place_ship(ocean_board, 'C', ships)
                else:
                    print("You already placed the carrier.\n")
            case 'C':
                if carrier == False:
                    carrier = query_and_place_ship(ocean_board, 'C', ships)
                else:
                    print("You already placed the carrier.\n")
            case 'b':
                if battleship == False:
                    battleship = query_and_place_ship(ocean_board, 'B', ships)
                else:
                    print("You already placed the battleship.\n")
            case 'B':
                if battleship == False:
                    battleship = query_and_place_ship(ocean_board, 'B', ships)
                else:
                    print("You already placed the battleship.\n")
            case 'D':
                if destroyer == False:
                    destroyer = query_and_place_ship(ocean_board, 'D', ships)
                else:
                    print("You already placed the destroyer.\n")
            case 'd':
                if destroyer == False:
                    destroyer = query_and_place_ship(ocean_board, 'D', ships)
                else:
                    print("You already placed the destroyer.\n")
            case 'S':
                if submarine == False:
                    submarine = query_and_place_ship(ocean_board, 'S', ships)
                else:
                    print("You already placed the submarine.\n")
            case 's':
                if submarine == False:
                    submarine = query_and_place_ship(ocean_board, 'S', ships)
                else:
                    print("You already placed the submarine.\n")
            case 'p':
                if patrol_boat == False:
                    patrol_boat = query_and_place_ship(ocean_board, 'P', ships)
                else:
                    print("You already placed the patrol boat.\n")
            case 'P':
                if patrol_boat == False:
                    patrol_boat = query_and_place_ship(ocean_board, 'P', ships)
                else:
                    print("You already placed the patrol boat.\n")
            case 'q':
                exit()
            case 'Q':
                exit()
            case 'O':
                print('\nOCEAN BOARD\n')
                display_board(ocean_board)
            case 'o':
                print('\nOCEAN BOARD\n')
                display_board(ocean_board)
            case 'F':
                print('\nFIRING BOARD')
                print('H: Hit, M: Miss\n')
                display_board(firing_board)
            case 'f':
                print('\nFIRING BOARD:\n')
                print('H: Hit, M: Miss\n')
                display_board(firing_board)
            case 'T':
                if carrier == False or submarine == False or battleship == False or\
                   destroyer == False or patrol_boat == False:
                    print("\nYou must place all 5 of your ships before firing shots.\n")
                else:
                    # User fires shot
                    target_shot(opponent_board, firing_board, hits)
                    # Opponent fires shot at user
                    opponent_shot(ocean_board, opponent_firing_board, opponent_hits, ships)
            case 't':
                if carrier == False or submarine == False or battleship == False or destroyer == False or patrol_boat == False:
                   print("\nYou must place all 5 of your ships before firing shots.\n")
                else:
                    # User fires shot
                    target_shot(opponent_board, firing_board, hits)
                    # Opponent fires shot at user
                    opponent_shot(ocean_board, opponent_firing_board, opponent_hits, ships)

            # Hidden debug case to show computer's board, pull out later
            case 'z':
                display_board(opponent_board)
            case 'y':
                display_board(opponent_firing_board)
            case _:
                display_menu()
