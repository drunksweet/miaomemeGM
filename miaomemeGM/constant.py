import random

class COLOR:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    GREY = (190, 190, 190)
    YELLOW = (255, 255, 0)
    NAVAJOWHITE = (255, 222, 173)
    NAVAJOWHITE4 = (139, 121, 94)
    PINK=(255, 20, 147)

class WINDOW:
    WIDTH = 600
    HEIGHT = 900
    HEIGHT_SCREEN = HEIGHT*0.6
    X_LEN = 8
    Y_LEN = 6


class BLOCK:
    WIDTH = WINDOW.WIDTH // WINDOW.X_LEN
    HEIGHT = WIDTH
    SPEED = 5
    class FORM:
        NORM = 1
        LONG = 2
        SOLID = 3

        def random():
            return random.randint(1, 3)

