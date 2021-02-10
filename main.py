import pygame

size = (1000, 520)
sky_col = (200, 220, 255)
running = True
gravity = 1
d = 0
stopping = 1
goingL = False
goingR = False
walkingX = False
list_toUpdate = []


# BOARD Code


class Board:
    def __init__(self, row, col):
        self.mapEnd = None
        self.mapList = []
        self.texture_list = []
        self.bList = []
        self.row = row
        self.col = col
        self.char_loc = ()
        self.charxy = (0, 0)
        self.camera_checkpoint = 300
        self.end_camera_cp = 2201
        for i in range(self.row):
            bListj = []
            for j in range(self.col):
                bListj.append((((j - 1) * 50, i * 50), (j * 50, 50 * (i + 1)), '.'))  # x0,y0;x,y;block
            self.bList.append(bListj)

    def sort_map_text(self, fileName):
        mapFile = [elem for num, elem in enumerate(open(fileName, 'r'))]

        for i in range(self.row):
            line = mapFile[i].rstrip('\n')
            self.mapList.append(line)
        maxlen = max(map(lambda x: len(x), self.mapList))
        list(map(lambda x: [x[i] for i in range(len(x))], self.mapList))

        for i in range(self.row):
            for j in range(self.col):
                q = self.bList[i][j]
                self.bList[i][j] = (q[0], q[1], self.mapList[i][j])

    def render_map(self):
        for i in range(self.row):
            tl1 = []
            for j in range(self.col):
                elem = self.bList[i][j]
                if elem[2] == '#':
                    grass = Grass()
                    grass.rect.x, grass.rect.y = elem[0]
                    tl1.append(grass)
                if elem[2] == '@':
                    self.char_loc = (i, j)
                    self.charxy = (self.bList[i][j][0][0] + 15, self.bList[i][j][0][1] + 5)
                if elem[2] == '_':
                    platform = Platform()
                    platform.rect.x, platform.rect.y = elem[0]
                    tl1.append(platform)
                if elem[2] == '^':
                    spike = Spike()
                    spike.rect.x, spike.rect.y = elem[0][0], elem[0][1] + 30
                    tl1.append(spike)
                if elem[2] == '<':
                    spike = Spike('right')
                    spike.rect.x, spike.rect.y = elem[0][0] + 30, elem[0][1]
                    tl1.append(spike)
                if elem[2] == '>':
                    spike = Spike('left')
                    spike.rect.x, spike.rect.y = elem[0]
                    tl1.append(spike)
                if elem[2] == 'V':
                    spike = Spike('top')
                    spike.rect.x, spike.rect.y = elem[0]
                    tl1.append(spike)
                if elem[2] == 'F':
                    self.mapEnd = EndFlag()
                    self.mapEnd.rect.x, self.mapEnd.rect.y = elem[0][0] + 5, elem[0][1]
                    tl1.append(self.mapEnd)
                if elem[2] == 'G':
                    goomba = Enemy()
                    goomba.rect.x, goomba.rect.y = elem[0]
                    goomba.rect.x += 20
                    goomba.rect.y += 20
                    tl1.append(goomba)
                    list_toUpdate.append(goomba)
            self.texture_list.append(tl1)
        Ground_Sprites.draw(screen)
        Special_Sprites.draw(screen)


# MARIO Code

