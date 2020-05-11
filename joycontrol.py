from m5stack import axp, btnA, btnB
from m5ui import M5Rect, M5Circle, setScreenColor
from uiflow import wait_ms
import time
import hat

# configure size of deadzone on joystick input
joyTolerance = 0.5

# configure display
intDisplayBrightness = 35
setScreenColor(0x111111)
axp.setLcdBrightness(intDisplayBrightness)

# configure cursor position and size
lstCursorCrd = [20, 5] # initial position
cursorRad = 4
circle0 = M5Circle(lstCursorCrd[0], lstCursorCrd[1], cursorRad, 0xFFFFFF, 0xFFFFFF)

# rectangular obstruction and hit box around it
obs = (29, 109, 20, 20)
rectangle0 = M5Rect(obs[0], obs[1], obs[2], obs[3], 0xFF5500, 0xFF5500)
rectLeadX = obs[0]
rectLeadY = obs[1]
rectEndX = obs[0] + obs[2]
rectEndY = obs[1] + obs[3]

# define joystick hat
joy0 = hat.get(hat.JOYSTICK)
#get center positions on joystick for calibration
joyX = joy0.InvertX
joyY = joy0.InvertY

#store booleans of invalid motion
boolXPlus = True
boolXMinus = True
boolYPlus = True
boolYMinus = True

#store timeouts to reduce collision flicker
yTimeoutDur = None
xTimeoutDur = None
yTimedout = False
xTimedout = False

#store current state for play/pause
play = True

while True:
    while play is True:
        # move cursor hitbox
        circLeadY = round(lstCursorCrd[0]) - cursorRad - 2 
        circLeadX = round(lstCursorCrd[1]) - cursorRad - 2
        circEndY = round(lstCursorCrd[0]) + cursorRad + 2
        circEndX = round(lstCursorCrd[1]) + cursorRad + 2
        if not ((circEndY > rectLeadY) and (circLeadY < rectEndY) and (circLeadX < rectEndX) and (circEndX > rectLeadX)):
            # left
            if lstCursorCrd[0] < 153 and (joy0.InvertY - joyY) > (0 + joyTolerance) and yTimedout is False:
                lstCursorCrd[0] += abs((joy0.InvertY - joyY)/75)
            # right
            if lstCursorCrd[0] > 5 and (joy0.InvertY - joyY) < (0 - joyTolerance) and yTimedout is False:
                lstCursorCrd[0] -= abs((joy0.InvertY - joyY)/75)
            # down
            if lstCursorCrd[1] > 4 and (joy0.InvertX - joyX) > (0 + joyTolerance) and xTimedout is False:
                lstCursorCrd[1] -= abs((joy0.InvertX - joyX)/75)
            # up
            if lstCursorCrd[1] < 75 and (joy0.InvertX - joyX) < (0 - joyTolerance) and xTimedout is False:
                lstCursorCrd[1] += abs((joy0.InvertX - joyX)/75)
        
        #collision detection code
        elif circEndY >= rectLeadY and circLeadY < rectLeadY:
            # time out the cursor to prevent blink
            yTimeoutDur = time.ticks_ms()
            yTimedout = True
            # move cusor back
            lstCursorCrd[0] -= 1
        elif circLeadY <= rectEndY and circEndY > rectEndY:
            # time out the cursor to prevent blink
            yTimeoutDur = time.ticks_ms()
            yTimedout = True
            # move cursor back
            lstCursorCrd[0] += 1
        elif circEndX >= rectLeadX and circLeadX < rectLeadX:
            # time out the cursor to prevent blink
            xTimeoutDur = time.ticks_ms()
            xTimedout = True
            # move cursor back
            lstCursorCrd[1] -= 1
        elif circLeadX <= rectEndX and circEndX > rectEndX:
            # time out the cursor to prevent blink
            xTimeoutDur = time.ticks_ms()
            xTimedout = True
            # move cursor back
            lstCursorCrd[1] += 1

        
        #render cursor in current position
        circle0.setPosition(y=round(lstCursorCrd[0]), x=round(lstCursorCrd[1]))

        # unpause cursor movement after set duration from collision
        if time.ticks_diff(time.ticks_ms(), yTimeoutDur) > 200:
            yTimedout = False
        if time.ticks_diff(time.ticks_ms(), xTimeoutDur) > 200:
            xTimedout = False

        # pause game with button
        if btnB.wasPressed():
            play = False
        rectangle0.show()
    
    # adjust display brightness while paused
    if (joy0.InvertX - joyX) < (0 - joyTolerance) and intDisplayBrightness < 100:
        intDisplayBrightness += 5
        axp.setLcdBrightness(intDisplayBrightness)
        wait_ms(100)
    if (joy0.InvertX - joyX) > (0 + joyTolerance) and intDisplayBrightness > 20:
        intDisplayBrightness -= 5
        axp.setLcdBrightness(intDisplayBrightness)
        wait_ms(100)

    # resume game
    if btnB.wasPressed():
        play = True
