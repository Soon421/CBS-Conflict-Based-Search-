def mapping(walkable_nodes):
    """
    이동 가능한 노드 좌표들의 리스트를 받아,
    연결 관계를 나타내는 graph 딕셔너리를 생성합니다.
    비용(가중치)은 모두 1로 고정됩니다.

    :param walkable_nodes: 이동 가능한 (x, y) 좌표들의 리스트 또는 세트
    :return: 생성된 graph 딕셔너리
    """
    graph = {}
    # 리스트보다 세트(set)를 사용하는 것이 특정 노드가 있는지 확인할 때 훨씬 빠릅니다.
    walkable_set = set(walkable_nodes)

    # 모든 이동 가능 노드에 대해 반복합니다.
    for node in walkable_nodes:
        x, y = node
        neighbors = []
        # 현재 노드를 기준으로 상, 하, 좌, 우 위치를 확인합니다.
        possible_moves = [(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)]

        for move in possible_moves:
            # 이동하려는 위치가 '이동 가능한 노드' 목록에 있는지 확인합니다.
            if move in walkable_set:
                # 비용 포함 형식: ((x, y), 1)
                neighbors.append((move, 1))
        
        # 현재 노드와 연결된 이웃 노드 리스트를 딕셔너리에 추가합니다.
        graph[node] = neighbors
        
    return graph    

def find_obstacle_rectangles(map_width, map_height, walkable_nodes):
    # (이전에 만들었던 장애물 사각형 탐색 함수)
    rectangles = []
    all_nodes = set((x, y) for x in range(map_width) for y in range(map_height))
    obstacle_nodes = all_nodes - set(walkable_nodes)
    visited_obstacles = set()
    for y in range(map_height):
        for x in range(map_width):
            current_node = (x, y)
            if current_node in obstacle_nodes and current_node not in visited_obstacles:
                rect_width = 1
                while (x + rect_width, y) in obstacle_nodes and (x + rect_width, y) not in visited_obstacles:
                    rect_width += 1
                rect_height = 1
                while True:
                    is_expandable = True
                    for i in range(rect_width):
                        if (x + i, y + rect_height) not in obstacle_nodes:
                            is_expandable = False
                            break
                    if is_expandable:
                        rect_height += 1
                    else:
                        break
                rectangles.append(((x, y), rect_width, rect_height))
                for i in range(rect_width):
                    for j in range(rect_height):
                        visited_obstacles.add((x + i, y + j))
    return rectangles

if __name__ == '__main__':
    my_walkable_nodes= [(1,0),(3,0),(5,0),(7,0),
                        (1,1),(2,1),(3,1),(5,1),(7,1),
                        (1,2),(3,2),(5,2),(7,2),
                        (1,3),(3,3),(5,3),(6,3),(7,3),
                        (1,4),(2,4),(3,4),(4,4),(5,4),(6,4),(7,4),
                        (1,5),(3,5),(5,5),(7,5),
                        (1,6),(3,6),(5,6),(7,6),
                        (1,7),(5,7),(6,7),(7,7),
                        (1,8),(3,8),(4,8),(5,8),(7,8)]

    map=mapping(my_walkable_nodes)
    for node, neighbors in map.items():
        print(f"{node}: {neighbors},")


#그래프 예시 모아두기
# graph1 = {
#     # Row 0
#     (0,0): [((1,0), 1), ((0,1), 1)],
#     (1,0): [((0,0), 1), ((2,0), 1), ((1,1), 1)],
#     (2,0): [((1,0), 1), ((3,0), 1), ((2,1), 1)],
#     (3,0): [((2,0), 1), ((4,0), 1), ((3,1), 1)],
#     (4,0): [((3,0), 1), ((5,0), 1), ((4,1), 1)],
#     (5,0): [((4,0), 1), ((5,1), 1)],
#     # Row 1
#     (0,1): [((0,0), 1), ((1,1), 1), ((0,2), 1)],
#     (1,1): [((1,0), 1), ((0,1), 1), ((1,2), 1)],
#     (2,1): [((2,0), 1), ((3,1), 1), ((2,2), 1)],
#     (3,1): [((3,0), 1), ((2,1), 1), ((4,1), 1)],
#     (4,1): [((4,0), 1), ((3,1), 1), ((5,1), 1), ((4,2), 1)],
#     (5,1): [((5,0), 1), ((4,1), 1), ((5,2), 1)],
#     # Row 2
#     (0,2): [((0,1), 1), ((0,3), 1)],
#     (1,2): [((1,1), 1), ((2,2), 1)],
#     (2,2): [((2,1), 1), ((1,2), 1), ((2,3), 1)],
#     (3,2): [((4,2), 1), ((3,3), 1)],
#     (4,2): [((4,1), 1), ((3,2), 1), ((5,2), 1), ((4,3), 1)],
#     (5,2): [((5,1), 1), ((4,2), 1), ((5,3), 1)],
#     # Row 3
#     (0,3): [((0,2), 1), ((1,3), 1), ((0,4), 1)],
#     (1,3): [((0,3), 1), ((2,3), 1)],
#     (2,3): [((2,2), 1), ((1,3), 1), ((3,3), 1), ((2,4), 1)],
#     (3,3): [((3,2), 1), ((2,3), 1), ((4,3), 1), ((3,4), 1)],
#     (4,3): [((4,2), 1), ((3,3), 1), ((5,3), 1)],
#     (5,3): [((5,2), 1), ((4,3), 1), ((5,4), 1)],
#     # Row 4
#     (0,4): [((0,3), 1), ((1,4), 1)],
#     (1,4): [((1,3), 1), ((0,4), 1), ((2,4), 1)],
#     (2,4): [((2,3), 1), ((1,4), 1), ((3,4), 1)],
#     (3,4): [((3,3), 1), ((2,4), 1), ((4,4), 1)],
#     (4,4): [((3,4), 1), ((5,4), 1)],
#     (5,4): [((5,3), 1), ((4,4), 1)]
# }