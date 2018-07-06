# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import cv2
import time
import os
import websocket
import _thread

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
    

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("### Connected ###")
    pygame.init()
    size = [500, 700]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("My Game")
    #Loop until the user clicks the close button.
    done = False
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    
    # Initialize the joysticks
    pygame.joystick.init()
        
    # Get ready to print
    textPrint = TextPrint()
    # -------- Main Program Loop -----------
    while done==False:
        # EVENT PROCESSING STEP
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop
            
            # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
            if event.type == pygame.JOYBUTTONDOWN:
                1+1
                #print("Joystick button pressed.")
            if event.type == pygame.JOYBUTTONUP:
                1+1
                #print("Joystick button released.")
        screen.fill(WHITE)
        textPrint.reset()
    
        # Get count of joysticks
        joystick_count = pygame.joystick.get_count()
    
        textPrint.print(screen, "Number of joysticks: {}".format(joystick_count) )
        textPrint.indent()
        
        # For each joystick:
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
        
            textPrint.print(screen, "Joystick {}".format(i) )
            textPrint.indent()
        
            # Get the name from the OS for the controller/joystick
            name = joystick.get_name()
            textPrint.print(screen, "Joystick name: {}".format(name) )
            
            # Usually axis run in pairs, up/down for one, and left/right for
            # the other.
            axes = joystick.get_numaxes()
            textPrint.print(screen, "Number of axes: {}".format(axes) )
            textPrint.indent()
            
            for i in range( axes ):
                axis = joystick.get_axis( i )
                if (i == 2 and axis < -0.001):
                    print("forward")
                    ws.send("forward")
                elif (i == 2 and axis > 0.001):
                    print("stop")
                    ws.send("backward")
                textPrint.print(screen, "Axis {} value: {:>6.3f}".format(i, axis) )
            textPrint.unindent()
                
            buttons = joystick.get_numbuttons()
            textPrint.print(screen, "Number of buttons: {}".format(buttons) )
            textPrint.indent()
    
            for i in range( buttons ):
                button = joystick.get_button( i )
                if (i == 0 and button > 0):
                    print("stop")
                    ws.send("stop")
                textPrint.print(screen, "Button {:>2} value: {}".format(i,button) )
            textPrint.unindent()
                
            # Hat switch. All or nothing for direction, not like joysticks.
            # Value comes back in an array.
            hats = joystick.get_numhats()
            textPrint.print(screen, "Number of hats: {}".format(hats) )
            textPrint.indent()
    
            for i in range( hats ):
                x, y = joystick.get_hat( i )
                if (x > 0):
                    print("right")
                    ws.send("right")
                elif (x < 0):
                    print("left")
                    ws.send("left")
                textPrint.print(screen, "Hat {} value: {}".format(i, str(x), str(y)) )
            textPrint.unindent()    
            
            textPrint.unindent()
    
        
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
        
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
    
        # Limit to 20 frames per second
        clock.tick(20)
        
    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit ()
          
if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://"+host+":"+port+tail,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

