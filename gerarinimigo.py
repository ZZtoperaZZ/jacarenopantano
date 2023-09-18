import pygame

pygame.init()

def create_alligator_top_view():
    # Cria uma superfície transparente
    alligator = pygame.Surface((60, 20), pygame.SRCALPHA)
    alligator.fill((0, 0, 0, 0))  # Preenche com cor transparente

    # Corpo principal do jacaré (em verde escuro)
    pygame.draw.ellipse(alligator, (0, 100, 0), (5, 2, 50, 16))

    # Linha preta no meio do jacaré
    pygame.draw.line(alligator, (0, 0, 0), (5, 10), (55, 10), 1)

    # Cabeça (uma parte mais arredondada na frente)
    pygame.draw.ellipse(alligator, (0, 100, 0), (0, 4, 20, 12))

    # Olhos (pontos brancos para representar os olhos)
    pygame.draw.circle(alligator, (255, 255, 255), (10, 6), 2)
    pygame.draw.circle(alligator, (255, 255, 255), (10, 14), 2)

    # Narinas (pequenos círculos pretos na cabeça)
    pygame.draw.circle(alligator, (0, 0, 0), (5, 6), 1)
    pygame.draw.circle(alligator, (0, 0, 0), (5, 14), 1)

    # Cauda (uma parte mais fina e longa no final do corpo)
    pygame.draw.line(alligator, (0, 100, 0), (55, 10), (80, 10), 4)
    pygame.draw.line(alligator, (0, 100, 0), (80, 10), (90, 15), 2)
    pygame.draw.line(alligator, (0, 100, 0), (80, 10), (90, 5), 2)

    return alligator
# Salvar imagem do jacaré original
alligator_image = create_alligator_top_view()
# Tamanhos
sizes = [(90, 45), (70, 35), (60, 30), (50, 20)]
names = ["jacare_maior", "jacare_intermediario1", "jacare_intermediario2", "jacare_menor"]

for size, name in zip(sizes, names):
    resized_alligator = pygame.transform.scale(alligator_image, size)
    pygame.image.save(resized_alligator, f"{name}.png")

pygame.quit()
