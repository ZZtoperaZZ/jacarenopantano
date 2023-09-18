import pygame

# Inicializa o pygame
pygame.init()

def create_dano_powerup():
    # Espada ou estrela pontiaguda
    powerup = pygame.Surface((30, 30), pygame.SRCALPHA)
    powerup.fill((0, 0, 0, 0))
    pygame.draw.polygon(powerup, (255, 165, 0), [(15, 0), (15, 30), (30, 15), (0, 15)])  # Laranja
    return powerup

def create_velocidade_powerup():
    # Raio
    powerup = pygame.Surface((30, 30), pygame.SRCALPHA)
    powerup.fill((0, 0, 0, 0))
    pygame.draw.polygon(powerup, (255, 255, 0), [(15, 0), (30, 15), (15, 10), (0, 15)])  # Amarelo
    return powerup

def create_colete_powerup():
    # Escudo
    powerup = pygame.Surface((30, 30), pygame.SRCALPHA)
    powerup.fill((0, 0, 0, 0))
    pygame.draw.arc(powerup, (0, 0, 255), (5, 7, 20, 23), 0, 3.14, 10)  # Azul
    return powerup

def create_regeneracao_powerup():
    # Cruz
    powerup = pygame.Surface((30, 30), pygame.SRCALPHA)
    powerup.fill((0, 0, 0, 0))
    pygame.draw.rect(powerup, (255, 0, 0), (13, 5, 4, 20))  # Vermelho
    pygame.draw.rect(powerup, (255, 0, 0), (5, 13, 20, 4))  # Vermelho
    return powerup

# Criar e salvar as imagens
powerup_functions = {
    "dano": create_dano_powerup,
    "velocidade": create_velocidade_powerup,
    "colete": create_colete_powerup,
    "regeneracao": create_regeneracao_powerup
}

for powerup_name, func in powerup_functions.items():
    powerup_image = func()
    pygame.image.save(powerup_image, f"powerup_{powerup_name}.png")

pygame.quit()

print('Imagens de powerups criadas com sucesso!')
