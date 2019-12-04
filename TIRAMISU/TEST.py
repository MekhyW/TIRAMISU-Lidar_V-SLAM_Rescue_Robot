import random
from pyglet.gl import *
window = pyglet.window.Window(800, 480, "TEST")
xA=0
yA=0
xB=0
yB=0

def Update(dt):
    xA = random.randint(0, 800)
    yA = random.randint(0, 480)
    xB = random.randint(0, 800)
    yB = random.randint(0, 480)

    
pyglet.clock.schedule_interval(Update, 1/20)

@window.event
def on_draw():
    #glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_LINES)
    glVertex2i(xA, yA)
    glVertex2i(xB, yB)
    glEnd()

pyglet.app.run()