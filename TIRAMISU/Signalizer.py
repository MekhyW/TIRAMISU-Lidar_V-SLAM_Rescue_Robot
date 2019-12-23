import time
import pygame
import Poser
import Topographer
import MotionPlanner
pygame.init()
COLOUR_RED = (255, 0, 0)
COLOUR_YELLOW = (255, 255, 0)
COLOUR_GREEN = (0, 255, 0)
COLOUR_PINK = (255, 0, 255)
COLOUR_LETHALWALL = (0, 0, 0)
COLOUR_BLACKTILE = (0, 0, 0)
COLOUR_PRESENCE = (0, 0, 250)
COLOUR_SPLASHWALL = (80, 80, 80)
COLOUR_FREESPACE = (250, 250, 250)
COLOUR_UNKNOWN = (100, 100, 100)
Display = pygame.display.set_mode((800, 480))
OriginalSurface = pygame.Surface((160, 96))
ON_SCREEN_PALETTE = pygame.PixelArray(OriginalSurface)
OriginalSurface.fill(COLOUR_UNKNOWN)
LANDMARK_POSITION_LIST = []

def graphics_refresh():
    for c in range(-80, 80):
        for r in range(-48, 48):
            if 0 < Topographer.LANDMARK_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X + c)][round(Poser.ROBOT_POSITION_Y + r)] <= 7:
                LANDMARK_POSITION_LIST.append((c+80, r+48))
            elif MotionPlanner.PATH_MAP[round(Poser.ROBOT_POSITION_X + c)][round(Poser.ROBOT_POSITION_Y + r)] == 1:
                ON_SCREEN_PALETTE[c + 80][r + 48] = COLOUR_PINK
            elif Topographer.WALL_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X + c)][round(Poser.ROBOT_POSITION_Y + r)] == 1:
                ON_SCREEN_PALETTE[c + 80][r + 48] = COLOUR_LETHALWALL
            elif Topographer.LANDMARK_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X + c)][round(Poser.ROBOT_POSITION_Y + r)] == 99:
                ON_SCREEN_PALETTE[c + 80][r + 48] = COLOUR_BLACKTILE
            elif Topographer.WALL_SPLASH_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X + c)][round(Poser.ROBOT_POSITION_Y + r)] > 0:
                ON_SCREEN_PALETTE[c + 80][r + 48] = COLOUR_SPLASHWALL
            elif Topographer.PRESENCE_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X + c)][round(Poser.ROBOT_POSITION_Y + r)] == 1:
                ON_SCREEN_PALETTE[c + 80][r + 48] = COLOUR_PRESENCE
            elif Topographer.WALL_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X + c)][round(Poser.ROBOT_POSITION_Y + r)] == 0:
                ON_SCREEN_PALETTE[c + 80][r + 48] = COLOUR_FREESPACE
            elif Topographer.WALL_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X + c)][round(Poser.ROBOT_POSITION_Y + r)] == -1:
                ON_SCREEN_PALETTE[c + 80][r + 48] = COLOUR_UNKNOWN
    for lm in LANDMARK_POSITION_LIST:
        pygame.draw.circle(OriginalSurface, COLOUR_PINK, lm, 10)
        LANDMARK_POSITION_LIST.remove(lm)
        del lm
    pygame.transform.scale(OriginalSurface, (800, 480), Display)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()


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
