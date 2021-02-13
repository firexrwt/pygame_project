import pygame, math

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
nextMap = ''
nextMrows, nextMcols = 0, 0
won = 0
lastLev = False
level = 1
ticks = 0


# BOARD Code


class Board:
    def __init__(self, row, col):
        self.mapList = []
        self.texture_list = []
        self.bList = []
        self.row = row
        self.col = col
        self.char_loc = ()
        self.charxy = (0, 0)
        self.camera_checkpoint = 300
        self.end_camera_cp = self.col * 50 - 16 * 50

        self.lBorder = WorldBorder()
        self.rBorder = WorldBorder()

        for i in range(self.row):
            bListj = []
            for j in range(self.col):
                bListj.append((((j - 1) * 50, i * 50), (j * 50, 50 * (i + 1)), '.'))  # x0,y0;x,y;block
            self.bList.append(bListj)

    def sort_map_text(self, fileName):
        global nextMrows, nextMap, nextMcols, lastLev
        mapFile = [elem for num, elem in enumerate(open(fileName, 'r'))]

        for i in range(self.row):
            line = mapFile[i].rstrip('\n')
            self.mapList.append(line)
        if mapFile[self.row] == 'win':
            lastLev = True
        else:
            nextMap = mapFile[self.row].split(' ')[0]
            nextMrows = int(mapFile[self.row].split(' ')[1])
            nextMcols = int(mapFile[self.row].split(' ')[2])

        for i in range(self.row):
            for j in range(self.col):
                q = self.bList[i][j]
                self.bList[i][j] = (q[0], q[1], self.mapList[i][j])

    def render_map(self):
        global won
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
                    mapEnd = EndFlag()
                    mapEnd.rect.x, mapEnd.rect.y = elem[0][0] + 5, elem[0][1]
                    tl1.append(mapEnd)
                    print(1)
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

    def kill_all(self):
        for group in groupsList:
            for elem in group:
                elem.kill()


# MARIO Code

