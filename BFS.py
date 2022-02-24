from collections import deque

dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]

def direction(x):
    return ['right', 'left', 'down', 'up'][x]

def hash_state(x, y, state):
    chests = tuple(state[1])
    return ((x, y), chests)

def hash_all(state):
    pos = state[0]
    chests = tuple(state[1])
    good = tuple(state[2].items())
    return (pos, chests, good)

def is_there_a_chest(x, y, chests):
    for c in chests:
        if c == (x, y): return True
    return False

def blocked_chest(x, y, map):
    cnt = 0
    for i in range(4):
        if map[x + dx[i]][y + dy[i]] == '#': cnt += 1
    return cnt >= 3

def good_move(x, y, state, direction, N, M, map, ALL_STATES):
    if not(0 <= x < N) or not(0 <= y < M) or map[x][y] == '#': return False

    hs = hash_state(x, y, state)
    chests = state[1]

    for chest in chests:
        if map[chest[0]][chest[1]] == '#' or blocked_chest(chest[0], chest[1], map): return False

    if is_there_a_chest(x, y, chests):
        if direction == 'down' and x + 1 < N and (is_there_a_chest(x + 1, y, chests) or map[x + 1][y] == '#'): return False
        if direction == 'up' and x - 1 >= 0 and (is_there_a_chest(x - 1, y, chests) or map[x - 1][y] == '#'): return False
        if direction == 'right' and y + 1 < M and (is_there_a_chest(x, y + 1, chests) or map[x][y + 1] == '#'): return False
        if direction == 'left' and y - 1 >= 0 and (is_there_a_chest(x, y - 1, chests) or map[x][y - 1] == '#'): return False
    else:
        if hs in ALL_STATES: return False

    ALL_STATES.add(hs)
    return True

def move_chest(x, y, direction, chests, good_chests, goals):
    vector = (dx[direction], dy[direction])
    for i in range(len(chests)):
        c_x = chests[i][0]
        c_y = chests[i][1]
        if c_x == x and c_y == y:
            if chests[i] in goals: good_chests[chests[i]] = False
            chests[i] = (c_x + vector[0], c_y + vector[1])
            if chests[i] in goals: good_chests[chests[i]] = True

def win(good_chests):
    for c in good_chests.items():
        if not c[1]: return False
    return True

def print_map(map, state, N):
    map2 = [[] for _ in range(N)]
    for i in range(N): map2[i] = map[i].copy()
    s_pos = state[0]
    chests = state[1]
    map2[s_pos[0]][s_pos[1]] = 'P'
    for c in chests: map2[c[0]][c[1]] = 'C'
    for m in map2: print(*m)
    print()

def run_bfs(map):
    sokoban_pos = (0, 0)
    chests = []
    good_chests = {}
    goals = []
    ALL_STATES = set()

    print('<Beginning state>\n')
    print('C: chest | G: goal | P: player | #: wall\n')
    for m in map: print(*m)
    print('\n<Looking for solution>\n')
    
    N, M = len(map), len(map[0])

    # Extract all positions
    for i in range(N):
        for j in range(M):
            if map[i][j] == 'P': sokoban_pos = (i, j)
            if map[i][j] == 'C': chests.append((i, j))
            if map[i][j] == 'G':
                good_chests[(i, j)] = False
                goals.append((i, j))
            if map[i][j] == '*':
                good_chests[(i, j)] = True
                chests.append((i, j))
                goals.append((i, j))
            if map[i][j] != '#': map[i][j] = '.'

    Q = deque()
    state = (sokoban_pos, chests, good_chests, [])
    Q.append(state)
    ALL_STATES.add(hash_state(sokoban_pos[0], sokoban_pos[1], state))

    cnt = 0
    solution = []
    while len(Q) > 0:
        act_state = Q.popleft()
        cnt += 1
        if cnt % 10000 == 0: print('States visited: ', cnt)

        if win(act_state[2]):
            print('\n<SOLUTION FOUND!>\n')
            print_map(map, act_state, N)
            solution = [direction(i) for i in act_state[3]]
            break
        
        s_pos = act_state[0]
        for i in range(4):
            new_x = s_pos[0] + dx[i]
            new_y = s_pos[1] + dy[i]
            chests, good_chests = act_state[1].copy(), act_state[2].copy()
            moves = act_state[3].copy()
            if good_move(new_x, new_y, act_state, direction(i), N, M, map, ALL_STATES):
                if is_there_a_chest(new_x, new_y, act_state[1]):
                    move_chest(new_x, new_y, i, chests, good_chests, goals)
                moves.append(i)
                new_state = ((new_x, new_y), chests, good_chests, moves)
                Q.append(new_state)
    return solution
