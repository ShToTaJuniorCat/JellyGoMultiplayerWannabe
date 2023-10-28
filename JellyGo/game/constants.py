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

# Add any additional game-related constants here

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BACKGROUND_COLOR = (0, 0, 0, 0)
