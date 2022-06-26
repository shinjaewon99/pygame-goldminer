# 충돌 처리

import math
import os
import pygame


# 집게 클래스
class Claw(pygame.sprite.Sprite):
    def __init__(self,image , position):
        super().__init__()
        self.image = image
        self.original_image = image
        self.rect = image.get_rect(center = position)

        self.offset = pygame.math.Vector2(default_offset_x_claw ,0)
        self.position = position


        self.direction = LEFT #집게의 이동방향
        self.angle_speed = 2.5 # 집게의 각도 변경 폭  (좌우 이동 속도)

        self.angle = 10 # 최초의 각도정의

    def update(self , to_x): 
        if self.direction == LEFT:  # 왼쪾 방향으로 이동 하고 있다면
            self.angle += self.angle_speed  # 이동 속도만큼 각도 증가

        elif self.direction ==RIGHT: # 오른쪽 방향으로  이동하고 있다면
            self.angle -= self.angle_speed

        # 만약에 허용 각도 범위를 벗어난다면

        if self.angle >170:
            self.angle = 170
            self.set_direction(RIGHT) 
        elif self.angle <10:
            self.angle = 10
            self.set_direction(LEFT)
        
        self.offset.x += to_x

        self.rotate()  # 회전 처리


    
 
 


       # rect_center = self.position + self.offset
       # self.rect = self.image.get_rect(center = rect_center)

    
    def rotate(self):
        self.image = pygame.transform.rotozoom(self.original_image, -self.angle, 1) # 회전 대상 이미지 , 회전각도 , 이미지 크기
        
        offset_rotated = self.offset.rotate(self.angle)
        
        
        self.rect = self.image.get_rect(center=self.position + offset_rotated)
       
        pygame.draw.rect(screen, RED , self.rect, 1)
        
        
    def set_direction (self, direction):
        self.direction = direction 

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.circle(screen, RED, self.position , 3)
        pygame.draw.line(screen , Black , self.position , self.rect.center ,5) # 직선 그리기
    

    def set_init_state(self):
        self.offset.x =default_offset_x_claw
        self.angle = 10
        self.direction = LEFT

# 보석 클래스
class stone(pygame.sprite.Sprite):
    def __init__(self, image, position , price , speed):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
        self.price = price
        self.speed = speed

    def set_position(self,position,angle):

        r = self.rect.size[0] // 2 # 동그라미 이미지 기준으로 반지름
        rad_angle = math.radians(angle) # 각도
        to_x = r * math.cos(rad_angle) # 삼각형의 밑변
        to_y = r * math.sin(rad_angle) # 삼각형의 높이
        self.rect.center = (position[0] + to_x, position[1] + to_y)


def setup_stone():
    small_gold_price, small_gold_speed = 100, 5
    big_gold_price, big_gold_speed = 300, 2
    stone_price, stone_speed = 10, 2
    diamond_price, diamond_speed = 600, 7

    # 작은 금
    small_gold = stone(stone_images[0], (200, 380), small_gold_price, small_gold_speed) # 0번째 이미지를 (200, 380) 위치에
    stone_group.add(small_gold) # 그룹에 추가
    # 큰 금
    stone_group.add(stone(stone_images[1], (300, 500), big_gold_price, big_gold_speed))
    # 돌
    stone_group.add(stone(stone_images[2], (300, 380), stone_price, stone_speed))
    # 다이아몬드
    stone_group.add(stone(stone_images[3], (900, 420), diamond_price, diamond_speed))



pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gold Miner jaewon game")
clock = pygame.time.Clock()

# 색깔 변수
RED = (255,0,0) # 빨강

Black = (0,0,0)

# 게임 관련 변수

default_offset_x_claw = 40 # 중심점으로부터 집게까지의 x 거리
to_x = 0 # x 좌표 기준으로 집게 이미지를 이동 시킬 값 저장 변수
caught_stone = None #집게를 뻗어서 잡음

# 속도 변수

move_speed = 12 # 발사할때 집게 속도
return_speed = 20 # 아무것도 없이 돌아올때



LEFT = -1 #왼쪽 방향
STOP = 0 # 고정인 상태
RIGHT = 1 # 오른쪽 방향

# 배경 이미지 불러오기
current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
background = pygame.image.load(os.path.join(current_path, "background.png"))

# 4개 보석 이미지 불러오기 (작은 금, 큰 금, 돌, 다이아몬드)
stone_images = [
    pygame.image.load(os.path.join(current_path, "small_gold.png")), # 작은 금
    pygame.image.load(os.path.join(current_path, "big_gold.png")), # 큰 금
    pygame.image.load(os.path.join(current_path, "stone.png")), # 돌
    pygame.image.load(os.path.join(current_path, "diamond.png"))
    ] # 다이아몬드

# 보석 그룹
stone_group = pygame.sprite.Group()

setup_stone() # 게임에 원하는 만큼의 보석을 정의


# 집게

claw_image = pygame.image.load(os.path.join(current_path, "claw.png"))
claw = Claw(claw_image, (screen_width // 2 , 110)) # 가로위치는  화면 가로 크기로 절반 

running = True
while running:
    clock.tick(30) # FPS 값이 30 으로 고정

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type ==pygame.MOUSEBUTTONDOWN: #마우스 버튼 누를때 집게를 뻗음
            claw.set_direction(STOP)
            to_x = move_speed # move_speed 만큼 속도 반영
    if claw.rect.left < 0 or   claw.rect.right > screen_width or claw.rect.bottom >screen_height:
        to_x = -return_speed

    if claw.offset.x < default_offset_x_claw : # 원위치
        to_x = 0
        claw.set_init_state() # 처음상태로 되돌ㄹ림

        if caught_stone : #잡힌보석이 있다면
            # update_score(caught_stone.price) # 점수 업데이트 처리
            stone_group.remove(caught_stone) # 그룹에서 잡힌 보석 제외
            caught_stone =None


    if not caught_stone:  # 잡힌 보석이 없다고 하면
        for stone in stone_group:
            if claw.rect.colliderect(stone.rect):
                caught_stone = stone #잡힌 보석
                to_x = -stone.speed # 잡힌 보석의 속도
                break

        if caught_stone:
            caught_stone.set_position(claw.rect.center, claw.angle)


    screen.blit(background, (0, 0))

    stone_group.draw(screen) # 그룹 내 모든 스프라이트를 screen 에 그려준다
    claw.update(to_x)
    claw.draw(screen)


    pygame.display.update()

pygame.quit()