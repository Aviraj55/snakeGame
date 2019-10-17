import random, pygame, sys
from pygame.locals import *

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
CELL_SIZE = 30
FPS = 60
assert WINDOW_HEIGHT % CELL_SIZE == 0, "The window height must be a multiple of the cell size"
assert WINDOW_WIDTH % CELL_SIZE == 0, "The window width must be a multiple of the cell size"
CELL_WIDTH = int(WINDOW_WIDTH / CELL_SIZE) #Number of cells in the width of the window
CELL_HEIGHT = int(WINDOW_HEIGHT / CELL_SIZE) #Number of cells in the height of the window

#RGB TABLE      R    G   B  
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
RED        = (255,   0,   0)
GREEN      = (  0, 255,   0)
DARK_GREEN = (  0, 155,   0)
DARK_GRAY  = ( 40,  40,  40)

BACKGROUND_COLOR = BLACK

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

 #Set equal to 0 so we can reference the snake's position by snake_Coords[SNAKE_HEAD], more readable
SNAKE_HEAD = 0

def main():
    global fps_clock, game_screen, game_font, high_Score

    high_Score = 0
    pygame.init()
    fps_clock = pygame.time.Clock()
    game_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    game_font = pygame.font.Font("freesansbold.ttf", 20)
    pygame.display.set_caption("Avi's Snake")

    show_Start_Screen()
    while True:
        pygame.time.wait(300)
        run_Game()
        if game_score > high_Score:
            high_Score = game_score
        show_Game_Over_Screen()

 #Returns when a game over condition occurs
def run_Game():
    global game_score
    #Set snake to start at a random point, snake head is at (x_start, y_start)
    x_start = random.randint(5, CELL_WIDTH - 6)
    y_start = random.randint(5, CELL_HEIGHT - 6)
    #The snake is stored as a list within a dictionary of values, x and y keys represent the x and y values of the body segment
    snake_Coords = [ {"x": x_start, "y": y_start},
                     {"x" :x_start - 1, "y": y_start},
                     {"x": x_start - 2, "y": y_start}]
    direction = RIGHT

    #Set the apple to be at a random location
    apple = get_Random_Location()

    while True: #loop for the game
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT: #Quits program if there is a QUIT event
                terminate()
            # Checks if there is a KEYDOWN event, allows for movement in new, perpendicular directions only with Arrow keys or WASD
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()
        #Checks if the snake has collided with the edge of the window
        if snake_Coords[SNAKE_HEAD]['x'] == -1 or snake_Coords[SNAKE_HEAD]['x'] == CELL_WIDTH or snake_Coords[SNAKE_HEAD]['y'] == -1 or snake_Coords[SNAKE_HEAD]['y'] == CELL_HEIGHT:
            return 
        for snake_body in snake_Coords[1:]:
            if snake_body['x'] == snake_Coords[SNAKE_HEAD]['x'] and snake_body['y'] == snake_Coords[SNAKE_HEAD]['y']:
                return 

        #if the snake's head collides with an apple, set the apple at a new random location
        if snake_Coords[SNAKE_HEAD]["x"] == apple["x"] and snake_Coords[SNAKE_HEAD]["y"] == apple["y"]:
            apple = get_Random_Location()
        #delete the tail segment of the snake if not colliding with an apple
        else:
            del snake_Coords[-1]
        
        #Move the snake by adding a segment in the direction of the motion
        if direction == UP:
            new_Head = {'x': snake_Coords[SNAKE_HEAD]['x'], 'y': snake_Coords[SNAKE_HEAD]['y'] - 1}
        elif direction == DOWN:
            new_Head = {'x': snake_Coords[SNAKE_HEAD]['x'], 'y': snake_Coords[SNAKE_HEAD]['y'] + 1}
        elif direction == LEFT:
            new_Head = {'x': snake_Coords[SNAKE_HEAD]['x'] - 1, 'y': snake_Coords[SNAKE_HEAD]['y']}
        elif direction == RIGHT:
            new_Head = {'x': snake_Coords[SNAKE_HEAD]['x'] + 1, 'y': snake_Coords[SNAKE_HEAD]['y']}

        snake_Coords.insert(SNAKE_HEAD,new_Head)

        #Draw the game board, game elements
        game_screen.fill(BACKGROUND_COLOR)
        draw_Grid()
        draw_Snake(snake_Coords)
        draw_Apple(apple)
        game_score = len(snake_Coords) - 3
        draw_Score(game_score)
        pygame.time.wait(100)
        pygame.display.update()
        fps_clock.tick(FPS)

