#a_star, 가볍게 A* 구현해보기
import heapq
import math
import matplotlib.pyplot as plt

def distance(node1, node2):
    x1, y1 = node1
    x2, y2 = node2
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)   

# 그래프{해당노드:(이웃노드, cost)}, map은 바뀔 예정
graph = {
    (0, 0): [((0, 1),1)],
    (0, 1): [((0, 0),1), ((-1, 2),1.4), ((1, 2),1.4)],
    (-1,2): [((0, 1),1.4), ((1, 2),2), ((0,3),1.4), ((-2,3),1.4), ((-1,4),2)],
    (1,2): [((0, 1),1.4), ((-1, 2),2), ((0,3),1.4), ((2,3),1.4), ((1,4),2)],
    (0,3): [((-1, 2),1.4), ((1, 2),1.4), ((-1, 4),1.4), ((1, 4),1.4)],
    (-2,3):[((-1, 2),1.4), ((-1, 4),1.4), ((-3, 3),1)],
    (2,3):[((1, 2),1.4), ((1, 4),1.4), ((3, 3),1)],
    (-3,3):[((-2, 3),1)],
    (3,3):[((-2, 3),1)],
    (-1,4): [((0, 5),1.4), ((1, 4),2), ((0,3),1.4), ((-2,3),1.4), ((-1,2),2)],
    (1,4): [((0, 5),1.4), ((-1, 4),2), ((0,3),1.4), ((2,3),1.4), ((1,2),2)],
    (0, 5): [((0, 6),1), ((-1, 4),1.4), ((1, 4),1.4)],
    (0, 6): [((0, 5),1)]
}


# 초기 설정
s_node = (0, 0)
xg=int(input("목표지점의 x좌표를 입력하시오"))
yg=int(input("목표지점의 y좌표를 입력하시오"))
g_node = (xg, yg)

# open_list를 우선순위 큐로 사용.
# (f(n)값, 노드) 형태로 저장. 시작 노드의 f(n) = h(n)
open_list = [(distance(s_node, g_node), s_node)]
# 닫힌 목록은 중복 조회를 피하기 위해 set 사용
closed_list = set()    
g_costs = {s_node: 0}
#부모노드 기록
parents = {s_node : None}          
 #경로저장
path = []             


# 메인 알고리즘 
# open_list에 탐색할 노드가 남아있는 동안 반복
while open_list: 
    
    # open_list에서 f(n)이 가장 작은 노드를 꺼냄
    c_f, c_node = heapq.heappop(open_list)

    # 먼저 closed_list를 확인하여 중복 탐색을 방지
    if c_node in closed_list:
        continue
        
    # 현재 노드를 탐색 완료 목록에 추가
    closed_list.add(c_node)
    
    # 현재 노드가 목표 노드라면 경로를 만들고 종료
    if c_node == g_node:
        temp_node = g_node
        while temp_node in parents:
            path.append(temp_node)
            temp_node = parents[temp_node]
        # 마지막으로 시작 노드 추가
        path.append(s_node) 
        # 경로 뒤집기 (시작 -> 목표 순으로)
        path.reverse()      
        break
        
    # 현재 노드의 이웃들을 탐색
    for neighbor, cost_from_c_node in graph.get(c_node, []):
        
        # 이미 탐색 완료된 이웃이라면 건너뛰기
        if neighbor in closed_list:
            continue

        # g(n), h(n), f(n) 계산
        gn = g_costs[c_node] + cost_from_c_node
        hn = distance(neighbor, g_node)
        fn = gn + hn
        
        # 기존에 발견된 경로보다 더 좋은 경로가 아니면 무시
        if neighbor in g_costs and gn >= g_costs[neighbor]:
            continue

        # 더 좋은 경로를 찾았으므로 딕셔너리에 정보 업데이트
        g_costs[neighbor] = gn
        parents[neighbor] = c_node
        
        # 새로운 경로 후보를 open_list에 추가
        heapq.heappush(open_list, (fn, neighbor))

if path:
    print(f"최단 경로: {path}")
    print(f"총 비용: {g_costs[g_node]:.2f}")
    for i in range(len(path)):
        current_node = path[i]
        
        # 이전 프레임 지우기
        plt.clf() 
        
        # 배경 맵 그리기
        for node, neighbors in graph.items():
            plt.plot(node[0], node[1], 'o', color='black')
            for neighbor, _ in neighbors:
                plt.plot([node[0], neighbor[0]], [node[1], neighbor[1]], '--', color='black')
        
        # 시작점과 목표점 표시
        plt.plot(s_node[0], s_node[1], 'bs', markersize=10, label='Start')
        plt.plot(g_node[0], g_node[1], 'rs', markersize=10, label='Goal')

        # 전체 최종 경로 미리 그리기
        path_x = [p[0] for p in path]
        path_y = [p[1] for p in path]
        plt.plot(path_x, path_y, '-', color='gold', linewidth=3, alpha=0.5, label='Final Path')

        # 현재까지 지나온 경로 그리기
        sub_path_x = path_x[:i+1]
        sub_path_y = path_y[:i+1]
        plt.plot(sub_path_x, sub_path_y, '-', color='gold', linewidth=4)
        
        # 현재 위치를 큰 점으로 표시
        plt.plot(current_node[0], current_node[1], 'o', color='orange', markersize=12)

        plt.title("Path Planning")
        plt.legend(); plt.grid(True); plt.axis('equal')
        plt.pause(0.5) 

    # 애니메이션이 끝나고 창이 닫히지 않게 함
    plt.ioff(); plt.show() 

    
else:
    print("\n경로를 찾지 못했습니다.")

    
