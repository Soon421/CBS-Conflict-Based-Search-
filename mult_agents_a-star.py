import math
import heapq
import itertools
from simulation_multi import sim_multi

# 맨해튼 거리
def distance(node1, node2):
    x1, y1 = node1
    x2, y2 = node2
    return abs(x1 - x2) + abs(y1 - y2)

# 충돌체크 (vertex + edge conflict)
def has_conflict(prev_state, new_state):
    # vertex conflict
    if len(set(new_state)) < len(new_state):
        return True
    # edge conflict (swap)
    for i in range(len(prev_state)):
        for j in range(i + 1, len(prev_state)):
            if prev_state[i] == new_state[j] and prev_state[j] == new_state[i]:
                return True
    return False

# === SOC 계산(수정 버전): goal "첫 도달 시각"만 합산 ===
def compute_soc(solution, agents):
    soc = 0
    for aid, path in solution.items():
        goal = agents[aid]['goal']
        # 최초 goal 도달 시각(t)을 찾는다. (없다면 마지막 시각으로 보정)
        t_arrival = None
        for t, pos in enumerate(path):
            if pos == goal:
                t_arrival = t
                break
        if t_arrival is None:
            t_arrival = len(path) - 1  # 안전장치(정상해에선 거의 안 옴)

        print(f"Agent {aid} 도달 시간: {t_arrival}")
        soc += t_arrival
    return soc


def multi_agent_a_star(graph, agents, objective="soc"):
    """
    Multi-Agent A* Search
    objective: "soc" (Sum of Costs) / "makespan" (Time steps)
    """
    agent_ids = sorted(agents.keys())
    starts = tuple(agents[aid]['start'] for aid in agent_ids)
    goals  = tuple(agents[aid]['goal']  for aid in agent_ids)

    start_state = starts
    goal_state  = goals

    g_costs = {start_state: 0}
    h = sum(distance(s, g) for s, g in zip(starts, goals))
    open_list = [(h, start_state)]
    parents = {start_state: None}
    closed_list = set()

    while open_list:
        f, state = heapq.heappop(open_list)
        if state in closed_list:
            continue
        closed_list.add(state)

        # goal check
        if state == goal_state:
            # reconstruct path
            path = []
            s = state
            while s:
                path.append(s)
                s = parents[s]
            path.reverse()

            # agent별 분리
            paths = {aid: [] for aid in agent_ids}
            for joint in path:
                for i, aid in enumerate(agent_ids):
                    paths[aid].append(joint[i])
            return paths, g_costs[state]

        # branching: 각 agent move 조합
        moves_per_agent = []
        for pos in state:
            moves = [pos]  # 대기 가능
            if pos in graph:
                for nxt, _ in graph[pos]:
                    moves.append(nxt)
            moves_per_agent.append(moves)

        for joint_move in itertools.product(*moves_per_agent):
            if has_conflict(state, joint_move):
                continue

            new_state = tuple(joint_move)

            # --- 비용 계산 ---
            if objective == "soc":
                step_cost = 0
                for i in range(len(state)):
                    # goal 도달 전이라면 이번 timestep 비용 1 추가
                    if state[i] != goals[i]:
                        step_cost += 1
                cost = g_costs[state] + step_cost

            else:
                # makespan: joint timestep (한 번 움직이면 +1)
                cost = g_costs[state] + 1

            h = sum(distance(new_state[i], goals[i]) for i in range(len(state)))

            if new_state in g_costs and cost >= g_costs[new_state]:
                continue

            g_costs[new_state] = cost
            parents[new_state] = state
            heapq.heappush(open_list, (cost + h, new_state))

    return None, None


