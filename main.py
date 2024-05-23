import sys, pygame
pygame.init()
 
screen = pygame.display.set_mode()
 
size = width, height = screen.get_size()
speed = [1, 1]
black = 255, 255, 255

ball = pygame.image.load("dvd.png")
ballrect = ball.get_rect()
 
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
 
    ballrect = ballrect.move(speed) 

    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]

    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()