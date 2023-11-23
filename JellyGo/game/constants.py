from ctypes import windll

TOWER_CONSTANTS = {
    #   Level | Protection |  Jelly speed | Prod. speed | Capacity | Upgrade Cost
    "barracks": {
        1:     (1,          50,            0.4,          10,        5),
        2:     (1,          50,            0.8,          20,        10),
        3:     (1,          50,            1.2,          30,        20),
        4:     (1,          50,            1.6,          40,        30),
        5:     (1,          50,            2.0,          50,        0),
    },
    "fort": {
        1:     (2,          30,            0,            20,        10),
        2:     (2.5,        30,            0,            40,        15),
        3:     (3,          30,            0,            60,        20),
        4:     (3.5,        30,            0,            80,        25),
        5:     (4,          30,            0,            100,       0),
    },
    "lab": {
        1:     (1,          75,            0,            50,        15),
        2:     (1,          110,           0,            100,       20),
        3:     (1,          150,           0,            150,       0),
    },
    "house": {
        1:     (1,          50,            0.3,          10,        None),
    }
}

TOWERS_WIDTH = 100
TOWERS_TEXT_CENTER = TOWERS_WIDTH * 0.7
UPGRADE_BUTTON_SIZE = int(TOWERS_WIDTH / 3)
UPGRADE_INDICATOR_SIZE = TOWERS_WIDTH * 0.2
UPGRADE_BUTTON_MARGIN = 2
ATTRIBUTES_SURFACE_WIDTH = TOWERS_WIDTH
ATTRIBUTES_SURFACE_HEIGHT = TOWERS_WIDTH / 2
ATTRIBUTES_ICON_SIZE = TOWERS_WIDTH / 6
JELLY_BUBBLE_WIDTH = TOWERS_WIDTH / 5
JELLY_BUBBLE_TEXT_CENTER = JELLY_BUBBLE_WIDTH * 0.7

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
print(SCREEN_WIDTH, SCREEN_HEIGHT)

WINDOW_POSITION_X = 0
WINDOW_POSITION_Y = 0

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
