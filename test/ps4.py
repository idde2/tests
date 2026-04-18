import pygame

pygame.init()
pygame.joystick.init()

controller = pygame.joystick.Joystick(0)
controller.init()
axe = [0.0, 0.0, 0.0, 0.0, 0.0,0.0]
btn = [""] * 20

while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            btn[event.button] = True
        elif event.type == pygame.JOYBUTTONUP:
            btn[event.button] = ""
        if event.type == pygame.JOYAXISMOTION:
            axe[event.axis] = round(event.value,2)
        print(axe,btn)