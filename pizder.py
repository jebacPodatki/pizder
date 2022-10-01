import sys
import pygame
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d

class Car(object):
    def create_wheel(self, space):
        color = 252, 21, 90, 255
        mass = 25
        radius = 12.5
        moment = pymunk.moment_for_circle(mass, 10, radius)
        wheel_b = pymunk.Body(mass, moment)
        wheel_s = pymunk.Circle(wheel_b, radius)
        wheel_s.friction = 1.5
        wheel_s.color = color
        space.add(wheel_b, wheel_s)
        return wheel_b

    def create_blob(self, space):
        color = 50, 60, 190, 255
        mass = 25
        size = (40, 25)
        moment = pymunk.moment_for_box(mass, size)
        blob_b = pymunk.Body(mass, moment)
        blob_s = pymunk.Poly.create_box(blob_b, size)
        blob_s.color = color
        space.add(blob_b, blob_s)
        return blob_b

    def create_joints(self, wheel1, wheel2, blob, space):
        space.add(
            pymunk.PinJoint(wheel1, blob, (0, 0), (-12.5, -7.5)),
            pymunk.PinJoint(wheel1, blob, (0, 0), (-12.5, 7.5)),
            pymunk.PinJoint(wheel2, blob, (0, 0), (12.5, -7.5)),
            pymunk.PinJoint(wheel2, blob, (0, 0), (12.5, 7.5)),
        )

        speed = 0
        motor1 = pymunk.SimpleMotor(wheel1, blob, speed)
        motor2 = pymunk.SimpleMotor(wheel2, blob, speed)        
        space.add(motor1, motor2)
        return (motor1, motor2)

    def __init__(self, space, pos : Vec2d):
        wheel1 = self.create_wheel(space)
        wheel1.position = pos - (37.5, 0)
        wheel2 = self.create_wheel(space)
        wheel2.position = pos + (37.5, 0)
        blob = self.create_blob(space)
        blob.position = pos + (0, -12.5)
        self.motors = self.create_joints(wheel1, wheel2, blob, space)
        
    def steer(self, direction):
        rate = self.motors[0]._get_rate()
        rate += direction * 0.5
        self.motors[0]._set_rate(rate)
        self.motors[1]._set_rate(rate)

def create_poly(space, points, mass=5.0, pos=(0, 0)):
    moment = pymunk.moment_for_poly(mass, points)
    body = pymunk.Body(mass, moment)
    body.position = Vec2d(*pos)
    shape = pymunk.Poly(body, points)
    shape.friction = 0.001
    shape.collision_type = 0
    space.add(body, shape)

def create_box(space, pos, size=10, mass=5.0):
    box_points = [(-size, -size), (-size, size), (size, size), (size, -size)]
    return create_poly(space, box_points, mass=mass, pos=pos)

def create_wall_segments(space, points):
    points = [Vec2d(*p) for p in points]
    for i in range(len(points) - 1):
        v1 = Vec2d(points[i].x, points[i].y)
        v2 = Vec2d(points[i + 1].x, points[i + 1].y)
        wall_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        wall_shape = pymunk.Segment(wall_body, v1, v2, 0.0)
        wall_shape.friction = 1.0
        wall_shape.collision_type = 0
        space.add(wall_body, wall_shape)

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

    floor = pymunk.Segment(space.static_body, (-150, 500), (400, 420), 5)
    floor.friction = 1.0
    space.add(floor)

    floor2 = pymunk.Segment(space.static_body, (700, 420), (1200, 530), 5)
    floor2.friction = 1.0
    space.add(floor2)

    h = 400
    for y in range(1, h):
        x = 0
        s = 5
        p = Vec2d(450, -1800) + Vec2d(y / 20 * s * 2, y % 20 * s * 2)
        create_box(space, p, size=s, mass=1)
    create_wall_segments(space, [(430, 500), (440, 650), (660, 650), (670, 500)])

    pos09 = Vec2d(100, 200)
    carar1 = Car(space, pos09 )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        space.step(1.0 / fps)
        
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_RIGHT]:
            carar1.steer(1)
        if keys[pygame.K_LEFT]:
            carar1.steer(-1)

        screen.fill(pygame.Color("white"))

        space.debug_draw(draw_options)

        pygame.display.flip()

        clock.tick(fps)
        
if __name__=="__main__":
    main()        