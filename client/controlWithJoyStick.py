# -*- coding: utf-8 -*-
import pygame
import numpy as np
from remoteControl import RemoteControl

host = '192.168.5.66'
port = '8000'
tail = '/motor'
send = True

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10

def getAngle(x, y):
    angle = np.arctan2(x, y)
    if (angle <= 0):
        angle = (2 * np.pi + angle)
    return angle * 360 / (2 * np.pi) - 275

class ControlWithJoyStick:
    def __init__(self):
        pygame.init()
        size = [500, 700]
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("DMC-12 Control Panel")
        control = True
        clock = pygame.time.Clock()
        pygame.joystick.init()
        textPrint = TextPrint()
        self.remoteControl = RemoteControl(host, port, tail)
        # -------- Main Program Loop -----------
        while control:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    control = False
            screen.fill(WHITE)
            textPrint.reset()
            joystick_count = pygame.joystick.get_count()

            textPrint.print(screen, "Number of joysticks: {}".format(joystick_count) )
            textPrint.indent()
            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()

                # --------- Control Key -----------
                linearKey = joystick.get_axis(2)
                stopKey = joystick.get_button(0)
                exitKey = joystick.get_button(1)
                axisX = joystick.get_axis(0)
                axisY = joystick.get_axis(1)
                turnAngle = getAngle(axisX, axisY)
                turnX, turnY = joystick.get_hat(0)

                textPrint.print(screen, "Joystick {}".format(i) )
                textPrint.indent()
                name = joystick.get_name()
                textPrint.print(screen, "Joystick name: {}".format(name) )
                axes = joystick.get_numaxes()
                textPrint.print(screen, "Number of axes: {}".format(axes) )
                textPrint.indent()
                for i in range( axes ):
                    axis = joystick.get_axis( i )
                    textPrint.print(screen, "Axis {} value: {:>6.3f}".format(i, axis) )
                textPrint.unindent()

                buttons = joystick.get_numbuttons()
                textPrint.print(screen, "Number of buttons: {}".format(buttons) )
                textPrint.indent()

                for i in range( buttons ):
                    button = joystick.get_button( i )
                    textPrint.print(screen, "Button {:>2} value: {}".format(i,button) )
                textPrint.unindent()

                hats = joystick.get_numhats()
                textPrint.print(screen, "Number of hats: {}".format(hats) )
                textPrint.indent()

                for i in range( hats ):
                    x, y  = joystick.get_hat( i )
                    textPrint.print(screen, "Hat {} value: {}".format(i, str(x), str(y)) )
                textPrint.unindent()

                textPrint.unindent()

                if (linearKey < -0.001):
                    print("Forward")
                    #ws.send("forward")
                    self.remoteControl.forward()
                elif (linearKey > 0.001):
                    print("Backward")
                    #ws.send("backward")
                    self.remoteControl.backward()

                if (stopKey > 0):
                    print("Stop")
                    #ws.send("stop")
                    self.remoteControl.stop()

                if (exitKey > 0):
                    control = False

                if (turnX > 0):
                    print('Right')
                    #ws.send("right")
                    self.remoteControl.right()
                elif (turnX < 0):
                    print("Left")
                    #ws.send("left")
                    self.remoteControl.left()

                if (abs(axisX) > 0.001 and abs(axisY) > 0.001):
                    if (0 < turnAngle < 90):
                        print("Turn Right with Angle:", turnAngle)
                        #ws.send("right")
                    elif (-90 < turnAngle < 0):
                        print("Turn Left with Angle:", -turnAngle)
                        #ws.send("left")

            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # Limit to 20 frames per second
            clock.tick(20)
            self.remoteControl.exit()

if __name__ == "__main__":
    ctrl = ControlWithJoyStick()

