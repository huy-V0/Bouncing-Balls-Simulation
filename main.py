import pygame
import numpy as np
import math
import random
from settings import *

pygame.init()
pygame.display.set_caption("Bouncing Balls")

class Ball:
    def __init__(self, position, velocity):
        self.position = np.array(position, dtype=np.float64)
        self.velocity = np.array(velocity, dtype=np.float64)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.inside_arc = True

def draw_sector(surface, center, radius, start_angle, end_angle, color):
    farthest_p1 = center + (radius + 1000) * np.array([math.cos(start_angle), math.sin(start_angle)])
    farthest_p2 = center + (radius + 1000) * np.array([math.cos(end_angle), math.sin(end_angle)])
    pygame.draw.polygon(surface, color, [center, farthest_p1, farthest_p2], 0)

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

def color_transition(start_color, end_color, t):
    return tuple(int(start + (end - start) * t) for start, end in zip(start_color, end_color))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

circle_center = np.array(CIRCLE_CENTER, dtype=np.float64)
circle_radius = CIRCLE_RADIUS

ball_velocity = np.array([0, 0], dtype=np.float64)

initial_pos = np.array(INITIAL_BALL_POS, dtype=np.float64)
balls = [Ball(initial_pos, ball_velocity)]

start_angle = math.radians(-ARC_ANGLE / 2)
end_angle = math.radians(ARC_ANGLE / 2)

dragging_circle = False
dragging_resize = False
previous_mouse_pos = None
rotation_angle_offset = 0
resizing_radius = False

background_color = (0, 0, 0)
target_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
color_transition_speed = 0.001

is_running = True
time_passed = 0
while is_running:
    balls_to_remove = []  
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = np.array(pygame.mouse.get_pos())

            if np.linalg.norm(mouse_pos - circle_center) >= circle_radius - 10 and np.linalg.norm(mouse_pos - circle_center) <= circle_radius + 10:
                resizing_radius = True
                previous_mouse_pos = mouse_pos

            if np.linalg.norm(mouse_pos - circle_center) <= circle_radius:
                dragging_circle = True
                previous_mouse_pos = mouse_pos
                rotation_angle_offset = math.atan2(mouse_pos[1] - circle_center[1], mouse_pos[0] - circle_center[0])
                
        if event.type == pygame.MOUSEBUTTONUP:
            dragging_circle = False
            resizing_radius = False

        if event.type == pygame.MOUSEMOTION:
            mouse_pos = np.array(pygame.mouse.get_pos())

            if dragging_circle:
                angle_from_center = math.atan2(mouse_pos[1] - circle_center[1], mouse_pos[0] - circle_center[0])
                angle_diff = angle_from_center - rotation_angle_offset
                start_angle += angle_diff
                end_angle += angle_diff
                rotation_angle_offset = angle_from_center

            if resizing_radius:
                distance_to_mouse = np.linalg.norm(mouse_pos - circle_center)
                circle_radius = max(50, min(300, distance_to_mouse))

    for ball in balls:
        ball.velocity[1] += GRAVITY
        ball.position += ball.velocity

        dist_to_center = np.linalg.norm(ball.position - circle_center)
        if dist_to_center + BALL_RADIUS > circle_radius:
            if is_ball_in_arc(ball.position, circle_center, start_angle, end_angle):
                ball.inside_arc = False
            if ball.inside_arc:
                direction_to_center = ball.position - circle_center
                unit_direction = direction_to_center / np.linalg.norm(direction_to_center)
                ball.position = circle_center + (circle_radius - BALL_RADIUS) * unit_direction
                
                tangential_direction = np.array([-direction_to_center[1], direction_to_center[0]], dtype=np.float64)
                tangential_velocity = (np.dot(ball.velocity, tangential_direction) / np.dot(tangential_direction, tangential_direction)) * tangential_direction
                ball.velocity = 2 * tangential_velocity - ball.velocity
                ball.velocity += tangential_direction * ROTATION_SPEED

        if ball.position[1] > HEIGHT or ball.position[0] < 0 or ball.position[0] > WIDTH or ball.position[1] < 0:
            balls_to_remove.append(ball)

    for ball in balls_to_remove:
        balls.remove(ball)
        
    for ball in balls_to_remove:
        balls.append(Ball(position=[WIDTH // 2, HEIGHT // 2 - 120], velocity=[random.uniform(-4, 4), random.uniform(-1, 1)]))
        balls.append(Ball(position=[WIDTH // 2, HEIGHT // 2 - 120], velocity=[random.uniform(-4, 4), random.uniform(-1, 1)]))

    time_passed += color_transition_speed
    if time_passed >= 1:
        target_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        time_passed = 0

    background_color = color_transition(background_color, target_color, time_passed)
    triangle_color = background_color

    screen.fill(background_color)
    pygame.draw.circle(screen, ORANGE, circle_center, circle_radius, 3)
    draw_sector(screen, circle_center, circle_radius, start_angle, end_angle, triangle_color)

    for ball in balls:
        pygame.draw.circle(screen, ball.color, ball.position, BALL_RADIUS)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