class Mario(pygame.sprite.Sprite):
    mario = pygame.image.load('Data/Sprites/mario_standing.png')
    mariow1 = pygame.image.load('Data/Sprites/mario_walking1.png')
    mariow2 = pygame.image.load('Data/Sprites/mario_walking2.png')
    mariow3 = pygame.image.load('Data/Sprites/mario_walking3.png')
    mariow1l = pygame.image.load('Data/Sprites/mario_walking1L.png')
    mariow2l = pygame.image.load('Data/Sprites/mario_walking2L.png')
    mariow3l = pygame.image.load('Data/Sprites/mario_walking3L.png')
    marioj = pygame.image.load('Data/Sprites/mario_jumping2.png')

    def __init__(self, parentboard):
        global won
        super().__init__(Char_Sprite)
        self.camera_lock = False
        self.killed = False
        self.jcounter = 0  # Можно менять кол-во прыжков
        self.image = Mario.mario
        self.rect = self.image.get_rect()
        self.xvelocity = 0
        self.yvelocity = 0
        self.grounded = False
        self.board = parentboard
        self.gcheck, self.upcheck = GroundChkr(), GroundChkr()
        self.lcheck, self.rcheck = SideChkr(), SideChkr()
        self.rect.x, self.rect.y = board.charxy
        self.d = 0
        self.dead = False
        self.won = False
        self.facingR = True
        self.f = 1

    def updater(self):
        global goingL
        global goingR
        global walkingX
        global won

        board.lBorder.rect.x = -50
        board.rBorder.rect.x = 1005

        if pygame.sprite.spritecollideany(self, Ground_Sprites) and pygame.sprite.spritecollideany(self.gcheck,
                                                                                                   Ground_Sprites):
            self.rect.y -= 1
        if pygame.sprite.spritecollideany(self, Ground_Sprites) and pygame.sprite.spritecollideany(self.lcheck,
                                                                                                   Ground_Sprites):
            self.rect.x += 1
        if pygame.sprite.spritecollideany(self, Ground_Sprites) and pygame.sprite.spritecollideany(self.rcheck,
                                                                                                   Ground_Sprites):
            self.rect.x -= 1
        if pygame.sprite.spritecollideany(self, Ground_Sprites) and pygame.sprite.spritecollideany(self.upcheck,
                                                                                                   Ground_Sprites):
            self.rect.y += 1

        self.d += 1
        Char_Sprite.draw(screen)

        if self.d == 30:
            won = 0

        if not self.killed:
            self.lcheck.rect.x = self.rect.x - 2
            self.lcheck.rect.y = self.rect.y + 10
            self.rcheck.rect.x = self.rect.x + 26
            self.rcheck.rect.y = self.rect.y + 10
            self.gcheck.rect.x = self.rect.x
            self.gcheck.rect.y = self.rect.y + 43
            self.upcheck.rect.x = self.rect.x
            self.upcheck.rect.y = self.rect.y - 3

        if pygame.sprite.spritecollideany(self.gcheck, Ground_Sprites):
            self.grounded = True
        else:
            self.grounded = False
        if pygame.sprite.spritecollideany(self.lcheck, Ground_Sprites):
            goingL = False
            self.xvelocity = 0
        if pygame.sprite.spritecollideany(self.rcheck, Ground_Sprites):
            goingR = False
            self.xvelocity = 0
        if pygame.sprite.spritecollideany(self.upcheck, Ground_Sprites):
            try:
                name = pygame.sprite.spritecollideany(self.upcheck, Ground_Sprites).name
                if name != 'platform':
                    self.yvelocity = max(min(self.yvelocity, 0), -100000000000)
            except Exception:
                self.yvelocity = max(min(self.yvelocity, 0), -100000000000)

        if pygame.sprite.spritecollideany(self.gcheck, Special_Sprites):
            try:
                name = pygame.sprite.spritecollideany(self.lcheck, Special_Sprites).name
                if name == 'end flag':
                    self.won = True
            except Exception:
                pass
        if pygame.sprite.spritecollideany(self.lcheck, Special_Sprites):
            try:
                name = pygame.sprite.spritecollideany(self.lcheck, Special_Sprites).name
                if name == 'end flag':
                    self.won = True
            except Exception:
                pass
        if pygame.sprite.spritecollideany(self.rcheck, Ground_Sprites):
            try:
                name = pygame.sprite.spritecollideany(self.lcheck, Special_Sprites).name
                if name == 'end flag':
                    self.won = True
            except Exception:
                pass
        if pygame.sprite.spritecollideany(self.upcheck, Special_Sprites):
            try:
                name = pygame.sprite.spritecollideany(self.lcheck, Special_Sprites).name
                if name == 'end flag':
                    self.won = True
            except Exception:
                pass

        if pygame.sprite.spritecollideany(self.gcheck, Threat_Sprite):
            try:
                name = pygame.sprite.spritecollideany(self.gcheck, Threat_Sprite).name
                if name == 'goomba':
                    if self.yvelocity < 0:
                        pygame.sprite.spritecollideany(self.gcheck, Threat_Sprite).kill()
            except Exception:
                self.dead = True
        if pygame.sprite.spritecollideany(self.upcheck, Threat_Sprite):
            self.dead = True
        if pygame.sprite.spritecollideany(self.lcheck, Threat_Sprite):
            try:
                name = pygame.sprite.spritecollideany(self.gcheck, Threat_Sprite).name
                if name == 'goomba':
                    if self.yvelocity < 0:
                        pygame.sprite.spritecollideany(self.gcheck, Threat_Sprite).kill()
            except Exception:
                self.dead = True
        if pygame.sprite.spritecollideany(self.rcheck, Threat_Sprite):
            try:
                name = pygame.sprite.spritecollideany(self.gcheck, Threat_Sprite).name
                if name == 'goomba':
                    if self.yvelocity < 0:
                        pygame.sprite.spritecollideany(self.gcheck, Threat_Sprite).kill()
            except Exception:
                self.dead = True

        if self.grounded:
            self.jcounter = 0  # Можно менять кол-во прыжков
            self.yvelocity = 0
        else:
            if self.d % 5 == 1:
                self.yvelocity -= gravity

        if goingR:
            self.move('r')
            self.facingR = True
            if self.grounded:
                if self.d % 12 in [0, 1, 2, 3]:
                    self.image = Mario.mariow1
                elif self.d % 12 in [4, 5, 6, 7]:
                    self.image = Mario.mariow2
                elif self.d % 12 in [8, 9, 10, 11]:
                    self.image = Mario.mariow3
            else:
                self.image = Mario.marioj
        elif goingL:
            self.move('l')
            self.facingR = False
            if self.grounded:
                if self.d % 12 in [0, 1, 2, 3]:
                    self.image = Mario.mariow1l
                elif self.d % 12 in [4, 5, 6, 7]:
                    self.image = Mario.mariow2l
                elif self.d % 12 in [8, 9, 10, 11]:
                    self.image = Mario.mariow3l
            else:
                self.image = pygame.transform.flip(Mario.marioj, True, False)
        else:
            if self.facingR:
                if self.grounded:
                    self.image = Mario.mario
                else:
                    self.image = Mario.marioj
            else:
                if self.grounded:
                    self.image = pygame.transform.flip(Mario.mario, True, False)
                else:
                    self.image = pygame.transform.flip(Mario.marioj, True, False)

        if walkingX:
            if not self.camera_lock:
                self.rect.x += self.xvelocity
            self.rect.y -= self.yvelocity
        else:
            self.rect.y -= self.yvelocity

        if (board.texture_list[0][-1].rect.x >= 1005) and (self.rect.x >= 300):
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
            jump.play()
        else:
            if self.jcounter > 0:
                self.yvelocity = 5
            self.jcounter -= 1

    def kill_ch(self):
        self.killed = True
        self.gcheck.rect.y -= 1000000000
        self.lcheck.rect.y -= 1000000000
        self.upcheck.rect.y -= 1000000000
        self.rcheck.rect.y -= 1000000000


