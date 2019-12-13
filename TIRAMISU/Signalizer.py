import time
import pygame
import Poser
import Topographer
pygame.init()
COLOUR_LETHALWALL = (0, 0, 0)
COLOUR_BLACKTILE = (0, 0, 0)
COLOUR_PRESENCE = (0, 0, 255)
COLOUR_SPLASHWALL = (80, 80, 80)
COLOUR_FREESPACE = (255, 255, 255)
COLOUR_UNKNOWN = (100, 100, 100)
Display = pygame.display.set_mode((800, 480))
Display.fill(COLOUR_UNKNOWN)
ON_SCREEN_PALETTE = pygame.PixelArray(Display)
LANDMARK_POSITION_LIST = [0]
VICTIM_SPRITE = pygame.image.load('VICTIM_SPRITE.png')
BLINKER_HEATED_SPRITE = pygame.image.load('BlinkerHeated.png')
BLINKER_H_SPRITE = pygame.image.load('BlinkerH.png')
BLINKER_S_SPRITE = pygame.image.load('BlinkerS.png')
BLINKER_U_SPRITE = pygame.image.load('BlinkerU.png')
BLINKER_RED_SPRITE = pygame.image.load('BlinkerRed.png')
BLINKER_YELLOW_SPRITE = pygame.image.load('BlinkerYellow.png')
BLINKER_GREEN_SPRITE = pygame.image.load('BlinkerGreen.png')
EXIT_SPRITE = pygame.image.load('Exit.png')

def GraphicsRefresh():
    LANDMARK_POSITION_LIST.clear()
    for c in range(-100, 101):
        for r in range(-60, 61):
            if Topographer.LANDMARK_MAP[Poser.CURRENT_FLOOR][Poser.ROBOT_POSITION_X + c][Poser.ROBOT_POSITION_Y + r] > 0 and Topographer.LANDMARK_MAP[Poser.CURRENT_FLOOR][Poser.ROBOT_POSITION_X + c][Poser.ROBOT_POSITION_Y + r] <= 7:
                LANDMARK_POSITION_LIST.append(((4*c)+400-25, (4*r)+240-25))
            elif Topographer.WALL_MAP[Poser.CURRENT_FLOOR][Poser.ROBOT_POSITION_X + c][Poser.ROBOT_POSITION_Y + r] == 1:
                for a in range(0, 5):
                    for b in range(0, 5):
                        ON_SCREEN_PALETTE[(4*c)+a+400][(4*r)+b+240] = COLOUR_LETHALWALL
            elif Topographer.LANDMARK_MAP[Poser.CURRENT_FLOOR][Poser.ROBOT_POSITION_X + c][Poser.ROBOT_POSITION_Y + r] == 99:
                for a in range(0, 5):
                    for b in range(0, 5):
                        ON_SCREEN_PALETTE[(4*c)+a+400][(4*r)+b+240] = COLOUR_BLACKTILE
            elif Topographer.PRESENCE_MAP[Poser.CURRENT_FLOOR][Poser.ROBOT_POSITION_X + c][Poser.ROBOT_POSITION_Y + r] == 1:
                for a in range(0, 5):
                    for b in range(0, 5):
                        ON_SCREEN_PALETTE[(4*c)+a+400][(4*r)+b+240] = COLOUR_PRESENCE
            elif Topographer.WALL_SPLASH_MAP[Poser.CURRENT_FLOOR][Poser.ROBOT_POSITION_X + c][Poser.ROBOT_POSITION_Y + r] > 0:
                for a in range(0, 5):
                    for b in range(0, 5):
                        ON_SCREEN_PALETTE[(4*c)+a+400][(4*r)+b+240] = COLOUR_SPLASHWALL
            elif Topographer.WALL_MAP[Poser.CURRENT_FLOOR][Poser.ROBOT_POSITION_X + c][Poser.ROBOT_POSITION_Y + r] == 0:
                for a in range(0, 5):
                    for b in range(0, 5):
                        ON_SCREEN_PALETTE[(4*c)+a+400][(4*r)+b+240] = COLOUR_FREESPACE
            elif Topographer.WALL_MAP[Poser.CURRENT_FLOOR][Poser.ROBOT_POSITION_X + c][Poser.ROBOT_POSITION_Y + r] == -1:
                for a in range(0, 5):
                    for b in range(0, 5):
                        ON_SCREEN_PALETTE[(4*c)+a+400][(4*r)+b+240] = COLOUR_UNKNOWN
    for l in LANDMARK_POSITION_LIST:
        Display.blit(VICTIM_SPRITE, l)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.update()


def SignalizeVictim(VictimType):
    for second in range(1, 11):
        Display.fill((0, 0, 0))
        time.sleep(0.5)
        print('\a')
        if VictimType == 1:
            Display.blit(BLINKER_HEATED_SPRITE, (0, 0))
        elif VictimType == 2:
            Display.blit(BLINKER_H_SPRITE, (0, 0))
        elif VictimType == 3:
            Display.blit(BLINKER_S_SPRITE, (0, 0))
        elif VictimType == 4:
            Display.blit(BLINKER_U_SPRITE, (0, 0))
        elif VictimType == 5:
            Display.blit(BLINKER_RED_SPRITE, (0, 0))
        elif VictimType == 6:
            Display.blit(BLINKER_YELLOW_SPRITE, (0, 0))
        elif VictimType == 7:
            Display.blit(BLINKER_GREEN_SPRITE, (0, 0))
        time.sleep(0.5)
        print('\a')

def SignalizeExit():
    Display.blit(EXIT_SPRITE, (0, 0))
    time.sleep(10)