import pygame
from pygame.locals import *
import time
from random import randint


def text_objects(text, font):
    textSurface = font.render(text, True, (255, 255, 255))
    return textSurface, textSurface.get_rect()


class Player(pygame.sprite.Sprite):

    def __init__(self):

        super(Player, self).__init__()

        self.surf = pygame.Surface((40, 60))

        self.surf.fill((0, 0, 0))

        self.rect = self.surf.get_rect()

        self.rect.left = 80
        self.rect.bottom = 360

        self.jumping = False
        self.gravity = 1.2
        self.time = 0
        self.adding = False
        self.delay = 0
        self.target = 300

    def update(self, pressed):
        if pressed[K_SPACE] and not self.jumping:
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


class Cactus():
    def __init__(self):
        self.surf = pygame.Surface((randint(10, 60), randint(30, 80)))
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
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Dino Game")
        width = 720
        height = 360
        self.screen = pygame.display.set_mode((width, height))
        self.exit = False

    def run(self):
        player = Player()
        self.cnt = 0
        cactuses = []
        max_dist = 100
        SPEED = 10
        self.goal = randint(30, max_dist)
        self.score = 0

        while not self.exit:
            self.cnt = (self.cnt+1) % self.goal
            if self.cnt == 0:
                self.goal = randint(30, max_dist)
                cactuses.append(Cactus())
                SPEED = min(SPEED+0.1, 20)
                max_dist = max(max_dist-1, 50)

            self.score += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            # User input
            pressed = pygame.key.get_pressed()
            player.update(pressed)

            # Drawing
            self.screen.fill((200, 200, 200))
            self.screen.blit(player.surf, player.rect)
            i = 0
            while True:
                if i >= len(cactuses):
                    break
                j = cactuses[i].update(SPEED)
                if j:
                    del cactuses[i]
                else:
                    if cactuses[i].rect.colliderect(player.rect):
                        self.exit = True
                    self.screen.blit(cactuses[i].surf, cactuses[i].rect)
                    i += 1

            largeText = pygame.font.Font('freesansbold.ttf', 20)
            TextSurf, TextRect = text_objects(str(self.score), largeText)
            TextRect.center = (40, 20)
            self.screen.blit(TextSurf, TextRect)

            pygame.display.flip()

        return True


if __name__ == '__main__':
    while True:
        game = Game()
        game.run()
