from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import urllib.request


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


def game_move(token, action):
    url = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=' + token
    post_field = {'action': action}
    request = Request(url, urlencode(post_field).encode())
    data = urlopen(request).read().decode()
    return json.loads(data)


def game_status(token):
    url = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=' + token
    data = urllib.request.urlopen(url).read()
    return json.loads(data)


def main():
    url = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/session'
    uid = '004906107'
    post_field = {'uid': uid}
    request = Request(url, urlencode(post_field).encode())
    data = urlopen(request).read().decode()
    json_token = json.loads(data)
    token = json_token['token']

    status = game_status(token)
    print(status)
    while status['status'] == 'PLAYING':
        xlen = status['maze_size'][0];
        ylen = status['maze_size'][1];
        maze = [['u' for a in range(xlen)] for b in range(ylen)]

        movestack = Stack()
        xpos = status['current_location'][0]
        ypos = status['current_location'][1]
        maze[ypos][xpos] = 'v'

        while True:
            if xpos + 1 < xlen and maze[ypos][xpos + 1] == 'u':
                result = game_move(token, 'RIGHT')['result']
                if result == 'END':
                    print('Found end at: ' + str(xpos+1) + ',' + str(ypos))
                    break
                elif result == 'SUCCESS':
                    movestack.push('R')
                    xpos += 1
                    maze[ypos][xpos] = 'v'
                    print('visiting position: ' + str(xpos) + ',' + str(ypos))
                    continue
                elif result == 'WALL':
                    maze[ypos][xpos + 1] = '*'
            if xpos - 1 >= 0 and maze[ypos][xpos - 1] == 'u':
                result = game_move(token, 'LEFT')['result']
                if result == 'END':
                    print('Found end at: ' + str(xpos + 1) + ',' + str(ypos))
                    break
                elif result == 'SUCCESS':
                    movestack.push('L')
                    xpos -= 1
                    maze[ypos][xpos] = 'v'
                    print('visiting position: ' + str(xpos) + ',' + str(ypos))
                    continue
                elif result == 'WALL':
                    maze[ypos][xpos - 1] = '*'
            if ypos + 1 < ylen and maze[ypos + 1][xpos] == 'u':
                result = game_move(token, 'DOWN')['result']
                if result == 'END':
                    print('Found end at: ' + str(xpos + 1) + ',' + str(ypos))
                    break
                elif result == 'SUCCESS':
                    movestack.push('D')
                    ypos += 1
                    maze[ypos][xpos] = 'v'
                    print('visiting position: ' + str(xpos) + ',' + str(ypos))
                    continue
                elif result == 'WALL':
                    maze[ypos + 1][xpos] = '*'
            if ypos - 1 >= 0 and maze[ypos - 1][xpos] == 'u':
                result = game_move(token, 'UP')['result']
                if result == 'END':
                    print('Found end at: ' + str(xpos + 1) + ',' + str(ypos))
                    break
                elif result == 'SUCCESS':
                    movestack.push('U')
                    ypos -= 1
                    maze[ypos][xpos] = 'v'
                    print('visiting position: ' + str(xpos) + ',' + str(ypos))
                    continue
                elif result == 'WALL':
                    maze[ypos - 1][xpos] = '*'

            # backtrack
            if not movestack.isEmpty():
                move = movestack.pop()
                if move == 'R':
                    xpos -= 1
                    game_move(token, 'LEFT')
                    print('backtracking to: ' + str(xpos) + ',' + str(ypos))
                    continue
                elif move == 'L':
                    xpos += 1
                    game_move(token, 'RIGHT')
                    print('backtracking to: ' + str(xpos) + ',' + str(ypos))
                    continue
                elif move == 'U':
                    ypos += 1
                    game_move(token, 'DOWN')
                    print('backtracking to: ' + str(xpos) + ',' + str(ypos))
                    continue
                elif move == 'D':
                    ypos -= 1
                    game_move(token, 'UP')
                    print('backtracking to: ' + str(xpos) + ',' + str(ypos))
                    continue
            elif movestack.isEmpty():
                print("STUCK! Resetting..")
                del maze
                maze = [['u' for a in range(xlen)] for b in range(ylen)]
                maze[ypos][xpos] = 'v'
        del maze
        del movestack
        status = game_status(token)
        print(game_status(token))


if __name__ == '__main__':
    main()