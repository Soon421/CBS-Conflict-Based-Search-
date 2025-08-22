import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
# find_obstacle_rectangles 함수는 mapping.py 같은 별도 파일에 있다고 가정합니다.
from utils.mapping import find_obstacle_rectangles 

def sim(path, s_node, g_node, graph, map_width=9, map_height=9):
    """
    모든 시각 요소를 격자 선에 맞춰 그리고, 장애물을 올바르게 표시합니다.
    """
    plt.ion()
    fig, ax = plt.subplots(figsize=(map_width / 1.5, map_height / 1.5))

    # --- 1. 배경 그리기 (고정 요소) ---
    
    # === 장애물 그리기  ===
    walkable_nodes = set(graph.keys())
    obstacle_rects = find_obstacle_rectangles(map_width, map_height, walkable_nodes)
    
    for rect_info in obstacle_rects:
        (x, y), w, h = rect_info
        # 사각형의 시작점을 -0.5씩 이동하여 격자점 중앙에 위치시킴
        obstacle = patches.Rectangle((x - 0.5, y - 0.5), w, h, facecolor='dimgray', edgecolor='black', zorder=1)
        ax.add_patch(obstacle)

    # 이동 가능 노드에 점 그리기 
    for node in walkable_nodes:
        # 노드 중앙에 희미한 흰색 점을 그림
        ax.plot(node[0] , node[1] , '.', color='black', alpha=0.4, markersize=6)
    
    # 이동 가능 경로(길) 그리기
    for node, neighbors in graph.items():
        for neighbor, _ in neighbors:
            ax.plot([node[0], neighbor[0]], [node[1], neighbor[1]], '-', color='black', alpha=0.3, zorder=0)

    # 시작점과 목표점
    ax.plot(s_node[0], s_node[1], 's', color='blue', markersize=10, label='Start', zorder=3)
    ax.plot(g_node[0], g_node[1], 's', color='red', markersize=10, label='Goal', zorder=3)

    # --- 그래프 기본 설정 ---
    # 축 범위를 조정하여 가장자리 장애물이 잘 보이지 않게 함
    ax.set_xlim(-0.5, map_width - 0.5)
    ax.set_ylim(-0.5, map_height - 0.5)
    ax.set_aspect('equal', adjustable='box')
    
    # 주 눈금 라벨은 정수로 표시
    ax.set_xticks(np.arange(0, map_width, 1))
    ax.set_yticks(np.arange(0, map_height, 1))


    # 범례 위치 조정
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1.02))
    fig.tight_layout(rect=[0, 0, 0.85, 1])
    
    dynamic_artists = []

    # --- 2. 애니메이션 루프 (움직이는 요소) ---
    for i in range(len(path)):
        for artist in dynamic_artists:
            artist.remove()
        dynamic_artists = []

        # 현재까지 지나온 경로
        path_x = [p[0] for p in path[:i+1]]
        path_y = [p[1] for p in path[:i+1]]
        line, = ax.plot(path_x, path_y, '-', color='cyan', linewidth=4, zorder=4)
        dynamic_artists.append(line)
        
        # 에이전트의 현재 위치
        current_node = path[i]
        agent, = ax.plot(current_node[0], current_node[1], 'o', color='orange', markersize=12, zorder=5)
        dynamic_artists.append(agent)

        ax.set_title(f"Path Planning (Time: {i})")

        plt.pause(1.0)

    plt.ioff()
    plt.show()

