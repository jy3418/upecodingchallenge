class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


def main():
    # Have an internal representation of an array
    # cross reference with internal representation, if the move that I'm trying is empty, try it, store that move
    # into a stack, mark the visited places
    # If possible move is unmarked, try it first. If successful, then store that move in a stack
    # If out of options of unvisited moves, backtrack by popping the last move in the stack

    given_maze = [
        ['S', '*', ' ', ' ', ' ', '*', ' ', ' ', ' '],
        [' ', ' ', '*', ' ', '*', ' ', ' ', '*', ' '],
        [' ', '*', '*', ' ', '*', '*', ' ', '*', ' '],
        [' ', ' ', ' ', ' ', ' ', '*', 'E', '*', ' '],
        [' ', '*', '*', '*', ' ', '*', '*', '*', ' '],
        ['*', ' ', ' ', ' ', ' ', ' ', ' ', '*', ' '],
        [' ', ' ', '*', '*', '*', '*', ' ', '*', ' '],
        [' ', '*', ' ', ' ', ' ', '*', '*', '*', ' '],
        [' ', ' ', ' ', '*', ' ', ' ', ' ', ' ', ' ']
    ]

    xlen = 3;
    ylen = 1;
    maze = [['u' for a in range(xlen)] for b in range(ylen)]

    movestack = Stack()
    xpos = 0
    ypos = 0
    maze[ypos][xpos] = 'v'

    while True:
        if given_maze[ypos][xpos] == 'E':
            print('Found end at: ' + str(xpos) + ',' + str(ypos))
            break

        if xpos + 1 < xlen and maze[ypos][xpos + 1] == 'u':
            if given_maze[ypos][xpos + 1] != '*':
                movestack.push('R')
                xpos += 1
                maze[ypos][xpos] = 'v'
                print('visiting position: ' + str(xpos) + ',' + str(ypos))
                continue
            elif given_maze[ypos][xpos + 1] == '*':
                maze[ypos][xpos + 1] = '*'
        if xpos - 1 >= 0 and maze[ypos][xpos - 1] == 'u':
            if given_maze[ypos][xpos - 1] != '*':
                movestack.push('L')
                xpos -= 1
                maze[ypos][xpos] = 'v'
                print('visiting position: ' + str(xpos) + ',' + str(ypos))
                continue
            elif given_maze[ypos][xpos - 1] == '*':
                maze[ypos][xpos - 1] = '*'
        if ypos + 1 < ylen and maze[ypos + 1][xpos] == 'u':
            if given_maze[ypos + 1][xpos] != '*':
                movestack.push('D')
                ypos += 1
                maze[ypos][xpos] = 'v'
                print('visiting position: ' + str(xpos) + ',' + str(ypos))
                continue
            elif given_maze[ypos + 1][xpos] == '*':
                maze[ypos + 1][xpos] = '*'
        if ypos - 1 >= 0 and maze[ypos - 1][xpos] == 'u':
            if given_maze[ypos - 1][xpos] != '*':
                movestack.push('U')
                ypos -= 1
                maze[ypos][xpos] = 'v'
                print('visiting position: ' + str(xpos) + ',' + str(ypos))
                continue
            elif given_maze[ypos - 1][xpos] == '*':
                maze[ypos - 1][xpos] = '*'

        # backtrack
        if not movestack.isEmpty():
            move = movestack.pop()
            if move == 'R':
                xpos -= 1
                print('backtracking to: ' + str(xpos) + ',' + str(ypos))
            elif move == 'L':
                xpos += 1
                print('backtracking to: ' + str(xpos) + ',' + str(ypos))
            elif move == 'U':
                ypos += 1
                print('backtracking to: ' + str(xpos) + ',' + str(ypos))
            elif move == 'D':
                ypos -= 1
                print('backtracking to: ' + str(xpos) + ',' + str(ypos))


if __name__ == '__main__':
    main()