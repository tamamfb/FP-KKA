import turtle
import math
import random
from collections import deque
import time

# Setup Screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Zombie Maze")
wn.setup(700, 700)
wn.tracer(0)

# Register Shapes
turtle.register_shape("player.gif")
turtle.register_shape("zombie.gif")
turtle.register_shape("wall.gif")
turtle.register_shape("food.gif")
turtle.register_shape("exit.gif")

# Pen Class
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)

# Player Class
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("player.gif")
        self.penup()
        self.speed(0)
        self.stamina = 40

    def decrease_stamina(self):
        if self.stamina > 0:
            self.stamina -= 1
        if self.stamina <= 0:
            self.stamina = 0
            game_over()  # Trigger game over when stamina reaches 0

    def go_up(self):
        if not game_over_flag and self.stamina > 0:
            move_to_x = self.xcor()
            move_to_y = self.ycor() + 24
            if (move_to_x, move_to_y) not in walls:
                self.goto(self.xcor(), self.ycor() + 24)
                self.decrease_stamina()  # Reduce stamina when player moves

    def go_down(self):
        if not game_over_flag and self.stamina > 0:
            move_to_x = self.xcor()
            move_to_y = self.ycor() - 24
            if (move_to_x, move_to_y) not in walls:
                self.goto(self.xcor(), self.ycor() - 24)
                self.decrease_stamina()  # Reduce stamina when player moves

    def go_left(self):
        if not game_over_flag and self.stamina > 0:
            move_to_x = self.xcor() - 24
            move_to_y = self.ycor()
            if (move_to_x, move_to_y) not in walls:
                self.goto(self.xcor() - 24, self.ycor())
                self.decrease_stamina()  # Reduce stamina when player moves

    def go_right(self):
        if not game_over_flag and self.stamina > 0:
            move_to_x = self.xcor() + 24
            move_to_y = self.ycor() 
            if (move_to_x, move_to_y) not in walls:
                self.goto(self.xcor() + 24, self.ycor())
                self.decrease_stamina()  # Reduce stamina when player moves

    def is_collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        if distance < 5:
            return True
        else:
            return False

