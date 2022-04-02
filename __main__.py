import pyray
import random
from raylib import KEY_SPACE
from ball import Ball
from platform import Platform

def main():
    screen_width = 450
    screen_height = 800
    current_state = "begin_state"

    states = {
        "begin_state": lambda: begin_state(screen_width, screen_height),
        "play_state": lambda: play_state(ball, platforms),
        "end_state": lambda: end_state(screen_width, screen_height, ball)
    }

    pyray.init_window(screen_width, screen_height, "Ball movement test")

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

    pyray.clear_background(pyray.Color(255,255,255))

    pyray.draw_text("Ball Dropper 69", 100, screen_height - 600, 30, [255,0,255])

    pyray.draw_text("Press 'SPACE' to begin!", 160, screen_height - 300, 20, [250,30,50])

    pyray.end_drawing()
    
    if pyray.is_key_down(KEY_SPACE):
        return "play_state"

    return "begin_state"


def play_state(ball, platforms):
    pyray.begin_drawing()

    pyray.clear_background(pyray.Color(255, 255, 255))
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

    pyray.clear_background(pyray.Color(255,255,255))
    score = ball.score
    pyray.draw_text("GAME OVER", screen_width//2-125, screen_height-400, 40, [255,0,255])
    pyray.draw_text(f"Final Score: {score}", screen_width//2-135, screen_height-500, 40, [255,0,0])

    pyray.end_drawing()

    return "end_state"

main()
