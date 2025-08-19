#CBS Main
import heapq
import math
from simulation_multi import sim_multi
from low_level_search import lls

# 그래프{해당노드:(이웃노드, cost)}, Basic map
# graph = {
#     #Row0
#     (1, 0): [((1, 1), 1)],
#     (3, 0): [((3, 1), 1)],
#     (5, 0): [((5, 1), 1)],
#     (7, 0): [((7, 1), 1)],
#     #Row1
#     (1, 1): [((1, 2), 1), ((1, 0), 1), ((2, 1), 1)],
#     (2, 1): [((1, 1), 1), ((3, 1), 1)],
#     (3, 1): [((3, 2), 1), ((3, 0), 1), ((2, 1), 1)],
#     (5, 1): [((5, 2), 1), ((5, 0), 1)],
#     (7, 1): [((7, 2), 1), ((7, 0), 1)],
#     #Row2
#     (1, 2): [((1, 3), 1), ((1, 1), 1)],
#     (3, 2): [((3, 3), 1), ((3, 1), 1)],
#     (5, 2): [((5, 3), 1), ((5, 1), 1)],
#     (7, 2): [((7, 3), 1), ((7, 1), 1)],
#     #Row3
#     (1, 3): [((1, 4), 1), ((1, 2), 1)],
#     (3, 3): [((3, 4), 1), ((3, 2), 1)],
#     (5, 3): [((5, 4), 1), ((5, 2), 1), ((6, 3), 1)],
#     (6, 3): [((6, 4), 1), ((5, 3), 1), ((7, 3), 1)],
#     (7, 3): [((7, 4), 1), ((7, 2), 1), ((6, 3), 1)],
#     #Row4
#     (1, 4): [((1, 5), 1), ((1, 3), 1), ((2, 4), 1)],
#     (2, 4): [((2, 5), 1), ((1, 4), 1), ((3, 4), 1)],
#     (3, 4): [((3, 5), 1), ((3, 3), 1), ((2, 4), 1), ((4, 4), 1)],
#     (4, 4): [((4, 5), 1), ((3, 4), 1), ((5, 4), 1)],
#     (5, 4): [((5, 5), 1), ((5, 3), 1), ((4, 4), 1), ((6, 4), 1)],
#     (6, 4): [((6, 5), 1), ((6, 3), 1), ((5, 4), 1), ((7, 4), 1)],
#     (7, 4): [((7, 5), 1), ((7, 3), 1), ((6, 4), 1)],
#     #Row5
#     (1, 5): [((1, 6), 1), ((1, 4), 1), ((2, 5), 1)],
#     (2, 5): [((2, 4), 1), ((1, 5), 1), ((3, 5), 1)],
#     (3, 5): [((3, 6), 1), ((3, 4), 1), ((2, 5), 1), ((4, 5), 1)],
#     (4, 5): [((4, 4), 1), ((3, 5), 1), ((5, 5), 1)],
#     (5, 5): [((5, 6), 1), ((5, 4), 1), ((4, 5), 1), ((6, 5), 1)],
#     (6, 5): [((6, 4), 1), ((5, 5), 1), ((7, 5), 1)],
#     (7, 5): [((7, 6), 1), ((7, 4), 1), ((6, 5), 1)],
#     #Row6
#     (1, 6): [((1, 7), 1), ((1, 5), 1)],
#     (3, 6): [((3, 7), 1), ((3, 5), 1)],
#     (5, 6): [((5, 7), 1), ((5, 5), 1)],
#     (7, 6): [((7, 7), 1), ((7, 5), 1)],
#     #Row7
#     (1, 7): [((1, 8), 1), ((1, 6), 1)],
#     (3, 7): [((3, 6), 1)],
#     (5, 7): [((5, 8), 1), ((5, 6), 1)],
#     (7, 7): [((7, 8), 1), ((7, 6), 1)],
#     #Row8
#     (1, 8): [((1, 9), 1), ((1, 7), 1)],
#     (5, 8): [((5, 9), 1), ((5, 7), 1), ((6, 8), 1)],
#     (6, 8): [((5, 8), 1), ((7, 8), 1)],
#     (7, 8): [((7, 9), 1), ((7, 7), 1), ((6, 8), 1)],
#     #Row9
#     (1, 9): [((1, 8), 1)],
#     (3, 9): [((4, 9), 1)],
#     (4, 9): [((3, 9), 1), ((5, 9), 1)],
#     (5, 9): [((5, 8), 1), ((4, 9), 1)],
#     (7, 9): [((7, 8), 1)],
# }
# 복도좁은 map
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

