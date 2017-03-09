# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: In our algorithm for naked twins, we are looping through the unit list and trying to remove all possible values from each box that were in the "naked twins." Mind you each unit is either a square, a column, a row, or a diagonal. By focusing on one unit at a time, we are reducing the search space dramatically and thus are able to solve to Sudoku puzzle. 

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The way we solve a diagonal sudoku with constraint propagation is similar to how we solve a normal sudoku. All the same algorithms, only-choice, elimination, and naked twins still apply to constrain the search space and thus affect the rest of the Sudoku. It's just that with the diagonal sudoku, we are adding one more constraint. In addition to having the square, column, and row having unique 1-9 numbers, both diagonals need to have unique 1-9 numbers as well. We simply solve it by adding the 2 diagonals to the list of units. By doing that, the corresponding cells will now have accounted for the diagonals as peers as well. As a result, all algorithms are still working as before, and we are able to solve the sudoku. 

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

