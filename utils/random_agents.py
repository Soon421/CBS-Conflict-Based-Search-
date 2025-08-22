import random

def assign_random_agents(graph, num_agents):
    """
    Randomly assigns unique start and goal nodes to a given number of agents.

    Args:
        graph (dict): The dictionary representing the map's walkable nodes and connections.
        num_agents (int): The number of agents to create.

    Returns:
        dict: A dictionary of agents with their assigned start and goal nodes.
              Example: {1: {'start': (x1, y1), 'goal': (g1, h1)}, ...}
    
    Raises:
        ValueError: If there aren't enough unique nodes in the graph for the
                    requested number of agents.
    """
    # 1. Get all available walkable nodes from the graph keys.
    walkable_nodes = list(graph.keys())
    
    # 2. Check if there are enough unique nodes for all agents' starts and goals.
    required_nodes = num_agents * 2
    if len(walkable_nodes) < required_nodes:
        raise ValueError(
            f"Error: Not enough nodes available ({len(walkable_nodes)}) "
            f"to assign unique start/goal positions to {num_agents} agents. "
            f"Required: {required_nodes} nodes."
        )
        
    # 3. Randomly select the required number of unique nodes without replacement.
    selected_nodes = random.sample(walkable_nodes, k=required_nodes)
    
    # 4. Create the agents dictionary by assigning a start and goal to each agent.
    agents = {}
    for i in range(num_agents):
        agent_id = i + 1
        # Pop nodes from the list to ensure each is used only once.
        start_node = selected_nodes.pop()
        goal_node = selected_nodes.pop()
        agents[agent_id] = {'start': start_node, 'goal': goal_node}
        
    return agents