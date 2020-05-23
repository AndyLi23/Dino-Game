import pygame
from pygame.locals import *
import time
from random import randint
import numpy


def text_objects(text, font):
    textSurface = font.render(text, True, (255, 255, 255))
    return textSurface, textSurface.get_rect()


def rect_distance(x1, y1, x1b, y1b, x2, y2, x2b, y2b):
    left = x2b < x1
    right = x1b < x2
    bottom = y2b < y1
    top = y1b < y2
    if left:
        return x2b - x1
    elif right:
        return x2 - x1b
    elif bottom:
        return y2b - y1
    elif top:
        return y2 - y1b
    else:
        return float('inf')


def dist(a, b, c, d):
    return ((a-b)**2 + (c-d)**2)**0.5


class ai:
    def __init__(self):
        self.d = 0

    def update(self, d):
        self.d = d

    def get(self):
        return self.d


class Player(pygame.sprite.Sprite):

    def __init__(self, ai):

        super(Player, self).__init__()

        self.surf = pygame.Surface((40, 60))

        self.surf.fill((randint(0, 255), randint(0, 255), randint(0, 255)))

        self.rect = self.surf.get_rect()

        self.rect.left = 80
        self.rect.bottom = 360

        self.jumping = False
        self.gravity = 1.2
        self.time = 0
        self.adding = False
        self.delay = 0
        self.target = 300
        self.ai = ai

    def update(self, dist):
        if dist < self.ai.get():
            pressed = True
        else:
            pressed = False

        if pressed and not self.jumping:
            self.jumping = True
            self.time = 0
            self.adding = True
            self.delay = 20
            self.target = 300
            self.cnt = 1

        if self.jumping:
            self.rect.top = self.target - \
                int(self.time**0.5 * 100 * self.gravity)
            if not self.adding:
                self.time -= 0.1
            else:
                self.time += 0.1

            if self.time < 0:
                self.jumping = False
            elif self.time > 1:
                self.adding = False

    def getAI(self):
        return self.ai.get()


class Cactus():
    def __init__(self):
        self.surf = pygame.Surface((randint(30, 50), randint(50, 100)))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.bottom = 360
        self.rect.left = 720

    def update(self, SPEED):
        self.rect.left -= SPEED
        if self.rect.left < -40:
            return True
        else:
            return False


class Game:
    def __init__(self, k):
        pygame.init()
        pygame.display.set_caption("Dino Game")
        width = 720
        height = 360
        self.screen = pygame.display.set_mode((width, height))
        self.exit = False
        self.default = False
        if k == True:
            self.default = True
        else:
            l = []
            for i, j in list(k.items())[-4:]:
                l.insert(0, i.getAI())
            self.stack = set()
            for a in l:
                for b in l:
                    for c in l:
                        self.stack.add((a+b+c+randint(-300, 300))/3)

    def run(self):
        players = []
        for i in range(10):
            ai_ = ai()
            if self.default:
                ai_.update(randint(-500, 500))
            else:
                ai_.update(self.stack.pop())
            player = Player(ai_)
            players.append(player)
        self.cnt = 0
        cactuses = []
        max_dist = 40
        SPEED = 10
        self.goal = randint(22, max_dist)
        self.score = 0
        die = {}

        while not self.exit:
            self.cnt = (self.cnt+1) % self.goal
            if self.cnt == 0:
                self.goal = randint(25, max_dist)
                cactuses.append(Cactus())
                SPEED = min(SPEED+1, 13)
                max_dist = max(max_dist-1, 28)

            self.score += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            def getCactusDistance(player):
                try:
                    return min(rect_distance(player.rect.left, player.rect.top, player.rect.right, player.rect.bottom, c.rect.left, c.rect.top, c.rect.right, c.rect.bottom) for c in cactuses if rect_distance(player.rect.left, player.rect.top, player.rect.right, player.rect.bottom, c.rect.left, c.rect.top, c.rect.right, c.rect.bottom) >= 0)
                except:
                    return float('inf')

            for player in players:
                player.update(getCactusDistance(player))

            print(len(players))

            # Drawing
            self.screen.fill((200, 200, 200))

            for player in players:
                self.screen.blit(player.surf, player.rect)
            i = 0
            while True:
                if i >= len(cactuses):
                    break
                j = cactuses[i].update(SPEED)
                if j:
                    del cactuses[i]
                else:
                    p = 0
                    while True:
                        if len(players) == 0:
                            self.exit = True
                        if p >= len(players):
                            break
                        if cactuses[i].rect.colliderect(players[p].rect):
                            die[players[p]] = self.score
                            del players[p]
                        else:
                            p += 1

                    self.screen.blit(cactuses[i].surf, cactuses[i].rect)
                    i += 1

            largeText = pygame.font.Font('freesansbold.ttf', 20)
            TextSurf, TextRect = text_objects(str(self.score), largeText)
            TextRect.center = (40, 20)
            self.screen.blit(TextSurf, TextRect)

            pygame.display.flip()

        return die


if __name__ == '__main__':
    k = True
    while True:
        game = Game(k)
        k = game.run()
