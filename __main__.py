import pyray
import random
from raylib import KEY_SPACE
from ball import Ball
from platform import Platform

def main():
    # ------------------------------------------------------------------------------------------------
    #   The main game loop
    #
    #   Functions: 
    #       begin_state(screen_width, screen_height): Draws and handles input for the menu screen 
    #
    #       play_state(ball, platforms): Draws and handles input for the main game loop
    #
    #       end_state(screen_width, screen_height, ball): Draws the game- over screen
    # ------------------------------------------------------------------------------------------------
    screen_width = 450
    screen_height = 800
    current_state = "begin_state"

    states = {
        "begin_state": lambda: begin_state(screen_width, screen_height),
        "play_state": lambda: play_state(ball, platforms),
        "end_state": lambda: end_state(screen_width, screen_height, ball)
    }

    pyray.init_window(screen_width, screen_height, "Dropper Prototype")

    ball = Ball(screen_width / 2, screen_height / 2, 25, (255, 0, 0))

    platforms = []
    for i in range((screen_height // (50 + 150)) + 1):
        platforms.append(Platform(random.randint(
            0, screen_width), i*150, [255, 0, 255]))

    pyray.set_target_fps(60)

    while not pyray.window_should_close():
        current_state = states[current_state]()

    pyray.close_window()

def begin_state(screen_width, screen_height):
    pyray.begin_drawing()

    pyray.clear_background(pyray.Color(182, 194, 252))

    pyray.draw_text("Dropper Prototype", 75, screen_height - 700, 30, [81, 37, 122])

    pyray.draw_text("Press 'SPACE' to begin!", 77, screen_height - 500, 25, [250,30,50])

    pyray.end_drawing()
    
    if pyray.is_key_down(KEY_SPACE):
        return "play_state"

    return "begin_state"


def play_state(ball, platforms):
    pyray.begin_drawing()

    pyray.clear_background(pyray.Color(182, 194, 252))
    score = ball.score
    pyray.draw_text("Move ball with arrow keys", 10, 10, 20, [0, 0, 0])
    pyray.draw_text(f"Score: {score}", 10,40,20, [0,0,0])

    for platform in platforms:
        platform.update()
        platform.draw()

    ball.handle_collision(platforms)

    ball.update()
    ball.draw()

    if ball.is_dead():
        return "end_state"

    pyray.end_drawing()

    return "play_state"

def end_state(screen_width, screen_height, ball):
    pyray.begin_drawing()

    pyray.clear_background(pyray.Color(182, 194, 252))

    score = ball.score
    
    pyray.draw_text("GAME OVER", 50, screen_height-500, 60, [157, 0, 255])
    pyray.draw_text(f"Final Score: {score}", 70, screen_height-400, 40, [255,0,0])

    pyray.end_drawing()

    return "end_state"

main()
