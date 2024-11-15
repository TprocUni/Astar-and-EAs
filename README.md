# Astar-and-EAs
This report implements two computational approaches to solve challenging puzzles: the **A\*** algorithm for the 8-puzzle problem and a **genetic algorithm** for Sudoku. Both methods demonstrate the applicability of heuristic and evolutionary techniques to search and optimisation problems.


### A\* Algorithm for the 8-Puzzle Problem

#### Problem Framing
The 8-puzzle problem involves arranging numbered tiles on a 3x3 grid to match a target configuration. Moves involve sliding a tile into an adjacent empty space. The problem is framed as a **search problem**, where:

- **States**: Represented by tile configurations.
- **Actions**: Valid moves (up, down, left, right) depending on the empty space's position.
- **Goal State**: The target tile configuration.
- **Path Cost**: Each move has a cost of 1.

The search tree grows recursively, exploring possible moves until the goal state is reached. Optimizations include preventing repeated state evaluations and loops.

#### A\* Algorithm
The **A\*** algorithm uses heuristics to guide the search towards the goal. Two heuristics were implemented:

1. **Misplaced Tile Heuristic**:
   - Counts tiles not in their goal positions.
   - Simple and computationally inexpensive but provides limited information.

2. **Manhattan Distance**:
   - Calculates the total horizontal and vertical distances of tiles from their goal positions.
   - More informative but computationally intensive.

#### Results and Observations
- The **misplaced tile heuristic** produced faster results due to lower computational overhead, solving the puzzle in as few as 130 moves.
- The **Manhattan distance heuristic** yielded more optimal solutions (134 moves on average) but required more time per computation.
- Combining both heuristics reduced the number of moves to ~60, showcasing the benefits of heuristic synergy.
- Loop prevention strategies, such as penalizing repeated states by adjusting their `f` values, effectively reduced infinite loops.

#### Limitations
- The algorithm struggles with unsolvable configurations, which occur when the initial state has an odd number of tile inversions relative to the goal state.
- Space and time complexities remain high due to the need to store and traverse all possible paths.

---

### Genetic Algorithm for Sudoku

#### Problem Representation
The Sudoku puzzle is represented as a 9x9 grid where rows, columns, and 3x3 subgrids must contain unique digits (1-9). The genetic algorithm (GA) iteratively evolves solutions, guided by a fitness function.

1. **Chromosome Representation**:
   - A candidate solution is encoded as a 9x9 matrix, with initial values fixed based on the puzzle's given numbers.

2. **Fitness Function**:
   - Measures the number of conflicts (e.g., duplicates in rows, columns, or subgrids) and rewards solutions closer to the goal state.

3. **Operators**:
   - **Crossover**: Combines traits of two parent solutions to create offspring.
   - **Mutation**: Ensures diversity by randomly altering non-fixed values or swapping elements.

4. **Population Management**:
   - The population starts with diverse candidates, retaining elite individuals across generations.
   - Periodic mutations introduce novelty and avoid premature convergence.

#### Experimentation and Results
- **Sample Sizes**:
   - Smaller populations (e.g., size 10) converged quickly but often got stuck in local minima due to lack of diversity.
   - Larger populations (e.g., size 10,000) reached lower fitness scores but were computationally expensive.
   - **Optimal size**: A population of 100 balanced speed and diversity effectively.

- **Grid Complexity**:
   - Grids with fewer given values (e.g., 23/81) were harder to solve, as the algorithm relied heavily on random guesses, leading to higher conflict rates.
   - Simpler grids with more initial values (e.g., 78/81) were solved in seconds, confirming the algorithm's correctness.

#### Limitations
- The algorithm frequently stalled at local minima, requiring additional strategies like adaptive mutation rates or hybrid approaches.
- Computational time increased significantly for larger populations or complex grids.

---

### Comparative Insights

1. **Algorithm Suitability**:
   - A\* excels in problems with defined goal states and limited moves (e.g., 8-puzzle).
   - Genetic algorithms are better suited for optimization problems with large, complex solution spaces (e.g., Sudoku).

2. **Performance Trade-offs**:
   - A\* offers guaranteed optimality but suffers from poor space complexity.
   - Genetic algorithms can approximate solutions quickly but lack guarantees for optimality.

3. **Future Directions**:
   - Integrating heuristic-based approaches in the Sudoku solver could enhance efficiency.
   - Applying evolutionary strategies to the 8-puzzle might explore novel optimization avenues.

---

### Conclusion

This report showcases the versatility of heuristic and evolutionary algorithms in solving complex puzzles. The A\* algorithm efficiently handles structured problems like the 8-puzzle, while genetic algorithms offer robust, adaptable solutions for optimization tasks like Sudoku. Both methods demonstrate strengths and weaknesses, paving the way for hybrid approaches and further exploration.
