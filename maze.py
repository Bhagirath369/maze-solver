class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        return self.frontier.pop()

class Maze:
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()

            # check for exactly one starting and ending point

        if contents.count("A") != 1 or contents.count("B") != 1:
            raise Exception("Maze must have exactly one starting point and one goal")

        self.height = len(contents.splitlines())
        self.width = max(len(line) for line in contents.splitlines())
        self.walls = []

        for i, line in enumerate(contents.splitlines()):
            row = []
            for j in range(self.width):
                if j < len(line):
                    if line[j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif line[j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif line[j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                else:
                    row.append(True)  # Out of bounds is a wall
            self.walls.append(row)

        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else []
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("@", end='')
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbours(self, state):
        row, col = state
        # all possible states
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]
       
       # Ensure actions are valid
        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    def solve(self):
         # find the solution of the maze if it exists
         # keep track  of numver of states explored
        self.num_explored = 0
        #initialize frontier to just  the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        self.explored = set()

        while True:
            if frontier.empty():
                raise Exception("no solution")

            node = frontier.remove()
            self.num_explored += 1

            if node.state == self.goal:
                actions = []
                cells = []

                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent

                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            self.explored.add(node.state)

            for action, state in self.neighbours(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

if __name__ == "__main__":
    maze = Maze("maze1.txt")

    # Solve the maze
    maze.solve()

    # Print the solution
    maze.print()

    # Print the number of explored states
    print(f"Number of states explored: {maze.num_explored}")





    


            

    

        


