  1 import pygame
  2 import random
  3 
  4 pygame.init()
  5 
  6 all_sprites = pygame.sprite.Group()
  7 BLACK = (0, 0, 0)
  8 display_width = 800
  9 display_height = 600
 10 
 11 gameDisplay = pygame.display.set_mode((display_width, display_height))
 12 pygame.display.set_caption('Kyudo')
 13 clock = pygame.time.Clock()
 14 
 15 background = pygame.image.load("background.jpg").convert()
 16 background = pygame.transform.scale(background,(display_width, display_height))
 17 screen = pygame.image.load("start.jpg").convert()
 18 screen = pygame.transform.scale(screen,(display_width, display_height))
 19 
 20 font_name = pygame.font.match_font('arial')
 21 
 22 def draw_text(surf, text, size,x,y):
 23     font = pygame.font.Font(font_name, size)
 24     text_surface = font.render(text,True,BLACK)
 25     text_rect = text_surface.get_rect()
 26     text_rect.midtop = (x, y)
 27     surf.blit(text_surface, text_rect)
 28 
 29 class BowArrow(pygame.sprite.Sprite):
 30     def __init__(self):
 31         pygame.sprite.Sprite.__init__(self)
 32         self.image = pygame.image.load("bow7.png")
 33         self.rect = self.image.get_rect()
 34         self.rect.centery = display_height / 2
 35         self.rect.left = 10
 36         self.speedy  = 0
 37 
 38     def update(self):
 39         self.speedx = 0
 40         keystate = pygame.key.get_pressed()
 41         if keystate[pygame.K_UP]:
 42             self.speedy = -50
 43             self.rect.y += self.speedy
 44         if keystate[pygame.K_DOWN]:
 45             self.speedy = 50
 46             self.rect.y += self.speedy
 47         if self.rect.bottom > display_height:
 48             self.rect.bottom = display_height
 49         if self.rect.top < 0:
 50             self.rect.top = 0
 51 
 52     def shoot(self):
 53         arrow = Arrow(self.rect.centery,self.rect.left)
 54         all_sprites.add(arrow)
 55         arrows.add(arrow)
 56 
 57 class Lantern(pygame.sprite.Sprite):
 58     def __init__(self):
 59         pygame.sprite.Sprite.__init__(self)
 60         self.image = pygame.image.load("oie_transparent.png")
 61         self.image = pygame.transform.scale(self.image,(40,40))
 62         self.rect = self.image.get_rect()
 63         self.rect.x = random.randrange(display_height / 2 , display_height)
 64         self.rect.y = random.randrange(-100, -40)
 65         self.speedy = random.randrange(1, 80)
 66 
 67     def update(self):
 68         self.rect.y += self.speedy
 69         if self.rect.top > display_height :
 70             self.rect.x = random.randrange(display_height / 2, display_height)
 71             self.rect.y = random.randrange(-100,-40)
 72             self.speedy = random.randrange(1,80)
 73 
 74 class Arrow(pygame.sprite.Sprite):
 75     def __init__(self, x, y):
 76         pygame.sprite.Sprite.__init__(self)
 77         self.image = pygame.image.load("arrow.png")
 78         self.image = pygame.transform.scale(self.image,(60,10))
 79         self.rect = self.image.get_rect()
 80         self.rect.left = y
 81         self.rect.centery = x
 82         self.speedx = 50
 83 
 84     def update(self):
 85         self.rect.x += self.speedx
 86         if self.rect.right > display_width:
 87             self.kill()
 88 
 89 all_sprites = pygame.sprite.Group()
 90 lantern = pygame.sprite.Group()
 91 arrows = pygame.sprite.Group()
 92 bowarrow = BowArrow()
 93 all_sprites.add(bowarrow)
 94 
 95 
 96 for i in range(10):
 97     m = Lantern()
 98     all_sprites.add(m)
 99     lantern.add(m)
100 
101 
102 def start_screen():
103     gameDisplay.blit(screen,(0,0))
104     draw_text(gameDisplay,"KYUDO",70,520,50)
105     draw_text(gameDisplay, "press any key to START the game",30,545,150)
106     pygame.display.flip()
107     waiting = True
108     while waiting:
109         clock.tick(1)
110         for event in pygame.event.get():
111             if event.type == pygame.KEYUP:
112                 waiting = False
113 
114 def game_over(score):
115     draw_text(gameDisplay,"GAME OVER ",70,400,300)
116     draw_text(gameDisplay,"SCORE :",50,300,400)
117     draw_text(gameDisplay,str(score),50,425,400)
118     pygame.display.update()
119     waiting = True
120     while waiting:
121         clock.tick(1)
122         for event in pygame.event.get():
123             if event.type == pygame.KEYUP:
124                 game_loop()
125                 waiting = False
126 
127 def game_loop():
128     burst = False
129     start = True
130     score = 0
131     lives = 16
132     while not burst :
133         if start:
134             start_screen()
135             start = False
136         for event in pygame.event.get():
137             if event.type == pygame.QUIT:
138                 burst = True
139             elif event.type == pygame.KEYDOWN:
140                 if event.key == pygame.K_SPACE:
141                     lives -= 1
142                     bowarrow.shoot()
143                     if lives == 0:
144                         game_over(score)
145                         burst = True
146 
147             gameDisplay.blit(background,(0,0))
148             all_sprites.update()
149             hits = pygame.sprite.groupcollide(arrows,lantern,True,True )
150             for hit in hits:
151                 score += 1
152                 m = Lantern()
153                 all_sprites.add(m)
154                 lantern.add(m)
155             all_sprites.draw(gameDisplay)
156             draw_text(gameDisplay,"SCORE :",20,730,20)
157             draw_text(gameDisplay, str(score), 20, 780,20)
158             draw_text(gameDisplay,"ARROWS :",20,720,50)
159             draw_text(gameDisplay,str(lives) , 20, 780 ,50)
160             pygame.display.update()
161             clock.tick(5)
162
163 game_loop()
164 pygame.quit()
165 quit()
