def move_zombie_towards_player(zombie, player, walls):
    start = (zombie.xcor(), zombie.ycor())
    goal = (player.xcor(), player.ycor())
    
    path = dijkstra(start, goal, walls)
    
    if path:
        next_position = path[1]  # Zombie follows the path found
        zombie.goto(next_position[0], next_position[1])