def draw_Key_Press_Message():
    press_Key_Surface = game_font.render("Press any key to play.", True, DARK_GRAY)
    press_Key_Rectangle = press_Key_Surface.get_rect()
    press_Key_Rectangle.topleft = (WINDOW_WIDTH - 250, WINDOW_HEIGHT - 30)
    game_screen.blit(press_Key_Surface, press_Key_Rectangle)

#Checks if there are any QUIT events in the queue, ex. when esc key stopped being pressed
def check_For_Key_Press(): 
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
    
    key_Up_Events = pygame.event.get(KEYUP)

    if len(key_Up_Events) == 0:
        return None
    if key_Up_Events[0].key == K_ESCAPE:
        terminate()
    return key_Up_Events[0].key

def get_Random_Location():
    return {'x': random.randint(0, CELL_WIDTH - 1), 'y': random.randint(0, CELL_HEIGHT - 1)}


def show_Start_Screen():
    title_Font = pygame.font.Font("freesansbold.ttf", 100)
    #Has white text with a dark green background
    title_Surface1 = title_Font.render("SNAKEE!", True, WHITE, DARK_GREEN)
    #Green text with transparent background 
    title_Surface2 = title_Font.render("SNAKEE!", True, GREEN)
    degrees1 = 0
    degrees2 = 0

    while True:
        game_screen.fill(BACKGROUND_COLOR)
        rotated_Surface1 = pygame.transform.rotate(title_Surface1,degrees1)
        rotated_Rectangle1 = rotated_Surface1.get_rect()
        rotated_Rectangle1.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        game_screen.blit(rotated_Surface1, rotated_Rectangle1)

        rotated_Surface2 = pygame.transform.rotate(title_Surface2,degrees2)
        rotated_Rectangle2 = rotated_Surface2.get_rect()
        rotated_Rectangle2.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        game_screen.blit(rotated_Surface2, rotated_Rectangle2)

        draw_Key_Press_Message()

        pygame.display.update()
        fps_clock.tick(FPS)
        degrees1 += 2
        degrees2 += 5

        if check_For_Key_Press():
            pygame.event.clear()
            return

def show_Game_Over_Screen():
    #Creates the "Game" and "Over" surface objects and draws them on the screen
    game_Over_Font = pygame.font.Font("freesansbold.ttf", 150)
    game_Surface = game_Over_Font.render("Game", True, WHITE)
    over_Surface = game_Over_Font.render("Over", True, WHITE)
    game_Rectangle = game_Surface.get_rect()
    over_Rectanagle = over_Surface.get_rect()
    game_Rectangle.midtop = (WINDOW_WIDTH / 2, 10)
    over_Rectanagle.midtop = (WINDOW_WIDTH / 2, game_Rectangle.height + 10 + 25)

    game_screen.blit(game_Surface, game_Rectangle)
    game_screen.blit(over_Surface, over_Rectanagle)
    draw_Key_Press_Message()
    pygame.display.update()
    # Clear out key presses in the queue of events, waits half a second before user can input
    pygame.time.wait(500)
    check_For_Key_Press()
    #Stays on the screen until the player presses a key
    while True:
        if check_For_Key_Press():
            pygame.event.get() #clears the event queue
            return

def draw_Grid():
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(game_screen, DARK_GRAY, (x,0), (x,WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(game_screen, DARK_GRAY, (0,y), (WINDOW_WIDTH,y))

#Draws a dark green box for each snake segment
def draw_Snake(snake_Coordinates):
    for coord in snake_Coordinates:
        x = coord["x"] * CELL_SIZE
        y = coord["y"] * CELL_SIZE
        #Draws an outer dark green rectangle with a light green inner rectangle
        snake_Segment_Rectangle = pygame.Rect(x,y,CELL_SIZE,CELL_SIZE)
        pygame.draw.rect(game_screen,DARK_GREEN,snake_Segment_Rectangle)
        snake_Inner_Segment_Rectangle = pygame.Rect(x + 4, y + 4, CELL_SIZE - 8, CELL_SIZE - 8)
        pygame.draw.rect(game_screen, GREEN, snake_Inner_Segment_Rectangle)


def draw_Apple(coordinate):
    x = coordinate["x"] * CELL_SIZE
    y = coordinate["y"] * CELL_SIZE
    apple_rectangle = pygame.Rect(x,y,CELL_SIZE,CELL_SIZE)
    pygame.draw.rect(game_screen, RED, apple_rectangle)

def draw_Score(score):
    score_Surface = game_font.render("Score: %s" %score +  5 * " " + "High Score: %s" %high_Score, True, WHITE)
    score_Rectangle = score_Surface.get_rect()
    score_Rectangle.topleft = (WINDOW_WIDTH - 300, 10)
    game_screen.blit(score_Surface,score_Rectangle)


def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
