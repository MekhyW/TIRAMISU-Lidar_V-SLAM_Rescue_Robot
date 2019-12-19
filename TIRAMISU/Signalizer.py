import time
import pygame
import Poser
import Topographer
pygame.init()
COLOUR_RED = (255, 0, 0)
COLOUR_YELLOW = (255, 255, 0)
COLOUR_GREEN = (0, 255, 0)
COLOUR_BLUE = (0, 0, 255)
COLOUR_LETHALWALL = (0, 0, 0)
COLOUR_BLACKTILE = (0, 0, 0)
COLOUR_PRESENCE = (0, 0, 250)
COLOUR_SPLASHWALL = (80, 80, 80)
COLOUR_FREESPACE = (250, 250, 250)
COLOUR_UNKNOWN = (100, 100, 100)
Display = pygame.display.set_mode((800, 480))
Display.fill(COLOUR_UNKNOWN)
ON_SCREEN_PALETTE = pygame.PixelArray(Display)
LANDMARK_POSITION_LIST = [0]

def graphics_refresh():
    LANDMARK_POSITION_LIST.clear()
    for c in range(-100, 101):
        for r in range(-60, 61):
            if 0 < Topographer.LANDMARK_MAP[Poser.ROBOT_POSITION_X + c][Poser.ROBOT_POSITION_Y + r][Poser.CURRENT_FLOOR] <= 7:
                LANDMARK_POSITION_LIST.append(((4*c)+400-25, (4*r)+240-25))
            elif Topographer.WALL_MAP[Poser.ROBOT_POSITION_X + c][Poser.ROBOT_POSITION_Y + r][Poser.CURRENT_FLOOR] == 1:
                for a in range(4):
                    for b in range(4):
                        ON_SCREEN_PALETTE[(4*c)+a+400][(4*r)+b+240] = COLOUR_LETHALWALL
            elif Topographer.LANDMARK_MAP[Poser.ROBOT_POSITION_X + c][Poser.ROBOT_POSITION_Y + r][Poser.CURRENT_FLOOR] == 99:
                for a in range(4):
                    for b in range(4):
                        ON_SCREEN_PALETTE[(4*c)+a+400][(4*r)+b+240] = COLOUR_BLACKTILE
            elif Topographer.PRESENCE_MAP[Poser.ROBOT_POSITION_X + c][Poser.ROBOT_POSITION_Y + r][Poser.CURRENT_FLOOR] == 1:
                for a in range(4):
                    for b in range(4):
                        ON_SCREEN_PALETTE[(4*c)+a+400][(4*r)+b+240] = COLOUR_PRESENCE
            elif Topographer.WALL_SPLASH_MAP[Poser.ROBOT_POSITION_X + c][Poser.ROBOT_POSITION_Y + r][Poser.CURRENT_FLOOR] > 0:
                for a in range(4):
                    for b in range(4):
                        ON_SCREEN_PALETTE[(4*c)+a+400][(4*r)+b+240] = COLOUR_SPLASHWALL
            elif Topographer.WALL_MAP[Poser.ROBOT_POSITION_X + c][Poser.ROBOT_POSITION_Y + r][Poser.CURRENT_FLOOR] == 0:
                for a in range(4):
                    for b in range(4):
                        ON_SCREEN_PALETTE[(4*c)+a+400][(4*r)+b+240] = COLOUR_FREESPACE
    for l in LANDMARK_POSITION_LIST:
        pygame.draw.circle(Display, COLOUR_BLUE, l, 10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    pygame.display.update()


def signalize_victim(victim_type):
    for second in range(1, 11):
        Display.fill((0, 0, 0))
        pygame.display.update()
        print('\a')
        time.sleep(0.5)
        if victim_type in (1, 8, 3, 10, 6, 13):
            Display.fill(COLOUR_YELLOW)
        elif victim_type in (2, 9, 5, 12):
            Display.fill(COLOUR_RED)
        elif victim_type in (4, 11, 7, 14):
            Display.fill(COLOUR_GREEN)
        pygame.display.update()
        print('\a')
        time.sleep(0.5)

def signalize_exit_bonus():
    Display.fill(COLOUR_GREEN)
    pygame.display.update()
    time.sleep(10)
