import pygame

# Screen dimensions
WIDTH = 800
HEIGHT = 800

# Colors 
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)

# Circle and ball 
BALL_RADIUS = 5
CIRCLE_RADIUS = 150
GRAVITY = 0.2
ROTATION_SPEED = 0.01
ARC_ANGLE = 60

# Initial positions
CIRCLE_CENTER = (WIDTH // 2, HEIGHT // 2)
INITIAL_BALL_POS = (WIDTH // 2, HEIGHT // 2 - 120)

FPS = 60

pygame.init()
pygame.mixer.init()