class Mario(pygame.sprite.Sprite):
    mario = pygame.image.load('Data/mario.png')

    def __init__(self, board):
        super().__init__(Char_Sprite)
        self.camera_lock = False
        self.jcounter = 0  # Можно менять кол-во прыжков
        self.image = Mario.mario
        self.rect = self.image.get_rect()
        self.xvelocity = 0
        self.yvelocity = 0
        self.grounded = False
        self.board = board
        self.gcheck = GroundChkr()
        self.lcheck, self.rcheck = SideChkr(), SideChkr()
        self.rect.x, self.rect.y = board.charxy
        self.d = 0
        self.dead = False
        self.won = False

    def updater(self):
        global goingL
        global goingR
        global walkingX

        if pygame.sprite.spritecollideany(self, Ground_Sprites) and pygame.sprite.spritecollideany(self.gcheck,
                                                                                                   Ground_Sprites):
            self.rect.y -= 1
        if pygame.sprite.spritecollideany(self, Ground_Sprites) and pygame.sprite.spritecollideany(self.lcheck,
                                                                                                   Ground_Sprites):
            self.rect.x += 1
        if pygame.sprite.spritecollideany(self, Ground_Sprites) and pygame.sprite.spritecollideany(self.rcheck,
                                                                                                   Ground_Sprites):
            self.rect.x -= 1

        self.d += 1
        Char_Sprite.draw(screen)

        self.lcheck.rect.x = self.rect.x - 2
        self.lcheck.rect.y = self.rect.y + 10
        self.rcheck.rect.x = self.rect.x + 26
        self.rcheck.rect.y = self.rect.y + 10
        self.gcheck.rect.x = self.rect.x
        self.gcheck.rect.y = self.rect.y + 43

        if pygame.sprite.spritecollideany(self.gcheck, Ground_Sprites):
            self.grounded = True
        else:
            self.grounded = False
        if pygame.sprite.spritecollideany(self.lcheck, Ground_Sprites):
            goingL = False
            self.xvelocity = 0
        elif pygame.sprite.spritecollideany(self.rcheck, Ground_Sprites):
            goingR = False
            self.xvelocity = 0

        if pygame.sprite.spritecollideany(self.gcheck, Threat_Sprite):
            self.dead = True
        if pygame.sprite.spritecollideany(self.lcheck, Threat_Sprite):
            self.dead = True
        elif pygame.sprite.spritecollideany(self.rcheck, Threat_Sprite):
            self.dead = True

        if self.grounded:
            self.jcounter = 0  # Можно менять кол-во прыжков
            self.yvelocity = 0
        else:
            if self.d % 5 == 1:
                self.yvelocity -= gravity
        if goingR:
            self.move('r')
        elif goingL:
            self.move('l')

        if goingR or goingL:
            if not self.camera_lock:
                self.rect.x += self.xvelocity
            board.camera_checkpoint -= self.xvelocity
            board.end_camera_cp -= self.xvelocity
            self.rect.y -= self.yvelocity
        else:
            self.rect.y -= self.yvelocity

        if (board.end_camera_cp >= self.rect.x) and (self.rect.x >= board.camera_checkpoint):
            self.camera_lock = True
        else:
            self.camera_lock = False

        if self.rect.y > board.row * 50:
            self.dead = True

    def move(self, direction):
        if direction == 'r':
            self.xvelocity = 4
        if direction == 'l':
            self.xvelocity = -4

    def jump(self):
        self.rect.y -= 10
        if self.grounded:
            self.yvelocity = 7
        else:
            if self.jcounter > 0:
                self.yvelocity = 5
            self.jcounter -= 1


# OTHER SPRITES' Code


class Grass(pygame.sprite.Sprite):
    grass = pygame.image.load('Data/grass.png')

    def __init__(self):
        super().__init__(Ground_Sprites)
        self.image = Grass.grass
        self.rect = self.image.get_rect()


class Platform(pygame.sprite.Sprite):
    platform = pygame.image.load('Data/platform.png')

    def __init__(self):
        super().__init__(Ground_Sprites)
        self.image = Platform.platform
        self.rect = self.image.get_rect()


class GroundChkr(pygame.sprite.Sprite):
    gcheck = pygame.image.load('Data/groundChkr.png')

    def __init__(self, xsmaller=0):
        super().__init__(Collide_Sprite)
        self.image = pygame.transform.scale(GroundChkr.gcheck, (24 + xsmaller, 1))
        self.rect = self.image.get_rect()


class Spike(pygame.sprite.Sprite):
    spike = pygame.image.load('Data/spikes.png')

    def __init__(self, l='bottom'):
        super().__init__(Threat_Sprite)
        self.image = Spike.spike
        if l == 'right':
            self.image = pygame.transform.rotate(self.image, 90)
        elif l == 'left':
            self.image = pygame.transform.rotate(self.image, 270)
        elif l == 'top':
            self.image = pygame.transform.rotate(self.image, 180)
        elif l == 'bottom':
            pass
        self.rect = self.image.get_rect()


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        if walkingX:
            obj.rect.x -= self.dx

    def updater(self, target):
        if target.camera_lock:
            self.dx = target.xvelocity
        else:
            self.dx = 0


