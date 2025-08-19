import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
# find_obstacle_rectangles 함수는 mapping.py 같은 별도 파일에 있다고 가정합니다.
from mapping import find_obstacle_rectangles 


def sim_multi(solution, agents, graph, map_width=9, map_height=9):
    """
    다중 에이전트의 경로를 동시에 시각화합니다.
    solution: {agent_idx: path, ...} 형태의 딕셔너리
    agents: {agent_idx: {'start': s_node, 'goal': g_node}, ...} 형태의 딕셔너리
    """
    plt.ion()
    fig, ax = plt.subplots(figsize=(map_width / 1.5, map_height / 1.5))

    # 에이전트별 색상 지정
    colors = ['orange', 'cyan', 'magenta', 'green', 'yellow', 'purple']
    agent_colors = {idx: colors[i % len(colors)] for i, idx in enumerate(agents.keys())}
    
    # --- 1. 배경 그리기 (고정 요소) ---
    walkable_nodes = set(graph.keys())
    obstacle_rects = find_obstacle_rectangles(map_width, map_height, walkable_nodes)
    for rect_info in obstacle_rects:
        (x, y), w, h = rect_info
        obstacle = patches.Rectangle((x - 0.5, y - 0.5), w, h, facecolor='dimgray', edgecolor='black', zorder=1)
        ax.add_patch(obstacle)
    
    for node in walkable_nodes:
        ax.plot(node[0], node[1], '.', color='black', alpha=0.4, markersize=6)
    
    for node, neighbors in graph.items():
        for neighbor, _ in neighbors:
            ax.plot([node[0], neighbor[0]], [node[1], neighbor[1]], '-', color='black', alpha=0.3, zorder=0)

    # 모든 에이전트의 시작점과 목표점 그리기
    for idx, agent_info in agents.items():
        color = agent_colors[idx]
        s_node = agent_info['start']
        g_node = agent_info['goal']
        ax.plot(s_node[0], s_node[1], 's', color=color, markersize=10, label=f'Agent {idx} Start', zorder=3)
        ax.plot(g_node[0], g_node[1], 's', color=color, markersize=12, label=f'Agent {idx} Goal', zorder=3)

    # --- 그래프 기본 설정 ---
    ax.set_xlim(-0.5, map_width - 0.5)
    ax.set_ylim(-0.5, map_height - 0.5)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks(np.arange(0, map_width, 1))
    ax.set_yticks(np.arange(0, map_height, 1))
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1.02))
    fig.tight_layout(rect=[0, 0, 0.85, 1])
    
    # --- 2. 애니메이션 루프 (움직이는 요소) ---
    max_len = max(len(p) for p in solution.values()) if solution else 0
    dynamic_artists = []

    for t in range(max_len):
        # 이전 프레임의 움직이는 요소들 삭제
        for artist in dynamic_artists:
            artist.remove()
        dynamic_artists = []

        # 현재 시간 t에서 모든 에이전트의 위치와 경로를 그림
        for agent_idx, path in solution.items():
            color = agent_colors[agent_idx]
            
            # 현재까지 지나온 경로
            path_x = [p[0] for p in path[:t+1]]
            path_y = [p[1] for p in path[:t+1]]
            line, = ax.plot(path_x, path_y, '-', color=color, linewidth=3, alpha=0.7, zorder=4)
            dynamic_artists.append(line)
            
            # 에이전트의 현재 위치
            current_pos = path[t] if t < len(path) else path[-1]
            agent_marker, = ax.plot(current_pos[0], current_pos[1], 'o', color=color, markersize=12, markeredgecolor='black', zorder=5)
            dynamic_artists.append(agent_marker)
            
            # 에이전트 번호 텍스트
            agent_text = ax.text(current_pos[0], current_pos[1], str(agent_idx), color='black',
                                 ha='center', va='center', fontweight='bold', fontsize=8, zorder=6)
            dynamic_artists.append(agent_text)

        ax.set_title(f"Multi-Agent Path Planning (Time: {t})")
        plt.pause(0.6)

    plt.ioff()
    # 최종 경로를 보여주기 위해 마지막 프레임은 유지
    ax.set_title(f"Multi-Agent Path Planning (Final)")
    plt.show()