#N Node
class CTNode:
    def __init__(self, constraints, solution, cost):
        self.constraints = constraints
        self.cost = cost
        self.solution = solution 

    def __lt__(self, other):
        # heapq에서 비용을 기준으로 노드를 정렬하기 위한 비교 연산자.
        return self.cost< other.cost
    
#충돌감지
def detect_conflict(solution):
    if solution:
        max_len = max(len(p) for p in solution.values()) 
    else:
        max_len = 0

   
    for t in range(max_len):
        edges_at_time_t = {}
        positions_at_time_t = {}
        for agent_idx, path in solution.items():
             # 1. 간선 충돌(Edge Conflict) 확인
            if t + 1 < len(path):
                edge = (path[t], path[t+1])
                # 반대 방향 간선이 이미 있는지 확인 (A->B 와 B->A)
                if edge[::-1] in edges_at_time_t:
                    other_agent_idx = edges_at_time_t[edge[::-1]]
                    return {'type': 'edge', 'agents': [agent_idx, other_agent_idx], 'loc': edge, 'time': t}
                edges_at_time_t[edge] = agent_idx
            
             # 2. 정점 충돌(Vertex Conflict) 확인
            if t < len(path):
                pos = path[t]  
            else:
                pos= path[-1]
                
            if pos in positions_at_time_t:
                other_agent_idx = positions_at_time_t[pos]
                return {'type': 'vertex', 'agents': [agent_idx, other_agent_idx], 'loc': pos, 'time': t}
            positions_at_time_t[pos] = agent_idx
    

    return None

#SIC계산
def cal_sic(solution):
    return sum(len(p)- 1 for p in solution.values())

##High-level 메인 알고리즘, Conflict Tree
open_list= []
solution= None
all_initial_paths_found = True
#탐색노드
nodes_processed = 0

#디버깅용 변수
last_cost = -1
iterations_in_cost = 0
LOOP_DETECTION_THRESHOLD = 50000 # 5만번 동안 비용이 그대로면 루프 상태로 간주
detailed_logging = False

#루트 노드 생성
#agent별 빈 제약조건
root_constraints = {idx: set() for idx in agents.keys()}
#빈 solution
root_solution={}

#각 agent에 대해 제약 조건 없이 low-level search
for idx, agent_info in agents.items():
    solution, _ = lls(agent_info['start'], agent_info['goal'],root_constraints[idx], graph)
    #lls로 충돌고려없는 최적의 길을 찾지 못한 경우
    if solution is None:
        all_initial_paths_found = False
        break
    #최적의 길을 찾은 경우 solution 업데이트
    root_solution[idx] = solution

#루트노드 작성
if all_initial_paths_found:
    root = CTNode(root_constraints, root_solution, cal_sic(root_solution))
    heapq.heappush(open_list, root)

