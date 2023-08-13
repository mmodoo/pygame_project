""" cave - Copyright 2016 Kenichiro Tanaka  """
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 17:44:13 2023

@author: HWI
"""

import sys
from random import randint
import pygame
from pygame.locals import QUIT, Rect, KEYDOWN, K_SPACE, K_r

pygame.init()
pygame.key.set_repeat(5, 5)
SURFACE = pygame.display.set_mode((800, 600))
FPSCLOCK = pygame.time.Clock()


def main():
    """메인 루틴"""
    walls = 80
    ship_y = 250
    velocity = 0
    score = 0
    slope = randint(1, 6)
    sysfont = pygame.font.SysFont(None, 36)
    ship_image = pygame.image.load("ship.png")
    ship = ship_image.get_rect()
    bang_image = pygame.image.load("bang.png")
    obstacle_image = pygame.image.load("obstacle.png")
    obstacle = obstacle_image.get_rect()
    obstacle.center = (700, 400)

    holes = []
    for xpos in range(walls):
        holes.append(Rect(xpos * 10, 100, 10, 400))

    game_over = False

    while True:
        is_space_down = False
        is_rkey_down = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    is_space_down = True
                elif event.key == K_r:
                    is_rkey_down = True

        # 내 캐릭터를 이동
        if not game_over:
            score += 10
            velocity += -1 if is_space_down else 1
            ship_y += velocity

            # 동굴을 스크롤
            edge = holes[-1].copy()
            test = edge.move(0, slope)
            if test.top <= 0 or test.bottom >= 600:
                slope = randint(1, 6) * (-1 if slope > 0 else 1)
                edge.inflate_ip(0, -20)
            edge.move_ip(10, slope)
            holes.append(edge)
            del holes[0]
            holes = [x.move(-10, 0) for x in holes]

            # 충돌?
            if holes[0].top > ship_y or holes[0].bottom < ship_y + 80:
                game_over = True

            if (
                ship_y + 40 > obstacle.top
                and ship.right > obstacle.left
                and ship_y - 40 < obstacle.bottom
            ):
                game_over = True

        # 그리기
        SURFACE.fill((0, 125, 125))

        for hole in holes:
            pygame.draw.rect(SURFACE, (0, 0, 0), hole)
        SURFACE.blit(ship_image, (0, ship_y))
        score_image = sysfont.render("score is {}".format(score), True, (0, 0, 225))
        SURFACE.blit(score_image, (600, 20))

        # 장애물 생성 코드
        if not game_over:
            obstacle.move_ip(-13, 0)

            pygame.draw.rect(SURFACE, (255, 255, 255), obstacle)

            # 그림과 장애물 합치기
            obstacle2_center = list(obstacle.center)
            [x, y] = obstacle2_center
            obstacle_pos = Rect(x - 26, y - 25, 26, 25)

            SURFACE.blit(obstacle_image, obstacle_pos)

            print(
                obstacle.left,
                obstacle.top,
                ship_y,
                ship.right,
            )

            if obstacle.right < 50:
                slope2 = randint(-3, 3)
                obstacle.center = (700, 300 + slope2 * 50)

        if game_over:
            SURFACE.blit(bang_image, (0, ship_y - 40))
            restart_image = sysfont.render("Restart : Press R key", True, (255, 0, 0))
            SURFACE.blit(restart_image, (280, 300))
            if is_rkey_down:
                main()

        pygame.display.update()
        FPSCLOCK.tick(20)


if __name__ == "__main__":
    main()
