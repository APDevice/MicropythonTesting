import random
from microbit import *
import machine


SCREEN_MEMORY = [[0,0,0,0,0] for i in range(5)]
X = 2
Y = 2
TRIES = 0
up = down = left = right = False

# set how much time waited between successful moves
resttime = 25

def cursor(drct):
    global X, Y, up, down, left, right, SCREEN_MEMORY, TRIES
    if drct == 0 and up == False: # up
        if X > 0 and SCREEN_MEMORY[X-1][Y] == 0:
            X -= 1
            up = down = left = right = False
            sleep(resttime)
        else:
            up = True
    elif drct == 1 and down == False: # down
        if X < 4 and SCREEN_MEMORY[X+1][Y] == 0:
            X += 1
            up = down = left = right = False
            sleep(resttime)
        else:
            down = True
    elif drct == 2 and left == False: # left
        if Y > 0 and SCREEN_MEMORY[X][Y-1] == 0:
            Y -= 1
            up = down = left = right = False
            sleep(resttime)
        else:
            left = True
    elif drct == 3 and right == False: # right
        if Y < 4 and SCREEN_MEMORY[X][Y+1] == 0:
            Y += 1
            up = down = left = right = False
            sleep(resttime)
        else:
            right = True
    else:
        if all((up, down, left, right)):
            Perfect = True
            for i in range(0,5):
                 if 0 in SCREEN_MEMORY[i]:
                    Perfect = False
            if Perfect is False:
                sleep(100)
                display.clear()
                SCREEN_MEMORY = [[0,0,0,0,0] for i in range(5)]
                X, Y = 2, 2
                up = down = left = right = False
                TRIES += 1
            else:
                sleep(1000)
                display.scroll(str(TRIES), wait=True)
                return False

    display.set_pixel(X, Y, 9)
    SCREEN_MEMORY[X][Y] = 3
    return True
    


while True:
    # display.clear()
    intRan = random.randrange(0, 5)
    refresh = cursor(intRan)
    if refresh == True:
        for i in range(5):
            for l in range(5):
                if SCREEN_MEMORY[i][l] == 3 and (X, Y) != (i, l):
                    display.set_pixel(i, l, 3)