import pyray
import random
from body import Body

class Platform(Body):
    # ------------------------------------------------------------------------------------------------
    #   Handles drawing and positioning the rising platforms. Overwrites Body's Update and Draw methods. 
    #
    #   Methods: 
    #       update(self): Updates the platform position and wraps platforms around once they reach the top of the screen
    #
    #       draw(self): Draws the platforms as purple rectangles
    # ------------------------------------------------------------------------------------------------
    def __init__(self, x, y, color):
        super().__init__()
        self.position = pyray.Vector2(x, y)
        self.dimensions = pyray.Vector2(200, 50)
        self._color = color


    def update(self):
        self.position.y -= 4

        if(self.position.y <= 0):
            self.position.y = 800
            self.position.x = random.randint(10, 350)

    def draw(self):
        pyray.draw_rectangle_v(
            self.position, self.dimensions, [255, 0, 255])
