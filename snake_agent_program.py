def find_nearest_food(snake_head, food_sources):
    # Find the nearest food source based on Manhattan distance
    min_distance = float('inf')
    nearest_food = None
    for food in food_sources:
        # Calculate the Manhattan distance between the snake head and each food source
        distance = calculate_distance(snake_head, food)
        # Update the nearest_food and min_distance if a closer food source is found
        if distance < min_distance:
            min_distance = distance
            nearest_food = food
    return nearest_food

def find_nearest_obstacle(snake_head, obstacles):
    # Find the nearest obstacle based on Manhattan distance
    min_distance = float('inf')
    nearest_obstacle = None
    for obstacle in obstacles:
        # Calculate the Manhattan distance between the snake head and each obstacle
        distance = calculate_distance(snake_head, obstacle)
        # Update the nearest_obstacle and min_distance if a closer obstacle is found
        if distance < min_distance:
            min_distance = distance
            nearest_obstacle = obstacle
    return nearest_obstacle

def is_valid_move(x, y, obstacles, snake_body, display_width, display_height):
    # Check if the move is not hitting a wall or snake's body or an obstacle
    if (x, y) in obstacles or (x, y) in snake_body:
        return False

    # Check if the move is not going beyond the display boundaries
    if x < 0 or x >= display_width or y < 0 or y >= display_height:
        return False

    return True

import heapq
import math

def calculate_distance(coord1, coord2):
    # Calculate the Manhattan distance between two coordinates
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

def heuristic(coord, goal):
    # Calculate the heuristic value (Manhattan distance) between a coordinate and the goal
    return abs(coord[0] - goal[0]) + abs(coord[1] - goal[1])

def astar(start, goal, obstacles, snake_body, display_width, display_height):
    open_set = []
    closed_set = set()
    heapq.heappush(open_set, (0, start))
    came_from = {}

    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            # Reconstruct the path from the start to the goal if the goal is reached
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        closed_set.add(current)

        neighbors = [(current[0] + 1, current[1]),  # Right
                     (current[0] - 1, current[1]),  # Left
                     (current[0], current[1] + 1),  # Down
                     (current[0], current[1] - 1)]  # Up

        for neighbor in neighbors:
            if neighbor in closed_set or neighbor in obstacles or neighbor in snake_body:
                continue

            tentative_g_score = g_score[current] + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []

def snake_agent_program(percepts, actuators):
    snake_body = percepts["body-sensor"]
    food_sources = percepts["food-sensor"]
    obstacles = percepts["obstacles-sensor"]
    remaining_time = percepts["clock"]
    display_width = 640
    display_height = 480

    head_direction = actuators["head"]
    snake_head = snake_body[0]

    nearest_food = find_nearest_food(snake_head, food_sources)
    nearest_obstacle = find_nearest_obstacle(snake_head, obstacles)

    actions = []
    if nearest_food:
        food_x, food_y, _ = nearest_food
        head_x, head_y = snake_head

        path_to_food = astar(snake_head, (food_x, food_y), obstacles, snake_body, display_width, display_height)
        if path_to_food:
            next_x, next_y = path_to_food[0]
            if next_x > head_x:
                actions.append("move-right")
            elif next_x < head_x:
                actions.append("move-left")
            elif next_y > head_y:
                actions.append("move-down")
            elif next_y < head_y:
                actions.append("move-up")
            else:
                actions.append(f"move-{head_direction}")

        if (abs(head_x - food_x) <= 1 and abs(head_y - food_y) <= 1):
            actions.append("open-mouth")
        else:
            actions.append("close-mouth")

    if not actions:
        actions.append(f"move-{head_direction}")

    return actions
