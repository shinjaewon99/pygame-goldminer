# 기본 뼈대 작성

import pygame


pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width , screen_height))
pygame.display.set_caption("Gold Miner jaewon game")

clock = pygame.time.Clock()

running = True
while running:

    clock.tick(30)  # FPS 값을 30으로 고정
    
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running = False


pygame.quit()