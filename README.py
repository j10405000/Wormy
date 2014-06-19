Wormy
=====

Use "up down right left" to eat apple. 

# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys
from pygame.locals import *

速度 = 20
視窗寬度 = 640
視窗高度 = 480
格子大小 = 20
assert 視窗寬度 % 格子大小 == 0, "Window width must be a multiple of cell size."
assert 視窗高度 % 格子大小 == 0, "Window height must be a multiple of cell size."
格子寬度 = int(視窗寬度 / 格子大小)
格子高度 = int(視窗高度 / 格子大小)

#             R    G    B
白     = (255, 255, 255)
黑     = (  0,   0,   0)
紅       = (255,   0,   0)
綠     = (  0, 255,   0)
深綠 = (  0, 155,   0)
深灰  = ( 40,  40,  40)
背景色 = 黑

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

def main():
    global 時間, 展示波浪, 基本字型

    pygame.init()
    時間 = pygame.time.Clock()
    展示波浪 = pygame.display.set_mode((視窗寬度, 視窗高度))
    基本字型 = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    展示開始畫面()
    while True:
        執行遊戲()
        展示結束遊系畫面()


def 執行遊戲():
    # Set a random start point.
    開始時的x座標 = random.randint(5, 格子寬度 - 6)
    開始時的y座標 = random.randint(5, 格子高度 - 6)
    貪食蛇座標 = [{'x': 開始時的x座標,     'y': 開始時的y座標},
                  {'x': 開始時的x座標 - 1, 'y': 開始時的y座標},
                  {'x': 開始時的x座標 - 2, 'y': 開始時的y座標}]
    方向 = RIGHT

    # Start the 蘋果 in a random place.
    蘋果 = 取得隨機位子()

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                停止()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and 方向 != RIGHT:
                    方向 = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and 方向 != LEFT:
                    方向 = RIGHT
                elif (event.key == K_UP or event.key == K_w) and 方向 != DOWN:
                    方向 = UP
                elif (event.key == K_DOWN or event.key == K_s) and 方向 != UP:
                    方向 = DOWN
                elif event.key == K_ESCAPE:
                    停止()

        # check if the worm has hit itself or the edge
        if 貪食蛇座標[HEAD]['x'] == -1 or 貪食蛇座標[HEAD]['x'] == 格子寬度 or 貪食蛇座標[HEAD]['y'] == -1 or 貪食蛇座標[HEAD]['y'] == 格子高度:
            return # game over
        for wormBody in 貪食蛇座標[1:]:
            if wormBody['x'] == 貪食蛇座標[HEAD]['x'] and wormBody['y'] == 貪食蛇座標[HEAD]['y']:
                return # game over

        # check if worm has eaten an apply
        if 貪食蛇座標[HEAD]['x'] == 蘋果['x'] and 貪食蛇座標[HEAD]['y'] == 蘋果['y']:
            # don't remove worm's tail segment
            蘋果 = 取得隨機位子() # set a new 蘋果 somewhere
        else:
            del 貪食蛇座標[-1] # remove worm's tail segment

        # move the worm by adding a segment in the 方向 it is moving
        if 方向 == UP:
            newHead = {'x': 貪食蛇座標[HEAD]['x'], 'y': 貪食蛇座標[HEAD]['y'] - 1}
        elif 方向 == DOWN:
            newHead = {'x': 貪食蛇座標[HEAD]['x'], 'y': 貪食蛇座標[HEAD]['y'] + 1}
        elif 方向 == LEFT:
            newHead = {'x': 貪食蛇座標[HEAD]['x'] - 1, 'y': 貪食蛇座標[HEAD]['y']}
        elif 方向 == RIGHT:
            newHead = {'x': 貪食蛇座標[HEAD]['x'] + 1, 'y': 貪食蛇座標[HEAD]['y']}
        貪食蛇座標.insert(0, newHead)
        展示波浪.fill(背景色)
        畫格子()
        畫貪食蛇(貪食蛇座標)
        畫蘋果(蘋果)
        寫分數(len(貪食蛇座標) - 3)
        pygame.display.update()
        時間.tick(速度)

def 展示PressKey訊息():
    pressKeySurf = 基本字型.render('Press a key to play.', True, 深灰)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (視窗寬度 - 200, 視窗高度 - 30)
    展示波浪.blit(pressKeySurf, pressKeyRect)


def 確認鍵被點擊():
    if len(pygame.event.get(QUIT)) > 0:
        停止()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        停止()
    return keyUpEvents[0].key


def 展示開始畫面():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormy!', True, 白, 深綠)
    titleSurf2 = titleFont.render('Wormy!', True, 綠)

    degrees1 = 0
    degrees2 = 0
    while True:
        展示波浪.fill(背景色)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (視窗寬度 / 2, 視窗高度 / 2)
        展示波浪.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (視窗寬度 / 2, 視窗高度 / 2)
        展示波浪.blit(rotatedSurf2, rotatedRect2)

        展示PressKey訊息()

        if 確認鍵被點擊():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        時間.tick(速度)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def 停止():
    pygame.quit()
    sys.exit()


def 取得隨機位子():
    return {'x': random.randint(0, 格子寬度 - 1), 'y': random.randint(0, 格子高度 - 1)}


def 展示結束遊系畫面():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, 白)
    overSurf = gameOverFont.render('Over', True, 白)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (視窗寬度 / 2, 10)
    overRect.midtop = (視窗寬度 / 2, gameRect.height + 10 + 25)

    展示波浪.blit(gameSurf, gameRect)
    展示波浪.blit(overSurf, overRect)
    展示PressKey訊息()
    pygame.display.update()
    pygame.time.wait(500)
    確認鍵被點擊() # clear out any key presses in the event queue

    while True:
        if 確認鍵被點擊():
            pygame.event.get() # clear event queue
            return

def 寫分數(score):
    scoreSurf = 基本字型.render('Score: %s' % (score), True, 白)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (視窗寬度 - 120, 10)
    展示波浪.blit(scoreSurf, scoreRect)


def 畫貪食蛇(貪食蛇座標):
    for coord in 貪食蛇座標:
        x = coord['x'] * 格子大小
        y = coord['y'] * 格子大小
        wormSegmentRect = pygame.Rect(x, y, 格子大小, 格子大小)
        pygame.draw.rect(展示波浪, 深綠, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, 格子大小 - 8, 格子大小 - 8)
        pygame.draw.rect(展示波浪, 綠, wormInnerSegmentRect)


def 畫蘋果(coord):
    x = coord['x'] * 格子大小
    y = coord['y'] * 格子大小
    蘋果Rect = pygame.Rect(x, y, 格子大小, 格子大小)
    pygame.draw.rect(展示波浪, 紅, 蘋果Rect)


def 畫格子():
    for x in range(0, 視窗寬度, 格子大小): # draw vertical lines
        pygame.draw.line(展示波浪, 深灰, (x, 0), (x, 視窗高度))
    for y in range(0, 視窗高度, 格子大小): # draw horizontal lines
        pygame.draw.line(展示波浪, 深灰, (0, y), (視窗寬度, y))


if __name__ == '__main__':
    main()
