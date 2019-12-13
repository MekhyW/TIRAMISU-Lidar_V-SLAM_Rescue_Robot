import pygame
import Poser
import Topographer
import time
pygame.init()
colour_lethalwall = (0, 0, 0)
colour_blacktile = (0, 0, 0)
colour_presence = (0, 0, 255)
colour_splashwall = (80, 80, 80)
colour_freespace = (255, 255, 255)
colour_unknown = (100, 100, 100)
Display = pygame.display.set_mode((800, 480))
Display.fill(colour_unknown)
OnScreenPalette = pygame.PixelArray(Display)
LandmarkPositionList = [0]
VictimSprite = pygame.image.load('VictimSprite.png')
BlinkerHeatedSprite = pygame.image.load('BlinkerHeated.png')
BlinkerHSprite = pygame.image.load('BlinkerH.png')
BlinkerSSprite = pygame.image.load('BlinkerS.png')
BlinkerUSprite = pygame.image.load('BlinkerU.png')
BlinkerRedSprite = pygame.image.load('BlinkerRed.png')
BlinkerYellowSprite = pygame.image.load('BlinkerYellow.png')
BlinkerGreenSprite = pygame.image.load('BlinkerGreen.png')
ExitSprite = pygame.image.load('Exit.png')

def GraphicsRefresh():
    LandmarkPositionList.clear()
    for c in range(-100, 101):
        for r in range(-60, 61):
            if(Topographer.LandmarkMap[Poser.CurrentFloor][Poser.RobotPositionX + c][Poser.RobotPositionY + r] > 0 and Topographer.LandmarkMap[Poser.CurrentFloor][Poser.RobotPositionX + c][Poser.RobotPositionY + r] <= 7):
                LandmarkPositionList.append(((4*c)+400-25, (4*r)+240-25))
            elif(Topographer.WallMap[Poser.CurrentFloor][Poser.RobotPositionX + c][Poser.RobotPositionY + r] == 1):
                for a in range(0, 5):
                    for b in range(0, 5):
                        OnScreenPalette[(4*c)+a+400][(4*r)+b+240] = colour_lethalwall
            elif(Topographer.LandmarkMap[Poser.CurrentFloor][Poser.RobotPositionX + c][Poser.RobotPositionY + r] == 99):
                for a in range(0, 5):
                    for b in range(0, 5):
                        OnScreenPalette[(4*c)+a+400][(4*r)+b+240] = colour_blacktile
            elif(Topographer.PresenceMap[Poser.CurrentFloor][Poser.RobotPositionX + c][Poser.RobotPositionY + r] == 1):
                for a in range(0, 5):
                    for b in range(0, 5):
                        OnScreenPalette[(4*c)+a+400][(4*r)+b+240] = colour_presence
            elif(Topographer.WallSplashMap[Poser.CurrentFloor][Poser.RobotPositionX + c][Poser.RobotPositionY + r] > 0):
                for a in range(0, 5):
                    for b in range(0, 5):
                        OnScreenPalette[(4*c)+a+400][(4*r)+b+240] = colour_splashwall
            elif(Topographer.WallMap[Poser.CurrentFloor][Poser.RobotPositionX + c][Poser.RobotPositionY + r] == 0):
                for a in range(0, 5):
                    for b in range(0, 5):
                        OnScreenPalette[(4*c)+a+400][(4*r)+b+240] = colour_freespace
            elif(Topographer.WallMap[Poser.CurrentFloor][Poser.RobotPositionX + c][Poser.RobotPositionY + r] == -1):
                for a in range(0, 5):
                    for b in range(0, 5):
                        OnScreenPalette[(4*c)+a+400][(4*r)+b+240] = colour_unknown
    for l in LandmarkPositionList:
        Display.blit(VictimSprite, l)
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
        if(VictimType==1):
            Display.blit(BlinkerHeatedSprite, (0, 0))
        elif(VictimType==2):
            Display.blit(BlinkerHSprite, (0, 0))
        elif(VictimType==3):
            Display.blit(BlinkerSSprite, (0, 0))
        elif(VictimType==4):
            Display.blit(BlinkerUSprite, (0, 0))
        elif(VictimType==5):
            Display.blit(BlinkerRedSprite, (0, 0))
        elif(VictimType==6):
            Display.blit(BlinkerYellowSprite, (0, 0))
        elif(VictimType==7):
            Display.blit(BlinkerGreenSprite, (0, 0))
        time.sleep(0.5)
        print('\a')

def SignalizeExit():
    Display.blit(ExitSprite, (0, 0))
    time.sleep(10)