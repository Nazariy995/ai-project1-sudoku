import itertools

rows = 'ABCDEFGHI'
cols = '123456789'

assignments = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)
#get row units
row_units = [cross(r, cols) for r in rows]
#get column units
column_units = [cross(rows, c) for c in cols]
#get square units
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
#get the main diagonal list
main_diagonal_units = [ cross(r, cols[i])[0] for i, r in enumerate(rows)]
#get the secondary diagonal list
secondary_diagonal_units = [ cross(r, cols[8-i])[0] for i, r in enumerate(rows)]
#combine both diagonal units
diagonal_units = [main_diagonal_units , secondary_diagonal_units]
#combine rows, columns, squares, and diagonals into one unitlist 
unitlist = row_units + column_units + square_units + diagonal_units
#covnert unitlist to a dictionary form
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    #generate all 2 letter combinations that can be in boxes
    twin_combos = [ comb[0]+comb[1] for comb in list(itertools.combinations('123456789', 2))]
    #loop thorugh unitlist 
    for unit in unitlist:
        #check for each combination in the unit list
        for comb in twin_combos:
            dplaces = [box for box in unit if comb == values[box]]
            #if there are 2 boxes with the same combination
            if len(dplaces) == 2:
                #clear the combination from all the other boxes in the unit
                clear_naked_twins(values, unit, comb)
    return values

def clear_naked_twins(values, unit, comb):
    """
    Clear all values from the unit that are in the comb variable 
    Args:
        values(dict) - a dictionary of the form {'box_name': '123456789', ...}
        unit(array) - an array of the form [A1, A2, A3, ...]
        comb(string) - a two letter combination of '123456789' of the form '23'
    Returns:
        none
    """
    for box in unit:
        #make sure we are not replacing the actual combination
        if comb != values[box]:
            #clear all values from comb[0]
            new_value = values[box].replace(comb[0], '')
            #clear all values from comb[1]
            new_value = new_value.replace(comb[1], '')
            #assign a new value
            assign_value(values, box, new_value)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    #check if len of chars is 81, otherwise triger error
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """Eliminate values using the eliminate strategy. 
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with assigned values eliminated from peers.
    """
    #check for assigned values
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        #loop through all peers and replace the assigned value with a ""
        for peer in peers[box]:
            new_value = values[peer].replace(digit,'')
            assign_value(values, peer, new_value)
    return values

def only_choice(values):
    """Eliminate values using the only choice strategy. 
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with values assigned from only choice strategy.
    """
    #loop through unitlist
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            #check for a uniqe number amongst the unit
            if len(dplaces) == 1:
                #assign that unique number to the corresponding box
                assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    """
    Try solving the sudoku puzzle using the eliminate and only choice strategies.
    Check for any changes. If no changes found return. 
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the new reduced puzzle
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after

        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """Solve sudoku puzzle by tring different options of possible values
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary the solved sudoku puzzle or false for cannot be solved
    """
    sudoku = reduce_puzzle(values)
    if sudoku is False:
        return False;
    elif all(len(values[cell]) == 1 for cell in boxes):
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    n,cell = min((len(values[box]), box) for box in boxes if len(values[box]) >1)
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[cell]:
        new_sudoku = values.copy()
        new_sudoku[cell] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    solution = search(values)

    return values


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
