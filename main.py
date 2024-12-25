import pygame
import numpy as np
import math
import random

class MovingBall:
    def __init__(self, position, velocity):
        self.position = np.array(position, dtype=np.float64)
        self.velocity = np.array(velocity, dtype=np.float64)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.inside_arc = True

def draw_sector(surface, center, radius, start_angle, eng_angle):
    farthest_point_1 = center + (radius + 1000) * np.array([math.cos(start_angle), math.sin(start_angle)])
    farthest_point_2 = center + (radius + 1000) * np.array([math.cos(end_angle), math.sin(end_angle)])
    pygame.draw.polygon(surface, BLACK, [center, farthest_point_1, farthest_point_2], 0)

def is_ball_in_arc(ball_position, circle_center, angle_start, angle_end):
    delta_x = ball_position[0] - circle_center[0]
    delta_y = ball_position[1] - circle_center[1]
    ball_angle = math.atan2(delta_y, delta_x)
    
    angle_start = angle_start % (2 * math.pi)
    angle_end = angle_end % (2 * math.pi)
    
    if angle_start > angle_end:
        angle_end += 2 * math.pi
        
    if angle_start <= ball_angle <= angle_end or (angle_start <= ball_angle + 2 * math.pi <= angle_end):
        return True
    return False

pygame.init()

WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)

circle_center = np.array([WIDTH // 2, HEIGHT // 2], dtype=np.float64)
circle_radius = 150

ball_radius = 5
initial_position = np.array([WIDTH // 2, HEIGHT // 2 - 120], dtype=np.float64)
ball_velocity = np.array([0, 0], dtype=np.float64)

balls = [MovingBall(initial_position, ball_velocity)]

GRAVITY = 0.2
rotation_speed = 0.01
arc_angle = 60
start_angle = math.radians(-arc_angle / 2)
end_angle = math.radians(arc_angle / 2)

is_running = True

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    start_angle += rotation_speed
    end_angle += rotation_speed

    for ball in balls:
        if ball.position[1] > HEIGHT or ball.position[0] < 0 or ball.position[0] > WIDTH or ball.position[1] < 0:
            balls.remove(ball)
            balls.append(MovingBall(position=[WIDTH // 2, HEIGHT // 2 - 120], velocity=[random.uniform(-4, 4), random.uniform(-1, 1)]))
            balls.append(MovingBall(position=[WIDTH // 2, HEIGHT // 2 - 120], velocity=[random.uniform(-4, 4), random.uniform(-1, 1)]))

        ball.velocity[1] += GRAVITY
        ball.position += ball.velocity

        distance_to_center = np.linalg.norm(ball.position - circle_center)
        if distance_to_center + ball_radius > circle_radius:
            if is_ball_in_arc(ball.position, circle_center, start_angle, end_angle):
                ball.inside_arc = False
            if ball.inside_arc:
                direction_to_center = ball.position - circle_center
                unit_direction = direction_to_center / np.linalg.norm(direction_to_center)
                ball.position = circle_center + (circle_radius - ball_radius) * unit_direction
                
                tangential_direction = np.array([-direction_to_center[1], direction_to_center[0]], dtype=np.float64)
                tangential_velocity = (np.dot(ball.velocity, tangential_direction) / np.dot(tangential_direction, tangential_direction)) * tangential_direction
                ball.velocity = 2 * tangential_velocity - ball.velocity
                ball.velocity += tangential_direction * rotation_speed

    screen.fill(BLACK)
    pygame.draw.circle(screen, ORANGE, circle_center, circle_radius, 3)
    draw_sector(screen, circle_center, circle_radius, start_angle, end_angle)

    for ball in balls:
        pygame.draw.circle(screen, ball.color, ball.position, ball_radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