# Food Class
class Food(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("food.gif")
        self.penup()
        self.speed(0)
        self.goto(x, y)

    def destroy(self):
        self.goto(2000, 2000)  # Move off-screen
        self.hideturtle()

# Zombie Class
class Zombie(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("zombie.gif")
        self.penup()
        self.speed(0)
        self.goto(x, y)

# Exit Class
class Exit(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("exit.gif")
        self.penup()
        self.speed(0)
        self.goto(x, y)

# Levels list
levels = []

# First level
level_1 = [
"XXXXXXXXXXXXXXXXXXXXXXXXX",
"XP XXXXXXX          XXXXX",
"X  XXXXXXX  XXXXXX  XXXXX",
"X       XX  XXXXXX  XXXXX",
"X   T   XX  XXX        XX",
"XXXXXX  XX  XXX    T   XX",
"XXXXXX  XX  XXXXXX  XXXXX",
"XXXXXX  XX    XXXX  XXXXX",
"X  XXX        XXXXZ XXXXX",
"X  XXX  XXXXXXXXXXXXXXXXX",
"X         XXXXXXXXXXXXXXX",
"X    T           XXXXXXXX",
"XXXXXXXXXXXX     XXXXX  X",
"XXXXXXXXXXXXXXX  XXXXX  X",
"XXX  XXXXXXXXXX         X",
"XXX                     X",
"XXX    T    XXXXXXXXXXXXX",
"XXXXXXXXXX  XXXXXXXXXXXXX",
"XXXXXXXXXX        T     X",
"XXE  XXXXX              X",
"XX   XXXXXXXXXXXXX  XXXXX",
"XX     XXXXXXXXXXX  XXXXX",
"XX          XXXX        X",
"XXXX                    X",
"XXXXXXXXXXXXXXXXXXXXXXXXX"
]

levels.append(level_1)

# Maze Setup
def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]

            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)
            if character == "X":
                pen.goto(screen_x, screen_y)
                pen.shape("wall.gif")
                pen.stamp()
                walls.append((screen_x, screen_y))

            if character == "P":
                player.goto(screen_x, screen_y)

            if character == "T":
                foods.append(Food(screen_x, screen_y))

            if character == "Z":
                zombies.append(Zombie(screen_x, screen_y))

            if character == "E":
                exits.append(Exit(screen_x, screen_y))  

# Initialize Pen, Player, Walls, Foods, Zombies, Exits
pen = Pen()
player = Player()
walls = []
foods = []
zombies = []
exits = []

setup_maze(levels[0])

# Stamina Display
stamina_display = Pen()
stamina_display.goto(0, 310)
stamina_display.color("yellow")
stamina_display.hideturtle()

def update_stamina_display():
    stamina_display.clear()  # Clear previous stamina display
    stamina_display.write("Stamina: {}".format(player.stamina), align="center", font=("Arial", 18, "normal"))

# Game Over Flag
game_over_flag = False

# Game Over Screen with Win Condition
def game_over(won=False):
    global game_over_flag
    game_over_flag = True

    # Hide player, zombies, foods, walls, exits, and stamina display
    player.hideturtle()
    for food in foods:
        food.hideturtle()
    for zombie in zombies:
        zombie.hideturtle()
    for wall in walls:
        pen.goto(wall)
        pen.shape("square")
        pen.hideturtle()
    for exit_point in exits:
        exit_point.hideturtle()  # Hide each exit point
    stamina_display.hideturtle()

    # Display "GAME OVER" or "YOU WIN" message
    pen.clear()  # Clear previous screen before writing messages
    pen.goto(0, 0)

    if won:
        pen.color("green")
        pen.write("YOU WIN", align="center", font=("Arial", 24, "normal"))
    else:
        pen.color("red")
        pen.write("GAME OVER", align="center", font=("Arial", 24, "normal"))

    # Display Restart and Quit options
    pen.goto(0, -50)
    pen.color("yellow")
    pen.write("Press R to Restart", align="center", font=("Arial", 18, "normal"))

    pen.goto(0, -80)
    pen.color("yellow")
    pen.write("Press Q to Quit", align="center", font=("Arial", 18, "normal"))

# Add Exit Collision Logic
def check_exit_collision():
    for exit_point in exits:  # Use the correct list for exits
        if player.is_collision(exit_point):
            game_over(won=True)  # Trigger win condition when player touches exit

# Restart the Game
def restart_game():
    global game_over_flag
    game_over_flag = False

    # Hide the restart and quit options
    pen.clear()

    # Reset game state
    player.goto(-288, 288)
    player.showturtle()
    player.stamina = 40

    # Re-initialize foods, zombies, walls, and exits
    global foods, zombies, walls, exits
    foods.clear()
    zombies.clear()
    walls.clear()
    exits.clear()  # Clear existing exits

    setup_maze(levels[0])  # Recreate the maze
    update_stamina_display()

# Close the Game
def close_game():
    wn.bye()

# Keyboard Bindings
wn.listen()
wn.onkeypress(player.go_left, "Left")
wn.onkeypress(player.go_right, "Right")
wn.onkeypress(player.go_up, "Up")
wn.onkeypress(player.go_down, "Down")
wn.onkeypress(restart_game, "r")
wn.onkeypress(close_game, "q")

# Calculate Neighbors for Dijkstra
def get_neighbors(position, walls):
    x, y = position
    neighbors = [
        (x + 24, y),  # Right
        (x - 24, y),  # Left
        (x, y + 24),  # Up
        (x, y - 24)   # Down
    ]
    valid_neighbors = []
    for nx, ny in neighbors:
        if (nx, ny) not in walls:
            valid_neighbors.append((nx, ny))
    return valid_neighbors

# Dijkstra Algorithm to find shortest path
def dijkstra(start, goal, walls):
    queue = deque([(start, [start])])  # Queue contains (position, path)
    visited = set()

    while queue:
        current, path = queue.popleft()

        if current == goal:
            return path  # Return the path when we reach the goal

        if current in visited:
            continue
        visited.add(current)

        for neighbor in get_neighbors(current, walls):
            if neighbor not in visited:
                new_path = path + [neighbor]
                queue.append((neighbor, new_path))

    return []  # Return empty path if no path is found

# Move zombie towards player
def move_zombie_towards_player(zombie, player, walls):
    start = (zombie.xcor(), zombie.ycor())
    goal = (player.xcor(), player.ycor())

    path = dijkstra(start, goal, walls)

    if path and len(path) > 1:
        next_position = path[1]  # Zombie follows the path found
        zombie.goto(next_position[0], next_position[1])

# Initialize Frame Counter
frame_count = 0
zombie_move_interval = 10  # Adjust this value to control zombie speed

# Main Game Loop
while True:
    if not game_over_flag:
        for food in foods[:]:  # Iterate over a copy of the list
            if player.is_collision(food):
                player.stamina += 10  # Increase stamina when eating food
                print("Player Stamina: {}".format(player.stamina))
                food.destroy()
                foods.remove(food)

        for zombie in zombies:  # Collision with zombies (as enemies)
            if player.is_collision(zombie):
                print("Player dies!")
                game_over()  # Trigger game over when collision with zombie

        # Check for exit collision (win condition)
        check_exit_collision()

        # Update stamina display
        update_stamina_display()

        # Increment frame counter
        frame_count += 1

        # Move zombies at specified intervals
        if frame_count % zombie_move_interval == 0:
            for zombie in zombies:
                move_zombie_towards_player(zombie, player, walls)

    # Update the screen
    wn.update()

    # Add a small delay to control the overall game speed
    time.sleep(0.01)  # Adjust as needed
