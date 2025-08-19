#low_level_search_modul
import heapq
import math

#거리측정함수
def distance(node1, node2):
    x1, y1 = node1
    x2, y2 = node2
    #격자기반으로 움직이므로 맨허튼거리를 Heuristic 값으로 함.
    return abs(x1 - x2) + abs(y1 - y2)  

# LLS(Low-Level Search)
def lls(s_node, g_node, constraints, graph):
    # 1) 해당 agent의 제약들 중 '시간'의 최대값 계산
    horizon = 0
    for c in constraints:
        if isinstance(c, tuple) and len(c) == 2:  # 기존 포맷 ((...), t)
            horizon = max(horizon, c[1])
        elif isinstance(c, tuple) and len(c) == 3:  # 새 포맷 ('V'/'E', ..., t)
            horizon = max(horizon, c[2])

    # 상태: (node, time)
    s_state = (s_node, 0)
    open_list = [(distance(s_node, g_node), s_state)]
    closed_list = set()
    g_costs = {s_state: 0}
    parents = {s_state: None}

    while open_list:
        _, c_state = heapq.heappop(open_list)
        if c_state in closed_list:
            continue
        closed_list.add(c_state)
        c_node, c_time = c_state

        # 2) 종료 조건: goal 도달 & c_time >= horizon
        if c_node == g_node and c_time >= horizon:
            # 경로 복원
            path = []
            s = c_state
            while s is not None:
                path.append(s[0])
                s = parents[s]
            path.reverse()
            return (path, g_costs[c_state])

        # 3) move 생성 (대기 포함)
        possible_moves = graph.get(c_node, []) + [(c_node, 1)]

        for n_node, move_cost in possible_moves:
            n_time = c_time + 1
            n_state = (n_node, n_time)

            # --- (a) 정점 제약 ---
            # 구(현) 포맷 둘 다 지원
            if (n_node, n_time) in constraints:
                continue
            blocked_vertex = False
            for c in constraints:
                # 새 포맷: ('V', node, t)
                if isinstance(c, tuple) and len(c) == 3 and c[0] == 'V':
                    if c[1] == n_node and c[2] == n_time:
                        blocked_vertex = True
                        break
            if blocked_vertex:
                continue

            # --- (b) 간선 제약 ---
            blocked_edge = False
            for c in constraints:
                # 구 포맷: ((u, v), t)
                if isinstance(c, tuple) and len(c) == 2 and isinstance(c[0], tuple) and len(c[0]) == 2:
                    if (c_node, n_node) == c[0] and c_time == c[1]:
                        blocked_edge = True; break
                # 새 포맷: ('E', (u, v), t)
                if isinstance(c, tuple) and len(c) == 3 and c[0] == 'E':
                    if (c_node, n_node) == c[1] and c_time == c[2]:
                        blocked_edge = True; break
            if blocked_edge:
                continue

            if n_state in closed_list:
                continue

            gn = g_costs[c_state] + move_cost
            hn = distance(n_node, g_node)  # 맨해튼
            fn = gn + hn

            if n_state in g_costs and gn >= g_costs[n_state]:
                continue
            g_costs[n_state] = gn
            parents[n_state] = c_state
            heapq.heappush(open_list, (fn, n_state))

    return (None, float('inf'))
