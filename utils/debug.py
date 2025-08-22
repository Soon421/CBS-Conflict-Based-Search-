import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Your agent path data
solution = {
    1: [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (7, 5), (7, 6), (7, 7)],
    2: [(7, 8), (7, 7), (7, 6), (7, 5), (7, 5), (7, 4), (7, 4), (7, 4), (6, 4), (6, 4), (5, 4), (4, 4), (3, 4), (2, 4), (1, 4), (1, 3), (1, 2), (1, 1), (1, 0)],
    3: [(7, 0), (7, 1), (7, 2), (7, 3), (6, 3), (6, 3), (7, 3), (7, 3), (6, 3), (5, 3), (5, 4), (4, 4), (3, 4), (2, 4)],
    4: [(1, 2), (1, 3), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8)],
    5: [(1, 8), (1, 7), (1, 6), (1, 5), (2, 5), (3, 5), (3, 5), (3, 4), (4, 4), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (4, 8), (3, 8)]
}

# Your graph data to draw the map layout
graph = {
    (1, 0): [((1, 1), 1)], (3, 0): [((3, 1), 1)], (5, 0): [((5, 1), 1)], (7, 0): [((7, 1), 1)],
    (1, 1): [((1, 2), 1), ((1, 0), 1), ((2, 1), 1)], (2, 1): [((1, 1), 1), ((3, 1), 1)], (3, 1): [((3, 2), 1), ((3, 0), 1), ((2, 1), 1)], (5, 1): [((5, 2), 1), ((5, 0), 1)], (7, 1): [((7, 2), 1), ((7, 0), 1)],
    (1, 2): [((1, 3), 1), ((1, 1), 1)], (3, 2): [((3, 3), 1), ((3, 1), 1)], (5, 2): [((5, 3), 1), ((5, 1), 1)], (7, 2): [((7, 3), 1), ((7, 1), 1)],
    (1, 3): [((1, 4), 1), ((1, 2), 1)], (3, 3): [((3, 4), 1), ((3, 2), 1)], (5, 3): [((5, 4), 1), ((5, 2), 1), ((6, 3), 1)], (6, 3): [((6, 4), 1), ((5, 3), 1), ((7, 3), 1)], (7, 3): [((7, 4), 1), ((7, 2), 1), ((6, 3), 1)],
    (1, 4): [((1, 5), 1), ((1, 3), 1), ((2, 4), 1)], (2, 4): [((1, 4), 1), ((3, 4), 1), ((2, 5),1)], (3, 4): [((3, 5), 1), ((3, 3), 1), ((2, 4), 1), ((4, 4), 1)], (4, 4): [((3, 4), 1), ((5, 4), 1)], (5, 4): [((5, 5), 1), ((5, 3), 1), ((4, 4), 1), ((6, 4), 1)], (6, 4): [((6, 3), 1), ((5, 4), 1), ((7, 4), 1)], (7, 4): [((7, 5), 1), ((7, 3), 1), ((6, 4), 1), ((8,4), 1)], (8, 4): [((7, 4), 1)],
    (1, 5): [((1, 6), 1), ((1, 4), 1),((2, 5),1)], (2, 5): [((1, 5), 1), ((2, 4), 1), ((3, 5),1)], (3, 5): [((3, 6), 1), ((3, 4), 1), ((2, 5),1)], (5, 5): [((5, 6), 1), ((5, 4), 1)], (7, 5): [((7, 6), 1), ((7, 4), 1)],
    (1, 6): [((1, 7), 1), ((1, 5), 1)], (3, 6): [((3, 5), 1)], (5, 6): [((5, 7), 1), ((5, 5), 1)], (7, 6): [((7, 7), 1), ((7, 5), 1)],
    (1, 7): [((1, 8), 1), ((1, 6), 1)], (5, 7): [((5, 8), 1), ((5, 6), 1), ((6, 7), 1)], (6, 7): [((5, 7), 1), ((7, 7), 1)], (7, 7): [((7, 8), 1), ((7, 6), 1), ((6, 7), 1)],
    (1, 8): [((1, 7), 1)], (3, 8): [((4, 8), 1)], (4, 8): [((3, 8), 1), ((5, 8), 1)], (5, 8): [((5, 7), 1), ((4, 8), 1)], (7, 8): [((7, 7), 1)]
}


# --- Visualization Setup ---
fig, ax = plt.subplots(figsize=(10, 10))

# Find map boundaries
all_nodes = list(graph.keys())
min_x = min(node[0] for node in all_nodes) - 1
max_x = max(node[0] for node in all_nodes) + 1
min_y = min(node[1] for node in all_nodes) - 1
max_y = max(node[1] for node in all_nodes) + 1

ax.set_xlim(min_x, max_x)
ax.set_ylim(min_y, max_y)
ax.set_aspect('equal')
ax.set_xticks(range(min_x, max_x + 1))
ax.set_yticks(range(min_y, max_y + 1))
ax.grid(True, which='both', linestyle='--', linewidth=0.5)

# Draw the graph connections (the map)
for node, neighbors in graph.items():
    for neighbor, _ in neighbors:
        ax.plot([node[0], neighbor[0]], [node[1], neighbor[1]], color='gray', linewidth=0.75, zorder=1)

# Agent colors
colors = plt.cm.get_cmap('tab10', len(solution))
agent_artists = []
for i in range(len(solution)):
    # Create a circle for the agent
    circle = plt.Circle((0, 0), 0.3, color=colors(i), zorder=3)
    # Create a text label for the agent number
    label = ax.text(0, 0, str(i + 1), ha='center', va='center', color='white', weight='bold', fontsize=10, zorder=4)
    agent_artists.append({'circle': circle, 'label': label})
    ax.add_patch(circle)

# Time text display
time_template = 'Time = %d'
time_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, fontsize=14)

# Find the maximum path length for the animation duration
max_len = max(len(p) for p in solution.values())

# --- Animation Function ---
def animate(t):
    # Update agent positions
    for i, (agent_id, path) in enumerate(solution.items()):
        # If the agent's path is shorter than the current time, it stays at its goal
        pos_index = min(t, len(path) - 1)
        pos = path[pos_index]
        
        agent_artists[i]['circle'].set_center(pos)
        agent_artists[i]['label'].set_position(pos)
    
    # Update time text
    time_text.set_text(time_template % t)
    
    # Return a list of all artists that were updated
    return [artist['circle'] for artist in agent_artists] + [artist['label'] for artist in agent_artists] + [time_text]

# --- Run Animation ---
# 'interval' controls the speed of the animation (milliseconds per frame)
# 'frames' is the total number of steps in the animation
ani = animation.FuncAnimation(fig, animate, frames=max_len, interval=300, blit=True, repeat=False)

plt.show()