#High Level 탐색(CT)
try:
    while open_list:
        # 비용이 가장 낮은 노드를 꺼냄
        c_node = heapq.heappop(open_list)

        nodes_processed += 1

               # --- 루프 감지 및 디버깅 로직 ---
        if c_node.cost > last_cost:
            # 비용이 증가했으므로 상태 초기화
            if last_cost != -1: # 맨 처음 실행시에는 출력하지 않음
                print(f"\n✅ 비용 증가: {last_cost} -> {c_node.cost} (탐색한 노드: {nodes_processed})")
            last_cost = c_node.cost
            iterations_in_cost = 0
            detailed_logging = False # 상세 로깅 비활성화
        else:
            # 같은 비용 내에서 탐색 계속
            iterations_in_cost += 1

        # 만약 루프가 의심되면, 상세 로깅 시작
        if not detailed_logging and iterations_in_cost > LOOP_DETECTION_THRESHOLD:
            print("\n" + "!"*60)
            print(f"⚠️  경고: 비용 {c_node.cost}에서 {iterations_in_cost}번 이상 머물러 있습니다. 무한 루프가 의심됩니다.")
            print("지금부터 상세 로깅을 시작합니다...")
            print("!"*60 + "\n")
            detailed_logging = True
        
        # 충돌은 여기서 한 번만 확인합니다.
        conflict = detect_conflict(c_node.solution)

        # 상세 로깅이 활성화된 경우, 모든 정보 출력
        if detailed_logging:
            print(f"--- [상세 로그] 노드 #{nodes_processed} (Cost: {c_node.cost}) ---")
            
            if conflict:
                print(f"  > 현재 충돌: {conflict}")
            else:
                print("  > 현재 충돌 없음")

            print("  > 에이전트별 경로:")
            for agent_id, path in c_node.solution.items():
                print(f"    - Agent {agent_id}: {path}")
            print("-" * 60)
        
        # 충돌여부확인
        conflict = detect_conflict(c_node.solution)
        
        # 충돌이 없으면 성공 
        if conflict is None:
            print("경로를 찾았습니다")
            solution = c_node.solution
            break

        #충돌 시 알고리즘
        agent1_idx, agent2_idx = conflict['agents']
        time = conflict['time']

        if conflict['type'] == 'vertex':
            node = conflict['loc']
            if not detailed_logging:
                print(f"정점 충돌 감지(현재 비용: {c_node.cost}): Agent {agent1_idx}와 {agent2_idx}가 시간 {time}에 노드 {node}에서 충돌")
            constraints_to_add = {
                agent1_idx: (node, time),
                agent2_idx: (node, time)
            }
        elif conflict['type'] == 'edge':
            edge1 = conflict['loc']
            edge2 = edge1[::-1] # (u, v) -> (v, u)
            if not detailed_logging:
                print(f"간선 충돌 감지(현재 비용: {c_node.cost}): Agent {agent1_idx}와 {agent2_idx}가 시간 {time}에 간선 {edge1}에서 충돌")
            constraints_to_add = {
                agent1_idx: (edge1, time),
                agent2_idx: (edge2, time)
            }
            

        # 충돌 발생 시, 두 개의 자식 노드 생성 
        for agent_idx, new_constraint in constraints_to_add.items():
            # 새로운 제약 조건 추가
            new_constraints = {k: set(v) for k, v in c_node.constraints.items()}
            new_constraints[agent_idx].add(new_constraint)
            
            # 제약이 추가된 에이전트의 경로만 다시 계산
            new_path, _ = lls(agents[agent_idx]['start'], agents[agent_idx]['goal'], new_constraints[agent_idx], graph)
            
            if new_path is not None:
                #부모의 전체 solution 복사
                new_paths = c_node.solution.copy()
                #수정한 path만 교체
                new_paths[agent_idx] = new_path
                
                # 새로운 자식 노드를 open_list에 추가
                child_node = CTNode(new_constraints, new_paths, cal_sic(new_paths))
                heapq.heappush(open_list, child_node)

except KeyboardInterrupt: 
    print("\n\n[사용자 요청으로 탐색 중단]")

finally: 
    print(f"탐색된 총 노드의 수: {nodes_processed}개")

#결과출력
if solution:
    for agent_idx, path in solution.items():
        print(f"Agent {agent_idx}의 경로: {path}")
        print(f"Agent {agent_idx}의 비용: {len(path) - 1}")

    print(f"총 비용 (Sum of Costs): {cal_sic(solution)}")
    sim_multi(solution, agents, graph)
else:
    print("해법을 찾지 못했습니다.")
