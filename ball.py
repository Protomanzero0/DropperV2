import pyray
from raylib import KEY_LEFT, KEY_RIGHT

from body import Body

def AABBCollision(x1, y1, w1, h1, x2, y2, w2, h2):
    return (
        x1 < x2 + w2 and
        x1 + w1 > x2 and
        y1 < y2 + h2 and
        y1 + h1 > y2
    )

class Ball(Body):
    def __init__(self, x, y, radius, color):
        super().__init__()
        self.velocity = pyray.Vector2(0, 0)
        self.position = pyray.Vector2(x, y)
        self.radius = radius
        self.color = color

        self.control_lock = False

        self.sticky_platform = None

    def constrain(self, val, min, max):
        if val < min: 
            return min
        if val > max:
            return max
        return val

    def is_dead(self):
        return self.position.y > 800 or self.position.y < 0

    def handle_collision(self, platforms):

        self.sticky_platform = None
        no_collisions = True

        for platform in platforms:
            is_colliding = AABBCollision(
                    self.position.x - self.radius, 
                    self.position.y - self.radius,
                    self.radius * 2,
                    self.radius * 2,
                    platform.position.x,
                    platform.position.y,
                    platform.dimensions.x,
                    platform.dimensions.y
                    )
            no_collisions = no_collisions and not is_colliding
            if is_colliding:
                self.control_lock = False
                self.sticky_platform = platform
        
        if no_collisions:
            self.control_lock = True
        

    def update(self):            
        if not self.control_lock:
            if pyray.is_key_down(KEY_RIGHT):
                self.velocity.x += 0.5

            if pyray.is_key_down(KEY_LEFT):
                self.velocity.x -= 0.5

        self.velocity.y += 0.2

        self.position.x += self.velocity.x
        self.position.y += self.velocity.y

        self.velocity.x *= 0.95

        if self.sticky_platform:
            self.velocity.y = 0
            self.position.y = self.sticky_platform.position.y - self.radius

        self.position.x = self.constrain(self.position.x, 0, 450)


        

    def draw(self):
        pyray.draw_circle_v(self.position, self.radius, self.color)
    
