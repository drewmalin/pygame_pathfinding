import pygame
import sys
import pyganim
import random
from astar import PathManager

from pygame.locals import *
from static_entity import StaticEntity

pygame.init()
window = width, height = (640, 480)
windowSurface = pygame.display.set_mode(window)
clock = pygame.time.Clock()

walkLeftAnim = pyganim.PygAnimation(
    [('resources/duderunleft/duderunleft0.tiff', 0.1),
     ('resources/duderunleft/duderunleft1.tiff', 0.1),
     ('resources/duderunleft/duderunleft2.tiff', 0.1),
     ('resources/duderunleft/duderunleft3.tiff', 0.1),
     ('resources/duderunleft/duderunleft4.tiff', 0.1),
     ('resources/duderunleft/duderunleft5.tiff', 0.1),
     ('resources/duderunleft/duderunleft6.tiff', 0.1),
     ('resources/duderunleft/duderunleft7.tiff', 0.1)])

walkRightAnim = pyganim.PygAnimation(
    [('resources/duderunright/duderunright0.tiff', 0.1),
     ('resources/duderunright/duderunright1.tiff', 0.1),
     ('resources/duderunright/duderunright2.tiff', 0.1),
     ('resources/duderunright/duderunright3.tiff', 0.1),
     ('resources/duderunright/duderunright4.tiff', 0.1),
     ('resources/duderunright/duderunright5.tiff', 0.1),
     ('resources/duderunright/duderunright6.tiff', 0.1),
     ('resources/duderunright/duderunright7.tiff', 0.1)])

walkFrontAnim = pyganim.PygAnimation(
    [('resources/duderunfront/duderunfront0.tiff', 0.1),
     ('resources/duderunfront/duderunfront1.tiff', 0.1),
     ('resources/duderunfront/duderunfront2.tiff', 0.1),
     ('resources/duderunfront/duderunfront3.tiff', 0.1),
     ('resources/duderunfront/duderunfront4.tiff', 0.1),
     ('resources/duderunfront/duderunfront5.tiff', 0.1),
     ('resources/duderunfront/duderunfront6.tiff', 0.1),
     ('resources/duderunfront/duderunfront7.tiff', 0.1)])

walkBackAnim = pyganim.PygAnimation(
    [('resources/duderunback/duderunback0.tiff', 0.1),
     ('resources/duderunback/duderunback1.tiff', 0.1),
     ('resources/duderunback/duderunback2.tiff', 0.1),
     ('resources/duderunback/duderunback3.tiff', 0.1),
     ('resources/duderunback/duderunback4.tiff', 0.1),
     ('resources/duderunback/duderunback5.tiff', 0.1),
     ('resources/duderunback/duderunback6.tiff', 0.1),
     ('resources/duderunback/duderunback7.tiff', 0.1)])

walkLeftAnim.play()
walkRightAnim.play()
walkFrontAnim.play()
walkBackAnim.play()

target = [16, 16]
current = [16, 16]
anim = walkFrontAnim
debug_path = []
path = None
obstacles = []
blocked_nodes = []
debug = True

# generate obstacles
for i in range(80):
    o = StaticEntity([random.randint(0, width), random.randint(0, height)], random.randint(10, 50), random.randint(10, 50))
    obstacles.append(o)

    for node in o.nodes():
        blocked_nodes.append(node)

# create manager to handle all pathing requests
path_manager = PathManager(obstacles=blocked_nodes)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            target = event.pos
            path = path_manager.generate_path((current[0], current[1]),
                                              (target[0], target[1]))
            debug_path = path.get_path()

    # Clear screen
    windowSurface.fill((0, 0, 0))

    # test astar
    if debug and path:
        for node in path.get_closed_nodes():
            pygame.draw.circle(windowSurface, (255, 0, 0), node, 1, 1)
        for node in path.get_open_nodes():
            pygame.draw.circle(windowSurface, (255, 255, 0), node, 1, 1)

    if len(debug_path) > 1:
        pygame.draw.lines(windowSurface, (0, 255, 0), False, debug_path, 1)
        current = debug_path[0]
        debug_path.remove(current)
        anim.blit(windowSurface, (current[0] - 16, current[1] - 16))

    # If no movement, idle the animation at the first frame
    else:
        anim.blitFrameNum(0, windowSurface, (current[0] - 16, current[1] - 16))

    # draw obstacles
    for obstacle in obstacles:
        obstacle.draw(windowSurface)

    # Swap the buffers
    pygame.display.flip()
    clock.tick(60)