class SideChkr(pygame.sprite.Sprite):
    scheck = pygame.image.load('Data/sideChkr.png')

    def __init__(self, ysmaller=0):
        super().__init__(Collide_Sprite)
        self.image = pygame.transform.scale(SideChkr.scheck, (1, 20 + ysmaller))
        self.rect = self.image.get_rect()


class EndFlag(pygame.sprite.Sprite):
    flag = pygame.image.load('Data/end_flag.png')

    def __init__(self):
        super().__init__(Special_Sprites)
        self.image = EndFlag.flag
        self.rect = self.image.get_rect()

    def updater(self):
        if pygame.sprite.spritecollideany(self, Char_Sprite) or pygame.sprite.spritecollideany(self, Collide_Sprite):
            mario.won = True


class Enemy(pygame.sprite.Sprite):
    goomba = pygame.image.load('Data/enemy.png')

    def __init__(self):
        super().__init__(Threat_Sprite)
        self.image = Enemy.goomba
        self.rect = self.image.get_rect()
        self.gcheck = GroundChkr(6)
        self.lcheck, self.rcheck = SideChkr(-5), SideChkr(-5)
        self.grounded = False
        self.xVel = -1
        self.yVel = 0
        self.d = 0

    def updater(self):
        self.d += 1
        self.d = self.d % 100
        self.lcheck.rect.x = self.rect.x - 2
        self.lcheck.rect.y = self.rect.y + 7
        self.rcheck.rect.x = self.rect.x + 32
        self.rcheck.rect.y = self.rect.y + 7
        self.gcheck.rect.x = self.rect.x
        self.gcheck.rect.y = self.rect.y + 33

        if abs(self.rect.x - mario.rect.x) <= 1000:
            if pygame.sprite.spritecollideany(self, Ground_Sprites):
                self.grounded = True
                self.rect.y -= 1
            elif pygame.sprite.spritecollideany(self.gcheck, Ground_Sprites):
                self.grounded = True
            else:
                self.grounded = False

            if pygame.sprite.spritecollideany(self.lcheck, Ground_Sprites):
                self.xVel = 1
            elif pygame.sprite.spritecollideany(self.rcheck, Ground_Sprites):
                self.xVel = -1

            if not self.grounded:
                if self.d % 4 == 1:
                    self.yVel += gravity
            else:
                self.yVel = 0
            self.rect.x += self.xVel
            self.rect.y += self.yVel

            if pygame.sprite.spritecollideany(self, Char_Sprite) and (mario.yvelocity < 0):
                self.kill()
            elif pygame.sprite.spritecollideany(self.lcheck, Char_Sprite) and (mario.yvelocity < 0):
                self.kill()
            elif pygame.sprite.spritecollideany(self.rcheck, Char_Sprite) and (mario.yvelocity < 0):
                self.kill()



# MAIN Code


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Марио')
    screen = pygame.display.set_mode(size)
    screen.fill(sky_col)

    Ground_Sprites = pygame.sprite.Group()
    Char_Sprite = pygame.sprite.Group()
    Collide_Sprite = pygame.sprite.Group()
    Threat_Sprite = pygame.sprite.Group()
    Special_Sprites = pygame.sprite.Group()
    groupsList = [Ground_Sprites, Special_Sprites,
                  Threat_Sprite]

    UPDATER = pygame.USEREVENT + 1
    pygame.time.set_timer(UPDATER, 10)
    board = Board(11, 60)
    board.sort_map_text('Data/map1.txt')
    board.render_map()
    camera = Camera()
    mario = Mario(board)
    list_toUpdate.append(mario)
    list_toUpdate.append(board.mapEnd)

    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                walkingX = True
                if event.key == pygame.K_UP:
                    mario.jump()
            if event.type == UPDATER:
                for elem in list_toUpdate:
                    elem.updater()
                camera.updater(mario)
                for group in groupsList:
                    for sprite in group:
                        camera.apply(sprite)
        if keys[pygame.K_LEFT]:
            goingL = True
        else:
            goingL = False
        if keys[pygame.K_RIGHT]:
            goingR = True
        else:
            goingR = False

        if mario.dead:
            running = False
            print('You Died!')
        elif mario.won:
            running = False
            print('You Won!')

        walkingX = goingL or goingR
        screen.fill(sky_col)
        Ground_Sprites.draw(screen)
        Char_Sprite.draw(screen)
        Threat_Sprite.draw(screen)
        Special_Sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()
