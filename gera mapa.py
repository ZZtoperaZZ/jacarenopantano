import pygame
import random

# Inicializa o pygame
pygame.init()

# Tamanho do mapa
MAP_WIDTH, MAP_HEIGHT = 10000, 10000

# Tamanho da janela
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600

# Cores
VERDE_AZULADO = (30, 120, 120)
VERDE = (0, 255, 0)
MARROM = (139, 69, 19)  # Cor para representar a lama

# Criando a imagem do mapa
mapa = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
mapa.fill(VERDE_AZULADO)

# Adicionando áreas marrons (lama) - menos numerosas, mas maiores
for _ in range(150):
    width = random.randint(300, 800)
    height = random.randint(300, 800)
    x = random.randint(0, MAP_WIDTH - width)
    y = random.randint(0, MAP_HEIGHT - height)
    pygame.draw.ellipse(mapa, MARROM, (x, y, width, height))

# Adicionando áreas verdes (floresta) por cima das áreas marrons
for _ in range(1500):  # Reduzindo para 1500 áreas verdes
    width = random.randint(60, 150)
    height = random.randint(60, 150)
    x = random.randint(0, MAP_WIDTH - width)
    y = random.randint(0, MAP_HEIGHT - height)
    shape_type = random.choice(["ellipse", "rectangle", "circle"])

    if shape_type == "ellipse":
        pygame.draw.ellipse(mapa, VERDE, (x, y, width, height))
    elif shape_type == "rectangle":
        pygame.draw.rect(mapa, VERDE, (x, y, width, height))
    elif shape_type == "circle":
        pygame.draw.circle(mapa, VERDE, (x + width // 2, y + height // 2), width // 2)

# Configuração da janela
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Jogo do Pantano")

# Coordenadas iniciais para deslocar o mapa (centralizado)
x, y = -4600, -4600

# Dimensões da imagem
dimensions = (10000, 10000)

# Criar uma superfície com canal alfa (transparência)
canvas = pygame.Surface(dimensions, pygame.SRCALPHA)

# Preencher a superfície com verde floresta
canvas.fill((34, 139, 34))

# Desenhar o quadrado interno transparente
pygame.draw.rect(canvas, (0, 0, 0, 0), (400, 300, 9200, 9400))

# Adicionar texto
font = pygame.font.SysFont('arialblack', 400)
text_bottom = font.render('Mecânica da zueira', True, (0, 0, 0))
text_top = font.render('TianoGamer', True, (0, 0, 0))
canvas.blit(text_top, (5000 - text_top.get_width() // 2,-140))
canvas.blit(text_bottom, (5000 - text_bottom.get_width() // 2, 9550))


def save_map(surface, overlay):
    combined_surface = surface.copy()
    combined_surface.blit(overlay, (0, 0))
    pygame.image.save(combined_surface, "mapa_pantano.png")
    print("Mapa salvo!")


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_map(mapa, canvas)

    # Atualiza a posição do mapa com base nas teclas pressionadas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        y += 5
    if keys[pygame.K_DOWN]:
        y -= 5
    if keys[pygame.K_LEFT]:
        x += 5
    if keys[pygame.K_RIGHT]:
        x -= 5

    screen.blit(mapa, (x, y))
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
