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
    # state(node, time), 노드위치와 시간정보를 담고있는 '상태' 를 기준단위로 사용
    s_state=(s_node, 0)
    # open_list, (f(n)값, 상태) 형태로 저장. 시작 노드의 f(n) = h(n)
    open_list = [(distance(s_node, g_node), s_state)]
    closed_list = set()    
    g_costs = {s_state: 0}
    parents = {s_state : None}
    path = [] 

    # open_list에 탐색할 노드가 남아있는 동안 반복
    while open_list: 
        
        # open_list에서 f(n)이 가장 작은 노드를 꺼냄
        _, c_state = heapq.heappop(open_list)

        # 먼저 closed_list를 확인하여 중복 탐색을 방지
        if c_state in closed_list:
            continue

        #c_state를 위치,시간 정보로 언패킹
        c_node, c_time= c_state

        # 현재 노드를 탐색 완료 목록에 추가
        closed_list.add(c_state)
        
        # 현재 노드가 목표 노드라면 경로를 만들고 종료
        if c_node == g_node: 
            path_state = c_state
            while path_state in parents:
                path.append(path_state[0]) 
                path_state = parents[path_state]
            
            # 경로 뒤집기 (시작 -> 목표 순으로)
            path.reverse()      
            
            # 최종경로, cost를 return하며 함수 종료
            return (path, g_costs[c_state])
        

        #branching factor b
        possible_moves = graph.get(c_node,[]) + [(c_node, 1)]
        #state기반 충돌 확인.
        for n_node, move_cost in possible_moves:
            #다음상태 정의
            n_time=c_time+ 1
            n_state= (n_node, n_time)

            #제약조건 확인 로직
            # 1. 정점 제약 조건 확인
            if n_state in constraints:
                continue

            # 2. 간선 제약 조건 확인
            is_edge_constrained = False
            for constraint in constraints:
                # 제약의 형태를 확인하여 간선 제약인지 식별
                if isinstance(constraint, tuple) and len(constraint) == 2 and isinstance(constraint[0], tuple):
                    #간선제약 언패킹
                    edge, departure_time = constraint
                    # 현재 이동(c_node -> n_node)이 제약된 간선과 같고, 출발 시간이 같은지 확인
                    if (c_node, n_node) == edge and c_time == departure_time:
                        is_edge_constrained = True
                        break 
            
            if is_edge_constrained:
                continue

            #이미 탐색이 끝난 상태인지 확인
            if n_state in closed_list:
                continue
            
            #cost function 계산
            gn= g_costs[c_state] + move_cost
            hn = distance(n_node, g_node)
            fn = gn + hn
        
            # 기존에 발견된 경로보다 더 좋은 경로가 아니면 무시
            if n_state in g_costs and gn >= g_costs[n_state]:
                continue

            g_costs[n_state] = gn
            parents[n_state]=c_state

            # 새로운 경로 후보를 open_list에 추가
            heapq.heappush(open_list, (fn, n_state))

    return (None, float('inf'))
