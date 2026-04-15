import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
import pygame
import sys
import random
 
i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1115(i2c)

chan_x = AnalogIn(ads, 0)

chan_y = AnalogIn(ads, 1)
 
SW_PIN = 17 

GPIO.setmode(GPIO.BCM)

GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
 
pygame.init()

WIDTH, HEIGHT = 800, 600

BLOCK_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Joystick Snake")

clock = pygame.time.Clock()
 
COLOR_BG = (30, 30, 30)

COLOR_SNAKE = (0, 255, 0)

COLOR_FOOD = (255, 0, 0)
 
CENTER_V = 1.65

THRESHOLD = 0.5
 
def reset_game():

    snake = [[WIDTH // 2, HEIGHT // 2]]

    direction = [BLOCK_SIZE, 0]

    food = spawn_food(snake)

    return snake, direction, food, False
 
def spawn_food(snake):

    while True:

        pos = [random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,

               random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]

        if pos not in snake:

            return pos
 
def get_joystick_direction(current_dir):

    vx = chan_x.voltage - CENTER_V

    vy = chan_y.voltage - CENTER_V

    new_dir = current_dir

    if vx > THRESHOLD and current_dir[0] >= 0:

        new_dir = [BLOCK_SIZE, 0]

    elif vx < -THRESHOLD and current_dir[0] <= 0:

        new_dir = [-BLOCK_SIZE, 0]

    if vy > THRESHOLD and current_dir[1] >= 0:

        new_dir = [0, BLOCK_SIZE]

    elif vy < -THRESHOLD and current_dir[1] <= 0:

        new_dir = [0, -BLOCK_SIZE]

    return new_dir
 
snake, direction, food, game_over = reset_game()

running = True
 
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False
 
    if not game_over:

        direction = get_joystick_direction(direction)

        new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]

        if (new_head[0] < 0 or new_head[0] >= WIDTH or

            new_head[1] < 0 or new_head[1] >= HEIGHT or

            new_head in snake):

            game_over = True

        else:

            snake.insert(0, new_head)

            if new_head == food:

                food = spawn_food(snake)

            else:

                snake.pop() 

    else:

        if GPIO.input(SW_PIN) == GPIO.LOW:

            snake, direction, food, game_over = reset_game()
 
    screen.fill(COLOR_BG)

    for part in snake:

        pygame.draw.rect(screen, COLOR_SNAKE, (part[0], part[1], BLOCK_SIZE-2, BLOCK_SIZE-2))

    pygame.draw.rect(screen, COLOR_FOOD, (food[0], food[1], BLOCK_SIZE-2, BLOCK_SIZE-2))

    if game_over:

        font = pygame.font.SysFont(None, 55)

        msg = font.render("GAME OVER - Press Button", True, (255, 255, 255))

        screen.blit(msg, (WIDTH//2 - 200, HEIGHT//2))
 
    pygame.display.flip()

    clock.tick(10)
 
pygame.quit()

GPIO.cleanup()

sys.exit()