# 맵
graph = {
    #Row0
    (1, 0): [((1, 1), 1)],
    (3, 0): [((3, 1), 1)],
    (5, 0): [((5, 1), 1)],
    (7, 0): [((7, 1), 1)],
    #Row1
    (1, 1): [((1, 2), 1), ((1, 0), 1), ((2, 1), 1)],
    (2, 1): [((1, 1), 1), ((3, 1), 1)],
    (3, 1): [((3, 2), 1), ((3, 0), 1), ((2, 1), 1)],
    (5, 1): [((5, 2), 1), ((5, 0), 1)],
    (7, 1): [((7, 2), 1), ((7, 0), 1)],
    #Row2
    (1, 2): [((1, 3), 1), ((1, 1), 1)],
    (3, 2): [((3, 3), 1), ((3, 1), 1)],
    (5, 2): [((5, 3), 1), ((5, 1), 1)],
    (7, 2): [((7, 3), 1), ((7, 1), 1)],
    #Row3
    (1, 3): [((1, 4), 1), ((1, 2), 1)],
    (3, 3): [((3, 4), 1), ((3, 2), 1)],
    (5, 3): [((5, 4), 1), ((5, 2), 1), ((6, 3), 1)],
    (6, 3): [((6, 4), 1), ((5, 3), 1), ((7, 3), 1)],
    (7, 3): [((7, 4), 1), ((7, 2), 1), ((6, 3), 1)],
    #Row4
    (1, 4): [((1, 5), 1), ((1, 3), 1), ((2, 4), 1)],
    (2, 4): [((1, 4), 1), ((3, 4), 1), ((2, 5),1)],
    (3, 4): [((3, 5), 1), ((3, 3), 1), ((2, 4), 1), ((4, 4), 1)],
    (4, 4): [((3, 4), 1), ((5, 4), 1)],
    (5, 4): [((5, 5), 1), ((5, 3), 1), ((4, 4), 1), ((6, 4), 1)],
    (6, 4): [((6, 3), 1), ((5, 4), 1), ((7, 4), 1)],
    (7, 4): [((7, 5), 1), ((7, 3), 1), ((6, 4), 1), ((8,4), 1)],
    (8, 4): [((7, 4), 1)],
    #Row5
    (1, 5): [((1, 6), 1), ((1, 4), 1),((2, 5),1)],
    (2, 5): [((1, 5), 1), ((2, 4), 1), ((3, 5),1)],
    (3, 5): [((3, 6), 1), ((3, 4), 1), ((2, 5),1)],
    (5, 5): [((5, 6), 1), ((5, 4), 1)],
    (7, 5): [((7, 6), 1), ((7, 4), 1)],
    #Row6
    (1, 6): [((1, 7), 1), ((1, 5), 1)],
    (3, 6): [((3, 5), 1)],
    (5, 6): [((5, 7), 1), ((5, 5), 1)],
    (7, 6): [((7, 7), 1), ((7, 5), 1)],
    #Row7
    (1, 7): [((1, 8), 1), ((1, 6), 1)],
    (5, 7): [((5, 8), 1), ((5, 6), 1), ((6, 7), 1)],
    (6, 7): [((5, 7), 1), ((7, 7), 1)],
    (7, 7): [((7, 8), 1), ((7, 6), 1), ((6, 7), 1)],
    #Row8
    (1, 8): [((1, 7), 1)],
    (3, 8): [((4, 8), 1)],
    (4, 8): [((3, 8), 1), ((5, 8), 1)],
    (5, 8): [((5, 7), 1), ((4, 8), 1)],
    (7, 8): [((7, 7), 1)]
}
agents={
    1: {'start': (1, 0), 'goal': (7, 7)},
    2: {'start': (7, 8), 'goal': (1, 0)},
    3: {'start': (1, 1), 'goal': (2, 4)},
    4: {'start': (1, 2), 'goal': (7, 8)},
}

#실행 및 출력
solution, _ = multi_agent_a_star(graph, agents)
soc_value = compute_soc(solution, agents)  
print("SOC:", soc_value)
for aid, path in solution.items():
    print(f"Agent {aid} path: {path}")

# 시뮬레이션 (CBS와 같은 함수 재사용)
sim_multi(solution, agents, graph)


