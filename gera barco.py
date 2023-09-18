import pygame

pygame.init()

def create_boat_top_view(boat_color):
    # Cria uma superfície transparente
    boat = pygame.Surface((12, 20), pygame.SRCALPHA)
    boat.fill((0, 0, 0, 0))  # Preenche com cor transparente

    # Corpo principal do barco
    pygame.draw.ellipse(boat, boat_color, (1, 5, 10, 15))

    # Borda do barco em preto
    pygame.draw.ellipse(boat, (0, 0, 0), (1, 5, 10, 15), 1)  # Borda externa

    # Cabine (ponto preto para representar a pessoa)
    pygame.draw.circle(boat, (0, 0, 0), (6, 10), 1)

    # Motor (parte branca atrás)
    pygame.draw.rect(boat, (255, 255, 255), (5, 15, 2, 5))

    # Quadrado na ponta oposta ao motor
    pygame.draw.rect(boat, boat_color, (5, 3, 2, 2))

    # Agora, vamos dobrar o tamanho do barco
    boat = pygame.transform.scale(boat, (42, 80))

    return boat

colors = {
    "prata": (192, 192, 192),
    "azul": (0, 0, 255),
    "amarelo": (255, 255, 0),
    "vermelho": (255, 0, 0)
}

for color_name, color_value in colors.items():
    boat_image = create_boat_top_view(color_value)
    pygame.image.save(boat_image, f"barco_{color_name}.png")

pygame.quit()
