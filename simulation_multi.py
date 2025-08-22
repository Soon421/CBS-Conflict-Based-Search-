import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.animation import FuncAnimation
# find_obstacle_rectangles 함수는 mapping.py 같은 별도 파일에 있다고 가정합니다.
from mapping import find_obstacle_rectangles

def sim_multi(solution, agents, graph, map_width=9, map_height=10):
    """
    다중 에이전트의 경로를 '보간'을 통해 부드럽게 시각화합니다.
    """
    fig, ax = plt.subplots(figsize=(map_width / 1.5, map_height / 1.5))

    # 1. 애니메이션 속도 조절 파라미터 
    # 각 프레임 사이의 대기 시간 (ms). 작을수록 빨라집니다.
    interval_ms = 5  #초기값 20
    # 한 스텝(노드->노드)을 몇 개의 중간 프레임으로 나눌지 결정. 작을수록 이동이 빠르고, 클수록 부드럽고 느려집니다.
    sub_frames_per_step = 7 #초기값 15
   


    # 에이전트별 색상 지정
    colors = ['orange', 'cyan', 'magenta', 'green', 'yellow', 'purple']
    agent_colors = {idx: colors[i % len(colors)] for i, idx in enumerate(agents.keys())}

    # --- 2. 배경 그리기 (고정 요소) ---
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

    for idx, agent_info in agents.items():
        color = agent_colors[idx]
        s_node = agent_info['start']
        g_node = agent_info['goal']
        ax.plot(s_node[0], s_node[1], 's', color=color, markersize=10, label=f'Agent {idx} Start', zorder=3)
        ax.plot(g_node[0], g_node[1], 's', color=color, markersize=12, label=f'Agent {idx} Goal', zorder=3)

    ax.set_xlim(-0.5, map_width - 0.5)
    ax.set_ylim(-0.5, map_height - 0.5)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks(np.arange(0, map_width, 1))
    ax.set_yticks(np.arange(0, map_height, 1))
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1.02))
    fig.tight_layout(rect=[0, 0, 0.85, 1])

    # --- 3. 애니메이션을 위한 '아티스트' 초기화 ---
    max_len = max(len(p) for p in solution.values()) if solution else 0
    agent_artists = {}

    for idx, path in solution.items():
        color = agent_colors[idx]
        start_pos = path[0]
        marker, = ax.plot(start_pos[0], start_pos[1], 'o', color=color, markersize=12, markeredgecolor='black', zorder=5)
        line, = ax.plot([start_pos[0]], [start_pos[1]], '-', color=color, linewidth=3, alpha=0.7, zorder=4)
        text = ax.text(start_pos[0], start_pos[1], str(idx), color='black', ha='center', va='center', fontweight='bold', fontsize=8, zorder=6)
        agent_artists[idx] = {'marker': marker, 'line': line, 'text': text}

    ax.set_title("Multi-Agent Path Planning")

    # --- 4. 애니메이션 업데이트 함수 정의 ---
    def update(frame):
        time_step = frame // sub_frames_per_step
        sub_frame_idx = frame % sub_frames_per_step

        for idx, path in solution.items():
            start_node = path[time_step] if time_step < len(path) else path[-1]
            end_node = path[time_step + 1] if time_step + 1 < len(path) else start_node

            alpha = sub_frame_idx / sub_frames_per_step

            interp_x = start_node[0] * (1 - alpha) + end_node[0] * alpha
            interp_y = start_node[1] * (1 - alpha) + end_node[1] * alpha

            artists = agent_artists[idx]
            artists['marker'].set_data([interp_x], [interp_y])
            artists['text'].set_position((interp_x, interp_y))

            path_x = [p[0] for p in path[:time_step + 1]] + [interp_x]
            path_y = [p[1] for p in path[:time_step + 1]] + [interp_y]
            artists['line'].set_data(path_x, path_y)

        ax.set_title(f"Multi-Agent Path Planning (Time: {time_step})")

    # --- 5. 애니메이션 실행 ---
    total_frames = (max_len - 1) * sub_frames_per_step if max_len > 1 else 1
    ani = FuncAnimation(fig, update, frames=total_frames, interval=interval_ms, blit=False, repeat=False)

    plt.show()