import pygame

# Inicializa o pygame
pygame.init()

# Definições de tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Teste PowerUp')

# Carregando imagens
cenario = pygame.image.load('mapa_pantano.png')
barco = pygame.image.load('barco_amarelo.png')
powerup_dano_img = pygame.image.load('powerup_dano.png')

# Posições
posicao_barco = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Loop principal
correr = True
while correr:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            correr = False

    # Renderização
    screen.blit(cenario, (0, 0))
    screen.blit(barco, posicao_barco)
    screen.blit(powerup_dano_img, posicao_barco)

    pygame.display.flip()

pygame.quit()