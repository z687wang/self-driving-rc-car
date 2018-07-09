import tornado.websocket
from tornado.ioloop import PeriodicCallback
from Motor import Motor


class MotorHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def on_message(self, message):
        self.motor = Motor()
        if message == "forward":
            print("message recived - forward")
            self.motor.Motor_Forward()
        elif message == "backward":
            print("message recived - backward")
            self.motor.Motor_Backward()
        elif message == "left":
            print("message recived - left")
            self.motor.Motor_TurnLeft()
        elif message == "right":
            print("message recived - right")
            self.motor.Motor_TurnRight()
        elif message == 'forwardLeft':
            print("message received - forwardLeft")
            self.motor.Motor_ForwardLeft()
        elif message == 'forwardRight':
            print("message received - forwardRight")
            self.motor.Motor_ForwardRight()
        elif message == "stop":
            self.motor.Motor_Stop()
        else:
            print("MotorHandler - Unsupported function " + message)