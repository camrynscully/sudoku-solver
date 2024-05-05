# CISC 681 - Programming Assignment 2
# Camryn Scully

# Part 6: Web Visualization
# ----------------------------------------------------------------------------------------------------------------------------

from flask import Flask, render_template, request
from sudoku import solve_puzzle, csp9x9

app = Flask(__name__)

# convert the assignments to a 2D array to display as a sudoku board
def sudoku_grid(step):
    grid = [['' for _ in range(9)] for _ in range(9)]
    # double for loop to iterate over X, Y coordinates
    for x in range(1, 10):
        for y in range(1, 10):
            # construct the key as a string
            key = f"{x},{y}"
            
            value = step.get(key, " ")  # default blank value if key is not found
            value_str = str(value) 
            # Set value of grid in that location to the currently being-observed output
            grid[x-1][y-1] = value_str
    return grid

# Initialze the URL for flask
# Print the solution and intermediate board states given the user input board
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        puzzle_input = parse_puzzle_input(request.form)
        [result_board, solve_iterations] = solve_puzzle(csp9x9, puzzle_input)
        steps = [sudoku_grid(step) for step in solve_iterations]
        final_solution_grid = sudoku_grid(result_board)
        print(final_solution_grid)
        return render_template(
            'sudoku_grid.html',
            final_solution = final_solution_grid,
            steps = steps
        )
    return render_template('sudoku_grid.html')

# Helper function that takes extracts data from user input on the sudoku board
def parse_puzzle_input(formData):
    return {
        cell: int(value) 
        for cell, value in formData.items() 
        if value.isdigit()
    }

if __name__ == '__main__':
    app.run(debug=True)
    