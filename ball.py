import pyray
from raylib import KEY_LEFT, KEY_RIGHT

from body import Body

def AABBCollision(x1, y1, w1, h1, x2, y2, w2, h2):
    # ------------------------------------------------
    #   Handles collision of objects given their dimensions
    # ------------------------------------------------
    return (
        x1 < x2 + w2 and
        x1 + w1 > x2 and
        y1 < y2 + h2 and
        y1 + h1 > y2
    )

class Ball(Body):
    # ------------------------------------------------------------------------------------------------
    #   Handles drawing and positioning the controlled object. Overwrites Body's Update and Draw methods. 
    #
    #   Methods: 
    #       update(self): Updates the ball position based on player input and platform collision
    #
    #       draw(self): Draws the ball as a red circle
    #
    #       contrain(self, val, min, max): Prevents ball from leaving the bounds of the playspace
    #           
    #       is_dead(self): Handles collision with top or bottom of playspace
    #
    #       handle_collision(self, platforms): Handles collision of ball and platforms
    # ------------------------------------------------------------------------------------------------
    def __init__(self, x, y, radius, color):
        super().__init__()
        self._velocity = pyray.Vector2(0, 0)
        self._position = pyray.Vector2(x, y)
        self._radius = radius
        self._color = color
        self.score = 0

        self._control_lock = False

        self._sticky_platform = None

    def constrain(self, val, min, max):
        if val < min: 
            return min
        if val > max:
            return max
        return val

    def is_dead(self):
        return self._position.y > 800 or self._position.y < 0

    def handle_collision(self, platforms):
        self._sticky_platform = None
        no_collisions = True

        for platform in platforms:
            is_colliding = AABBCollision(
                    self._position.x - self._radius, 
                    self._position.y - self._radius,
                    self._radius * 2,
                    self._radius * 2,
                    platform.position.x,
                    platform.position.y,
                    platform.dimensions.x,
                    platform.dimensions.y
                    )
            no_collisions = no_collisions and not is_colliding
            if is_colliding:
                self._control_lock = False
                self._sticky_platform = platform
                self.score += 1
        
        if no_collisions:
            self._control_lock = True
        

    def update(self):
        if not self._control_lock:
            if pyray.is_key_down(KEY_RIGHT):
                self._velocity.x += 0.5

            if pyray.is_key_down(KEY_LEFT):
                self._velocity.x -= 0.5

        self._velocity.y += 0.2

        self._position.x += self._velocity.x
        self._position.y += self._velocity.y

        self._velocity.x *= 0.95

        if self._sticky_platform:
            self._velocity.y = 0
            self._position.y = self._sticky_platform.position.y - self._radius

        self._position.x = self.constrain(self._position.x, 0, 450)


        

    def draw(self):
        pyray.draw_circle_v(self._position, self._radius, self._color)
    
