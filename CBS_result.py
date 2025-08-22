import csv
import time
import datetime

# 기존 프로젝트에서 필요한 함수들을 가져옵니다.
from utils.random_agents import assign_random_agents
from core_logic.low_level_search import lls
# CBS 메인 로직에 있던 함수/클래스들을 가져오거나,
# 해당 로직 전체를 아래 run_single_cbs_trial 함수 안으로 옮깁니다.
from CBS_main import CTNode, detect_conflict, cal_sic, graph 
import heapq

# --- 1. 실험 설정 (Experiment Configuration) ---
# 테스트하고 싶은 에이전트 수 목록
AGENT_COUNTS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] 
# 각 에이전트 수마다 반복할 실험 횟수
NUM_TRIALS = 20
# 타임아웃 시간 (초)
TIME_LIMIT_SECONDS = 180
# 결과가 저장될 파일 이름
# 파일 이름에 날짜와 시간을 포함하여 이전 결과가 덮어쓰이는 것을 방지
timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
OUTPUT_FILENAME = f'results/experiment_results_{timestamp}.csv'


def run_single_cbs_trial(graph_map, agents_config, time_limit):
    """
    단일 CBS 실험을 실행하고 결과를 반환하는 함수.
    기존 CBS_main.py의 핵심 로직을 이 함수 안으로 가져왔습니다.
    """
    open_list = []
    solution = None
    nodes_processed = 0
    
    # 루트 노드 생성
    root_constraints = {idx: set() for idx in agents_config.keys()}
    root_solution = {}
    all_initial_paths_found = True

    for idx, agent_info in agents_config.items():
        path, _ = lls(agent_info['start'], agent_info['goal'], root_constraints[idx], graph_map)
        if path is None:
            all_initial_paths_found = False
            break
        root_solution[idx] = path

    if all_initial_paths_found:
        root = CTNode(root_constraints, root_solution, cal_sic(root_solution))
        heapq.heappush(open_list, root)

    start_time = time.time()
    
    while open_list:
        if time.time() - start_time > time_limit:
            # 타임아웃
            return {'success': 0, 'runtime': time.time() - start_time, 'nodes_expanded': nodes_processed, 'cost': -1}

        c_node = heapq.heappop(open_list)
        nodes_processed += 1
        
        conflict = detect_conflict(c_node.solution)
        
        if conflict is None:
            # 성공
            return {'success': 1, 'runtime': time.time() - start_time, 'nodes_expanded': nodes_processed, 'cost': c_node.cost}
        
        agent1_idx, agent2_idx = conflict['agents']
        conflict_time = conflict['time']

        if conflict['type'] == 'vertex':
            node = conflict['loc']
            constraints_to_add = {
                agent1_idx: (node, conflict_time),
                agent2_idx: (node, conflict_time)
            }
        elif conflict['type'] == 'edge':
            edge1 = conflict['loc']
            edge2 = edge1[::-1]
            constraints_to_add = {
                agent1_idx: (edge1, conflict_time),
                agent2_idx: (edge2, conflict_time)
            }
        
        for agent_idx, new_constraint in constraints_to_add.items():
            new_constraints = {k: set(v) for k, v in c_node.constraints.items()}
            new_constraints[agent_idx].add(new_constraint)
            
            new_path, _ = lls(agents_config[agent_idx]['start'], agents_config[agent_idx]['goal'], new_constraints[agent_idx], graph_map)
            
            if new_path is not None:
                new_paths = c_node.solution.copy()
                new_paths[agent_idx] = new_path
                child_node = CTNode(new_constraints, new_paths, cal_sic(new_paths))
                heapq.heappush(open_list, child_node)
                
    # 해를 찾지 못하고 open_list가 비어버린 경우
    return {'success': 0, 'runtime': time.time() - start_time, 'nodes_expanded': nodes_processed, 'cost': -1}


# --- 2. 실험 실행 루프 ---
# CSV 파일을 열고 헤더(첫 줄)를 작성합니다.
with open(OUTPUT_FILENAME, 'w', newline='', encoding='utf-8') as csvfile:
    # 필드 이름(엑셀의 열 제목)을 정의합니다.
    fieldnames = ['Algorithm', 'Num_Agents', 'Trial_ID', 'Success (1/0)', 'Runtime (s)', 'Nodes_Expanded', 'Cost']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    print("🚀 실험을 시작합니다...")
    # 설정된 에이전트 수 목록을 순회합니다.
    for num_agents in AGENT_COUNTS:
        print(f"\n--- {num_agents}명의 에이전트로 실험 진행 ({NUM_TRIALS}회) ---")
        # 각 에이전트 수마다 설정된 횟수만큼 반복합니다.
        for trial in range(1, NUM_TRIALS + 1):
            try:
                # 매번 새로운 랜덤 에이전트를 생성합니다.
                agents = assign_random_agents(graph, num_agents)
                print(f"  Trial {trial}/{NUM_TRIALS}... ", end="")
                
                # CBS 실험을 1회 실행하고 결과를 받습니다.
                result = run_single_cbs_trial(graph, agents, TIME_LIMIT_SECONDS)
                
                # 결과 행을 준비합니다.
                row_data = {
                    'Algorithm': 'CBS',
                    'Num_Agents': num_agents,
                    'Trial_ID': trial,
                    'Success (1/0)': result['success'],
                    'Runtime (s)': f"{result['runtime']:.4f}",
                    'Nodes_Expanded': result['nodes_expanded'],
                    'Cost': result['cost']
                }
                
                # CSV 파일에 한 줄을 작성합니다.
                writer.writerow(row_data)
                
                if result['success']:
                    print(f"성공 (시간: {result['runtime']:.2f}s, 노드: {result['nodes_expanded']})")
                else:
                    print(f"실패 (시간 초과 또는 해 없음)")

            except ValueError as e:
                print(f"에이전트 생성 실패: {e}")
                break # 더 이상 진행 불가

print(f"\n✅ 모든 실험 완료! 결과가 '{OUTPUT_FILENAME}' 파일에 저장되었습니다.")