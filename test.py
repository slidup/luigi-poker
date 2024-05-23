key = pygame.key.get_pressed()
    if key[pygame.K_d]:
        player.move_ip(1,0)
    if key[pygame.K_z]:
        player.move_ip(0,-1)
    if key[pygame.K_q]:
        player.move_ip(-1,0)
    if key[pygame.K_s]:
        player.move_ip(0,1)