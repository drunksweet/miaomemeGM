import pygame

class jumpingcat(pygame.sprite.Sprite):

    width = -1
    speedx= -1 #横轴移动的像素点
    speedy= -1 #纵轴移动的像素点

    def __init__(self, color, size, screensize, speed, img=False):
        pygame.sprite.Sprite.__init__(self)
        if img:
            try:
                self.image = pygame.image.load(img)
                self.width = self.image.get_width()
            except Exception as e:
                print("Error loading:", e)
                self.image = pygame.Surface((size, size))
                self.width = size
                self.image.fill(color)
        else:
            self.image = pygame.Surface((size, size))
            self.width = size
            self.image.fill(color)

        self.rect = self.image.get_rect()
        (self.WIDTH, self.HEIGHT) = screensize
        (self.speedx, self.speedy) = speed

    def reset(self,speed):
        self.rect.x = 490
        self.rect.y = 80
        (self.speedx,self.speedy) = speed

    def leftdate(self):
        self.rect.x = self.rect.x + self.speedx
        self.rect.y=

    def rightdate(self):
        self.rect.x = self.rect.x - self.speedx