import pygame, random
from pygame.locals import *
from time import sleep

# variáveis que não vao alterar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SPEED = 8
GRAVITY = 0.8
GAME_SPEED = 9

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 120


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('FlappyBird_wingUp.png').convert_alpha(),
                       pygame.image.load('FlappyBird_wingMid.png').convert_alpha(),
                       pygame.image.load('FlappyBird_wingDown.png').convert_alpha()]

        self.speed = SPEED

        self.current_image = 0

        self.image = pygame.image.load('FlappyBird_wingUp.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

        self.rect[0] = SCREEN_WIDTH / 2  # posição X que o passarinho começa
        self.rect[1] = SCREEN_HEIGHT / 2  # posição Y que o passarinho começa

    def update(self):
        self.current_image = (self.current_image + 1) % 3  # faz um ciclo entre as 3 imagens
        self.image = self.images[self.current_image]
        self.rect[1] += self.speed  # faz o passarinho cair
        self.speed += GRAVITY

    def bump(self):  # faz o passarinho pular
        self.speed = -SPEED


class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('pipe.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))  # alterar o tamanho da pipe

        self.rect = self.image.get_rect()
        self.rect[0] = xpos  # as pipes só vao aparecer em posiçoes X

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)  # False para girar o X e True para girar o Y
            self.rect[1] = -(self.rect[3] - ysize)  # esconde um pedaço do cano, pra colocar o tamanho que a gente quer
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize  # tela inteira - um certo tamanho y = tamanho do cano
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED


class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect[0] -= GAME_SPEED


def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])  # vai dizer se um sprite qualquer está fora da tela


def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return (pipe, pipe_inverted)


def start_the_game():
    menu = True
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    BACKGROUND = pygame.image.load('background.png')
    BACKGROUND = pygame.transform.scale(BACKGROUND, (
    SCREEN_WIDTH, SCREEN_HEIGHT))  # transforma a imagem "background" pro mesmo tamanho da tela

    bird_group = pygame.sprite.Group()
    bird = Bird()
    bird_group.add(bird)

    ground_group = pygame.sprite.Group()
    for i in range(2):
        ground = Ground(2 * SCREEN_WIDTH * i)
        ground_group.add(ground)

    pipe_group = pygame.sprite.Group()
    for i in range(2):
        pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    clock = pygame.time.Clock()  # FPS do jogo

    while True:  # o que mantém o jogo rodando
        fonte_coord = pygame.font.SysFont(pygame.font.get_default_font(), 100)
        fonte_coord2 = pygame.font.SysFont(pygame.font.get_default_font(), 50)
        # menu
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and menu == True:
                if event.button == 1:
                    screen.blit(BACKGROUND, (0, 0))
                    ground_group.draw(screen)
                    pygame.display.update()
                    sleep(0.3)
                    screen.blit(fonte_coord.render('3', True, (255, 255, 255)), (400, 250))
                    pygame.display.update()
                    sleep(1)
                    screen.blit(BACKGROUND, (0, 0))
                    ground_group.draw(screen)
                    pygame.display.update()
                    screen.blit(fonte_coord.render('2', True, (255, 255, 255)), (400, 250))
                    pygame.display.update()
                    sleep(1)
                    screen.blit(BACKGROUND, (0, 0))
                    ground_group.draw(screen)
                    pygame.display.update()
                    screen.blit(fonte_coord.render('1', True, (255, 255, 255)), (400, 250))
                    pygame.display.update()
                    sleep(1)
                    screen.blit(BACKGROUND, (0, 0))
                    ground_group.draw(screen)
                    pygame.display.update()
                    menu = False

            if event.type == KEYDOWN and menu == False:
                if event.key == K_SPACE:
                    bird.bump()

        clock.tick(30)
        screen.blit(BACKGROUND,
                    (0, 0))  # pega a superfície do plano de fundo e desenha na tela a partir da posiçao (x,y)

        if menu == True:
            ground_group.draw(screen)
            screen.blit(fonte_coord2.render('APERTE PARA COMEÇAR', True, (255, 255, 255)), (200, 250))
            pygame.display.update()
        if menu == False:
            if is_off_screen(ground_group.sprites()[0]):
                ground_group.remove(ground_group.sprites()[0])
                new_ground = Ground(GROUND_WIDTH - 20)
                ground_group.add(new_ground)

            if is_off_screen(pipe_group.sprites()[0]):
                pipe_group.remove(pipe_group.sprites()[0])  # remove o cano, pois está fora da tela
                pipe_group.remove(pipe_group.sprites()[
                                      0])  # depois de remover o primeiro, o invertido passa a ser o 0. Por isso duas linhas iguais

                pipes = get_random_pipes(SCREEN_WIDTH * 2)

                pipe_group.add(pipes[0])
                pipe_group.add(pipes[1])

            bird_group.update()
            ground_group.update()
            pipe_group.update()

            bird_group.draw(screen)
            ground_group.draw(screen)
            pipe_group.draw(screen)

            pygame.display.update()
            fonte_coord = pygame.font.SysFont(pygame.font.get_default_font(), 100)
            if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
                    pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
                screen.blit(fonte_coord.render('Game Over', True, (255, 255, 255)), (220, 250))
                pygame.display.update()
                sleep(3)
                # o mask faz com que só os pixels que tem alguma cor do pássaro colidem com os pixels do chão ou do cano
                # se eu quisesse matar um grupo depois da colisão, colocaria algum "group", mas já que não quero, coloquei False
                # caso um grupo colide com outro, termina o programa (break)
                break


start_the_game()