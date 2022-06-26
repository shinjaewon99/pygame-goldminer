# 기본 뼈대 작성
import os
from turtle import back
import pygame


pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width , screen_height))
pygame.display.set_caption("Gold Miner jaewon game")
clock = pygame.time.Clock()


# 배경 불러오기

current_path = os.path.dirname(__file__) # 현재위치 반환
background = pygame.image.load(os.path.join(current_path, "background.png"))


running = True
while running:

    clock.tick(30)  # FPS 값을 30으로 고정
    
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running = False

    screen.blit(background , (0,0))
    pygame.display.update()


pygame.quit()