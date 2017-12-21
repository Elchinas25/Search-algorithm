def make_moves(move, list): #orden de salida = UDLR
    if move == 'U':
        return moveUp(list)
    if move == 'D':
        return moveDown(list)
    if move == 'L':
        return moveLeft(list)
    if move == 'R':
        return moveRight(list)

def moveUp(current_list):
    initial_index = current_list.index(0)
    start_ind = initial_index
    final_ind = start_ind - 3
    val_to_change = current_list[final_ind]
    current_list[start_ind] = val_to_change
    current_list[final_ind] = 0
    return current_list

def moveDown(lista):
    initial_index = lista.index(0)
    current_list = lista
    start_ind = initial_index
    final_ind = start_ind + 3
    val_to_change = current_list[final_ind]
    current_list[start_ind] = val_to_change
    current_list[final_ind] = 0
    return current_list

def moveLeft(lista):
    initial_index = lista.index(0)
    current_list = lista
    start_ind = initial_index
    final_ind = start_ind - 1
    val_to_change = current_list[final_ind]
    current_list[start_ind] = val_to_change
    current_list[final_ind] = 0
    return current_list

def moveRight(lista):
    initial_index = lista.index(0)
    current_list = lista
    start_ind = initial_index
    final_ind = start_ind + 1
    val_to_change = current_list[final_ind]
    current_list[start_ind] = val_to_change
    current_list[final_ind] = 0
    return current_list

def list_moves(lista):
    index = lista.index(0)
    if index == 0:
        return ['D', 'R']
    elif index == 1:
        return ['D', 'L', 'R']
    elif index == 2:
        return ['D', 'L']
    elif index == 3:
        return ['U', 'D', 'R']
    elif index == 4:
        return ['U', 'D', 'L', 'R']
    elif index == 5:
        return ['U', 'D', 'L']
    elif index == 6:
        return ['U', 'R']
    elif index == 7:
        return ['U', 'L', 'R']
    elif index == 8:
        return ['U', 'L']


class StateInGame(object):
    def __init__(self, combinacion):
        self.combinacion = combinacion

    def get_list(self):
        return self.combinacion

    def check_moves(self):
        available_moves = list_moves(self.combinacion)
        return available_moves

    def neighbors(self):
        to_apply = list_moves(self.combinacion)
        children = []
        for m in to_apply:
            new_list = []
            for i in self.combinacion:
                new_list.append(i)
            new_list = make_moves(m, new_list)
            children.append(new_list)
        return children


import queue


class CheckableQueue(queue.Queue): # or OrderedSetQueue
    def __contains__(self, item):
        with self.mutex:
            return item in self.queue


def goal_test(comb):
    goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    if comb == goal:
        return True
    else:
        return False


def is_valid(pre, test):
    for i in pre:
        if i.get_list() == test:
            return False
    else:
        return True


def find_bfs_path(nod_vis, moves_list, states_dict):
    moves_path = []

    checking = len(moves_list) + 1
    diff = checking - nod_vis

    if diff > 0:
        while diff > 0:
            del moves_list[len(moves_list) - 1]
            diff -= 1

    node_index = nod_vis - 1
    move_index = nod_vis - 2

    dict_values = list(states_dict.values())
    end_road = dict_values[0]

    moves_path.append(moves_list[move_index])

    while not node_index in end_road:

        for l in dict_values:
            if node_index in l:
                parent_index = dict_values.index(l)

                move_index = parent_index - 1
                moves_path.append(moves_list[move_index])

        node_index = parent_index

    moves_path.reverse()

    return moves_path


def find_dfs_path(nod_vis, moves_list, states_list):
    moves_taken = []
    values_list = list(states_list.values())
    last_node_index = nod_vis - 1

    print(moves_list[last_node_index])
    moves_taken.append(moves_list[last_node_index])

    while not last_node_index == 0:
        for l in values_list:
            if last_node_index in l:
                last_node_index = list(states_list.keys())[list(states_list.values()).index(l)]
                moves_taken.append(moves_list[last_node_index])
                break

    moves_taken.reverse()

    return moves_taken

print()
print('Empezando busqueda por niveles...')
print()
print()

def fbs(initial_state):
    state_count = 0
    nodes_count = 0

    nodes_expanded = 0
    nodes_visited = 0

    explored = set()
    frontier = CheckableQueue()
    moves_dict = []
    states_dict = {}

    frontier.put(initial_state)

    while not frontier.empty():
        current_comb = frontier.get()
        scenario = StateInGame(current_comb)
        
        nodes_visited += 1

        if goal_test(current_comb):
            explored.add(scenario)
            print('Movimientos: %s' % moves_dict)
            print('Movimientos:')
            print('***')
            print('Solución encontrada: %s' % current_comb)
            print('***')
            path = find_bfs_path(nodes_visited, moves_dict, states_dict)
            print()
            print('Moves performed to reach the solution: ', path)
            print()
            print('Nodes expanded =', nodes_expanded)
            print('Nodes visited =', nodes_visited)
            print()
            break

        available_moves = scenario.check_moves()

        explored.add(scenario)

        state_children = []

        count = 0

        for child in scenario.neighbors():
            if is_valid(explored, child) and child not in frontier:
                nodes_count += 1
                nodes_expanded += 1

                moves_dict.append(available_moves[count])
                state_children.append(nodes_count)
                frontier.put(child)

            count += 1

        states_dict[state_count] = state_children

        state_count += 1

# fbs([1, 2, 5, 3, 4, 0, 6, 7, 8])

print()
print('Empezando busqueda profunda...')
print()
print()




from collections import deque


def find_node_in_game(dic, visited):
    vals = list(dic.values())
    vals.reverse()

    for l in vals:
        for i in l:
            if i not in visited:
                visited.append(i)
                return i
                break



def dfs(initial_state):
    nodes_expanded = 0
    nodes_visited = 0
    init_st_bool = 1

    frontier = deque()
    explored = set()

    moves_dict = []
    expanded_nodes_list = []
    states_dict = {}

    frontier.append(initial_state)

    while frontier:
        current_comb = frontier.pop()
        scenario = StateInGame(current_comb)

        if goal_test(current_comb):
            nodes_visited += 1
            print('***')
            print('Solución encontrada: %s' % current_comb)
            print('***')
            success_path = find_dfs_path(nodes_visited, moves_dict, states_dict)
            print()
            print('Moves taken to reach the solution: %s' % success_path)
            print()
            print('Nodes expanded: %s' % nodes_expanded)
            print('Nodes visited: %s' % nodes_visited)
            break

        explored.add(scenario)
        nodes_visited += 1

        available_moves = scenario.check_moves()
        possible_children_list = scenario.neighbors()

        possible_children_list.reverse()

        moves_count = len(available_moves) - 1
        children_list_count = []

        for child in possible_children_list:
            if is_valid(explored, child) and child not in frontier:
                nodes_expanded += 1

                children_list_count.append(nodes_expanded)
                frontier.append(child)
            else:
                del available_moves[moves_count]

            moves_count -= 1


        for m in available_moves:
            moves_dict.append(m)

        if init_st_bool == 1:
            states_dict[0] = children_list_count
            init_st_bool = 0
        else:
            curr_state = find_node_in_game(states_dict, expanded_nodes_list)
            states_dict[curr_state] = children_list_count


dfs([1, 4, 2, 3, 7, 5, 6, 0, 8])































