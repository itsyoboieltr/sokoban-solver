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

def get_solution_map(map, state, N):
    map2 = [[] for _ in range(N)]
    for i in range(N): map2[i] = map[i].copy()
    s_pos = state[0]
    chests = state[1]
    map2[s_pos[0]][s_pos[1]] = 'P'
    for c in chests: map2[c[0]][c[1]] = 'C'
    return map2
