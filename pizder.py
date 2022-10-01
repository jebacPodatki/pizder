import sys
import pygame
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d

class Car(object):
    def create_wheel(self, space):
        wheel_color = 52, 219, 119, 255
        mass = 100
        radius = 25
        moment = pymunk.moment_for_circle(mass, 20, radius)
        wheel_b = pymunk.Body(mass, moment)
        wheel_s = pymunk.Circle(wheel_b, radius)
        wheel_s.friction = 1.5
        wheel_s.color = wheel_color
        space.add(wheel_b, wheel_s)
        return wheel_b

    def create_blob(self, space):
        mass = 100
        size = (50, 30)
        moment = pymunk.moment_for_box(mass, size)
        blob_b = pymunk.Body(mass, moment)
        blob_s = pymunk.Poly.create_box(blob_b, size)
        space.add(blob_b, blob_s)
        return blob_b

    def create_joints(self, wheel1, wheel2, blob, space):
        space.add(
            pymunk.PinJoint(wheel1, blob, (0, 0), (-25, -15)),
            pymunk.PinJoint(wheel1, blob, (0, 0), (-25, 15)),
            pymunk.PinJoint(wheel2, blob, (0, 0), (25, -15)),
            pymunk.PinJoint(wheel2, blob, (0, 0), (25, 15)),
        )

        speed = 5
        motor1 = pymunk.SimpleMotor(wheel1, blob, speed)
        motor2 = pymunk.SimpleMotor(wheel2, blob, speed)        
        space.add(motor1, motor2)
        return (motor1, motor2)

    def __init__(self, space, pos : Vec2d):
        wheel1 = self.create_wheel(space)
        wheel1.position = pos - (55, 0)        
        wheel2 = self.create_wheel(space)
        wheel2.position = pos + (55, 0)        
        blob = self.create_blob(space)
        blob.position = pos + (0, -25)
        self.motors = self.create_joints(wheel1, wheel2, blob, space)
        
    def speedup(self):
        rate = self.motors[0]._get_rate()
        rate += 0.3
        self.motors[0]._set_rate(rate)
        self.motors[1]._set_rate(rate)

def main():
    fps = 60
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    clock = pygame.time.Clock()
    clock.tick(1)

    space = pymunk.Space()
    space.gravity = 0, 900
    space.sleep_time_threshold = 0.3

    draw_options = pymunk.pygame_util.DrawOptions(screen)
    pymunk.pygame_util.positive_y_is_up = False

    floor = pymunk.Segment(space.static_body, (-100, 500), (1000, 420), 5)
    floor.friction = 1.0
    space.add(floor)

    pos09 = Vec2d(100, 200)
    carar1 = Car(space, pos09 )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        space.step(1.0 / fps)
        
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_UP]:     
            carar1.speedup()     

        screen.fill(pygame.Color("white"))

        space.debug_draw(draw_options)

        pygame.display.flip()

        clock.tick(fps)
        
if __name__=="__main__":
    main()        