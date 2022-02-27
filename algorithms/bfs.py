from collections import deque
from .functions import hash_state, win, get_solution_map, direction, good_move, is_there_a_chest, move_chest, dx, dy

def run(map, N, M, sokoban_pos, chests, good_chests, goals):
    ALL_STATES = set()
    Q = deque()
    state = (sokoban_pos, chests, good_chests, [])
    Q.append(state)
    ALL_STATES.add(hash_state(sokoban_pos[0], sokoban_pos[1], state))

    solution = []
    solutionMap = []
    stateCount = 0

    while Q:
        act_state = Q.popleft()
        stateCount += 1

        if win(act_state[2]):
            solutionMap = get_solution_map(map, act_state, N)
            solution = [direction(i) for i in act_state[3]]
            break
        
        s_pos = act_state[0]
        for i in range(4):
            new_x = s_pos[0] + dx[i]
            new_y = s_pos[1] + dy[i]
            chests, good_chests = act_state[1].copy(), act_state[2].copy()
            moves = act_state[3].copy()
            if good_move(new_x, new_y, act_state, direction(i), N, M, map, ALL_STATES):
                if is_there_a_chest(new_x, new_y, act_state[1]): move_chest(new_x, new_y, i, chests, good_chests, goals)
                moves.append(i)
                new_state = ((new_x, new_y), chests, good_chests, moves)
                Q.append(new_state)
                
    return solution, solutionMap, stateCount
