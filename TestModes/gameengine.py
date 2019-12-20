import random
import time
import pygame
pygame.init()
COLOUR_UNKNOWN = (100, 100, 100)
Display = pygame.display.set_mode((800, 480))
OriginalSurface = pygame.Surface((160, 96))
ON_SCREEN_PALETTE = pygame.PixelArray(OriginalSurface)
OriginalSurface.fill(COLOUR_UNKNOWN)

while True:
    t = time.time()
    for c in range(0, 160):
        for r in range(0, 96):
            ON_SCREEN_PALETTE[c][r] = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
    pygame.transform.scale(OriginalSurface, (800, 480), Display)
    pygame.display.update()
    print(time.time() - t)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()