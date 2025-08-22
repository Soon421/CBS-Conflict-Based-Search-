**Project Title: CBS Algorithm for MAPF**

This repository contains an implementation of the **Conflict-Based Search (CBS)** algorithm, a leading method for efficiently solving the **Multi-Agent Path Finding (MAPF)** problem. The goal is to find optimal, collision-free paths for multiple agents from their starting locations to their respective destinations in a shared environment.

This project explores the core components of CBS, including the low-level search for individual agent paths and the high-level search that resolves conflicts between them. We aim to provide a clear and well-documented implementation for educational and research purposes.

### **Getting Started / Usage**

You can easily test the CBS implementation with your own scenarios.

1.  **Customize the Map:** Create or modify a map file that fits your needs.
2.  **Set the Agent Count:** In the code, both the start and goal positions for each agent are generated randomly on valid map nodes. To run a simulation, you only need to adjust the `number_of_agents_to_create` variable in the `CBS_Main.py` file.
3.  **Run the Simulation:** Execute the main script from your terminal.

<!-- end list -->

```bash
python CBS_Main.py
```