# OTHER SPRITES' Code


class WorldBorder(pygame.sprite.Sprite):
    border = pygame.image.load('Data/world_borders.png')

    def __init__(self):
        super().__init__(Ground_Sprites)
        self.image = WorldBorder.border
        self.rect = self.image.get_rect()


class Grass(pygame.sprite.Sprite):
    grass = pygame.image.load('Data/grass.png')

    def __init__(self):
        super().__init__(Ground_Sprites)
        self.image = Grass.grass
        self.rect = self.image.get_rect()
        self.name = 'grass'


class Platform(pygame.sprite.Sprite):
    platform = pygame.image.load('Data/platform.png')

    def __init__(self):
        super().__init__(Ground_Sprites)
        self.image = Platform.platform
        self.rect = self.image.get_rect()
        self.name = 'platform'


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
        self.name = 'spike'
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
        self.name = 'end flag'


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
        self.name = 'goomba'

    def updater(self):

        self.d += 1
        self.d = self.d % 100
        self.lcheck.rect.x = self.rect.x - 2
        self.lcheck.rect.y = self.rect.y + 7
        self.rcheck.rect.x = self.rect.x + 32
        self.rcheck.rect.y = self.rect.y + 7
        self.gcheck.rect.x = self.rect.x
        self.gcheck.rect.y = self.rect.y + 33

        if abs(self.rect.x - mario.rect.x) <= 1600:
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

            if mario.d % 50 == 0:
                self.image = Enemy.goomba
            elif mario.d % 50 == 24:
                self.image = pygame.transform.flip(self.image, True, False)

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
    pygame.mixer.music.load('Data/Mario Theme.wav')
    jump = pygame.mixer.Sound('Data/Jump_sound.mp3')
    pygame.mixer.music.set_volume(0.05)
    jump.set_volume(0.05)
    pygame.mixer.music.play(-1)
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
    board.sort_map_text('Data/maps/map1.txt')
    board.render_map()
    camera = Camera()
    mario = Mario(board)
    list_toUpdate.append(mario)

    while running:
        ticks += 1
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
            if won == 0:
                if not lastLev:
                    won += 1
                    mario.kill()
                    mario.kill_ch()
                    board.kill_all()
                    board = Board(nextMrows, nextMcols)
                    board.sort_map_text(f'Data/maps/{nextMap}')
                    board.render_map()
                    mario = Mario(board)
                    list_toUpdate.append(mario)
                    mario.rect.x, mario.rect.y = board.charxy
                    level += 1
                else:
                    running = False
                    print('You Win!')

        walkingX = goingL or goingR
        if goingL and goingR:
            goingL = False
            goingR = True
        screen.fill(sky_col)
        Char_Sprite.draw(screen)
        for group in groupsList:
            group.draw(screen)
        pygame.display.flip()

    pygame.quit()
