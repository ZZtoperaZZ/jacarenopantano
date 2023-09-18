import pygame
import sys
import math
import random

# Inicializa o pygame
pygame.init()

# Configurações
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
VERDE_AZULADO = (30, 120, 120)
VERDE = (0, 255, 0)
MARROM = (139, 69, 19)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo do Pantano")
mapa = pygame.image.load("mapa_pantano.png")

# Carregando imagens dos barcos e jacarés
barcos = {
    "prata": pygame.image.load("barco_prata.png"),
    "azul": pygame.image.load("barco_azul.png"),
    "amarelo": pygame.image.load("barco_amarelo.png"),
    "vermelho": pygame.image.load("barco_vermelho.png"),
}
jacares_imgs = {
    "jacare_maior": pygame.image.load("jacare_maior.png"),
    "jacare_intermediario1": pygame.image.load("jacare_intermediario1.png"),
    "jacare_intermediario2": pygame.image.load("jacare_intermediario2.png"),
    "jacare_menor": pygame.image.load("jacare_menor.png"),
}

# Carregando as imagens dos power-ups
powerup_dano_img = pygame.image.load('powerup_dano.png')
powerup_velocidade_img = pygame.image.load('powerup_velocidade.png')
powerup_colete_img = pygame.image.load('powerup_colete.png')
powerup_regeneracao_img = pygame.image.load('powerup_regeneracao.png')

# Função para calcular ângulo entre dois pontos
def calcular_angulo_entre_pontos(x1, y1, x2, y2):
    return math.degrees(math.atan2(y2 - y1, x2 - x1))

# Classe Jacaré
class Jacare:
    def __init__(self, x1, y1, imagem):
        self.angulo = 180
        self.x = x1
        self.y = y1
        self.imagem = imagem

        if imagem == jacares_imgs["jacare_maior"]:
            self.velocidade = .5
            self.vida = 140
        elif imagem == jacares_imgs["jacare_intermediario2"]:
            self.velocidade = .7
            self.vida = 120
        elif imagem == jacares_imgs["jacare_intermediario1"]:
            self.velocidade = 1
            self.vida = 80
        elif imagem == jacares_imgs["jacare_menor"]:
            self.velocidade = 1.2
            self.vida = 40

    def perseguir(self, x_alvo, y_alvo):
        angulo2 = math.atan2(y_alvo - self.y, x_alvo - self.x)
        self.x += self.velocidade * math.cos(angulo2)
        self.y += self.velocidade * math.sin(angulo2)
        self.angulo = calcular_angulo_entre_pontos(self.x, self.y, x_alvo, y_alvo)
        return self

    def desenhar(self, x_offset, y_offset):
        rotated2 = pygame.transform.rotate(self.imagem, -self.angulo)
        new_rect2 = rotated2.get_rect(center=self.imagem.get_rect(topleft=(self.x, self.y)).center)
        screen.blit(rotated2, (new_rect2.topleft[0] - x_offset, new_rect2.topleft[1] - y_offset))

# Classe PowerUp
class PowerUp:
    def __init__(self, xq, yq, tipo):
        self.x = xq
        self.y = yq
        self.tipo = tipo
        if tipo == 'dano':
            self.imagem = powerup_dano_img
        elif tipo == 'velocidade':
            self.imagem = powerup_velocidade_img
        elif tipo == 'colete':
            self.imagem = powerup_colete_img
        elif tipo == 'regeneracao':
            self.imagem = powerup_regeneracao_img

    def desenhar(self, screen2):
        screen2.blit(self.imagem, (self.x, self.y))

    def coletado(self, jogador_x, jogador_y):
        distancia = math.hypot(self.x - jogador_x, self.y - jogador_y)
        if distancia < 50:  # Supondo que 50 é a distância de coleta
            return True
        return False
def gerar_powerup_aleatorio(x, y):
    tipos = ['dano', 'velocidade', 'colete', 'regeneracao']
    tipo = random.choice(tipos)
    # Ajuste a posição do power-up para que ele apareça mais próximo do barco
    x = min(max(x, posicao_mapa[0] + 50), posicao_mapa[0] + SCREEN_WIDTH - 50)
    y = min(max(y, posicao_mapa[1] + 50), posicao_mapa[1] + SCREEN_HEIGHT - 50)
    return PowerUp(x, y, tipo)


# Função para gerar jacaré aleatório
def gerar_jacare_aleatorio():
    # Probabilidades ajustadas para gerar diferentes tipos de jacarés
    tipos = ["jacare_menor"] * 50 + ["jacare_intermediario1"] * 30 + ["jacare_intermediario2"] * 15 + [
        "jacare_maior"] * 5
    tipo = random.choice(tipos)

    # Gere uma posição aleatória para o jacaré dentro de um espaço definido (por exemplo, 10000x10000)
    x2 = random.randint(0, 10000)
    y2 = random.randint(0, 10000)

    # Crie uma instância do jacaré com a imagem correspondente ao tipo escolhido
    jacareq = Jacare(x2, y2, jacares_imgs[tipo])

    return jacareq


# Função para desenhar barras de vida
def desenhar_barras_de_vida(jacares2, x_offset, y_offset):
    for jacare2 in jacares2:
        xr = jacare2.x - x_offset
        yr = jacare2.y - y_offset - 10  # Posicione a barra acima do jacaré
        largura_barra = 40  # Largura da barra de vida fixa
        altura_barra = 5  # Altura da barra de vida

        # Calcule a largura da barra com base na vida do jacaré
        vida_maxima = 140 if jacare2.imagem == jacares_imgs["jacare_maior"] else \
                      120 if jacare2.imagem == jacares_imgs["jacare_intermediario2"] else \
                      80 if jacare2.imagem == jacares_imgs["jacare_intermediario1"] else 40
        largura_atual = int((jacare2.vida / vida_maxima) * largura_barra)

        # Desenhe a barra de vida (por exemplo, verde para vida cheia, vermelho para vida baixa)
        pygame.draw.rect(screen, (255, 0, 0), (xr, yr, largura_barra, altura_barra))  # Barra vermelha
        pygame.draw.rect(screen, (0, 255, 0), (xr, yr, largura_atual, altura_barra))  # Barra verde


# Variáveis iniciais
posicao_barco = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
posicao_mapa = [5000 - SCREEN_WIDTH // 2, 5000 - SCREEN_HEIGHT // 2]
velocidade = 3
cor_atual = random.choice(list(barcos.keys()))
balas = []
angulo = 90
jacares = [gerar_jacare_aleatorio() for _ in range(20)]
vida_jogador = 100
RAIO_BALA = 10
DANO_BALA = 20
powerups = []


# Loop principal
running = True
while running:
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                dx = mx - posicao_barco[0]
                dy = my - posicao_barco[1]
                angulo_tiro = math.degrees(math.atan2(-dy, dx))
                bala = {
                    "pos": [posicao_barco[0], posicao_barco[1]],
                    "dir": [math.cos(math.radians(angulo_tiro)), -math.sin(math.radians(angulo_tiro))],
                    "distancia_percorrida": 0
                }
                balas.append(bala)

        # Ajuste de velocidade com base na cor abaixo do barco
        cor_abaixo_do_barco = mapa.get_at(
            (int(posicao_barco[0] + posicao_mapa[0]), int(posicao_barco[1] + posicao_mapa[1])))
        if cor_abaixo_do_barco == VERDE:
            velocidade_atual = 0.2
        elif cor_abaixo_do_barco == MARROM:
            velocidade_atual = velocidade / 2
        else:
            velocidade_atual = velocidade

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            angulo = 45
        elif keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            angulo = 315
        elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            angulo = 135
        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            angulo = 225
        elif keys[pygame.K_UP]:
            angulo = 0
        elif keys[pygame.K_DOWN]:
            angulo = 180
        elif keys[pygame.K_LEFT]:
            angulo = 270
        elif keys[pygame.K_RIGHT]:
            angulo = 90

        mover_mapa_x = mover_mapa_y = True

        # Movimento do mapa
        if keys[pygame.K_LEFT]:
            posicao_mapa[0] -= velocidade_atual
        if keys[pygame.K_RIGHT]:
            posicao_mapa[0] += velocidade_atual
        if keys[pygame.K_UP]:
            posicao_mapa[1] -= velocidade_atual
        if keys[pygame.K_DOWN]:
            posicao_mapa[1] += velocidade_atual

        # Garantir que o mapa não saia dos limites
        posicao_mapa[0] = max(0, min(posicao_mapa[0], 10000 - SCREEN_WIDTH))
        posicao_mapa[1] = max(0, min(posicao_mapa[1], 10000 - SCREEN_HEIGHT))

        # Desenhar o mapa e os objetos
        screen.blit(mapa, (-posicao_mapa[0], -posicao_mapa[1]))
        desenhar_barras_de_vida(jacares, posicao_mapa[0], posicao_mapa[1])




        for jacare in jacares:
            jacare.perseguir(posicao_barco[0] + posicao_mapa[0], posicao_barco[1] + posicao_mapa[1]).desenhar(
                posicao_mapa[0], posicao_mapa[1])

        for bala in balas[:]:
            bala["pos"][0] += bala["dir"][0] * 10
            bala["pos"][1] += bala["dir"][1] * 10
            bala["distancia_percorrida"] += 10
            pygame.draw.circle(screen, (0, 0, 0), (int(bala["pos"][0]), int(bala["pos"][1])), RAIO_BALA)

            for jacare in jacares[:]:  # Verifique a colisão de cada bala com cada jacaré
                dist_bala_jacare = math.hypot(jacare.x - bala["pos"][0] - posicao_mapa[0],
                                              jacare.y - bala["pos"][1] - posicao_mapa[1])
                if dist_bala_jacare < RAIO_BALA + 20:  # Supondo que 20 é metade do tamanho do jacaré
                    jacare.vida -= DANO_BALA  # Reduzir a vida do jacaré
                    balas.remove(bala)  # Remover a bala que atingiu o jacaré
                    break  # Sair do loop interno, já que a bala foi removida

            if bala["distancia_percorrida"] >= 190:
                if bala in balas:  # Verifique se a bala ainda está na lista antes de removê-la
                    balas.remove(bala)  # Remova a bala da lista

        for jacare in jacares[:]:  # Agora, verifique se o jacaré ainda está vivo
            if jacare.vida <= 0:
                jacares.remove(jacare)


        # Renderização
        screen.blit(mapa, (-posicao_mapa[0], -posicao_mapa[1]))
        desenhar_barras_de_vida(jacares, posicao_mapa[0], posicao_mapa[1])
        for jacare in jacares:
            jacare.perseguir(posicao_barco[0] + posicao_mapa[0], posicao_barco[1] + posicao_mapa[1]).desenhar(
                posicao_mapa[0], posicao_mapa[1])
        for jacare in jacares:
            jacare.perseguir(posicao_barco[0] + posicao_mapa[0], posicao_barco[1] + posicao_mapa[1]).desenhar(
                posicao_mapa[0], posicao_mapa[1])

            dist = math.hypot(jacare.x - (posicao_barco[0] + posicao_mapa[0]),
                              jacare.y - (posicao_barco[1] + posicao_mapa[1]))
            if dist < 50:  # Se o jacaré estiver perto do barco
                vida_jogador -= 10  # Reduz a vida do jogador
                jacares.remove(jacare)  # Remove o jacaré após o ataque
        for jacare in jacares[:]:
            # ... (restante do código para detecção de colisão e dano)

            if jacare.vida <= 0:
                jacares.remove(jacare)
                # Quando um jacaré é eliminado, um novo é gerado
                novo_jacare = gerar_jacare_aleatorio()
                jacares.append(novo_jacare)

                # Gera um power-up na posição do jacaré morto
                powerup = gerar_powerup_aleatorio(jacare.x, jacare.y)
                # Adicione o power-up a uma lista de power-ups ativos (você precisa criar essa lista)
                powerups.append(powerup)

        # Renderizar o barco
        rotated_barco = pygame.transform.rotate(barcos[cor_atual], -angulo)
        new_rect = rotated_barco.get_rect(
            center=barcos[cor_atual].get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)).center)
        screen.blit(rotated_barco, new_rect.topleft)
        # Renderizando os power-ups
        for powerup in powerups:
            powerup.desenhar(screen)

        # Renderizar balas
        for bala in balas:
            pygame.draw.circle(screen, (0, 0, 0), (int(bala["pos"][0]), int(bala["pos"][1])), RAIO_BALA)
        pygame.draw.rect(screen, (255, 0, 0), (10, 10, 200, 20))
        pygame.draw.rect(screen, (0, 255, 0), (10, 10, 2 * vida_jogador, 20))
        for powerup in powerups[:]:
            powerup.desenhar(screen)
            if powerup.coletado(posicao_barco[0] + posicao_mapa[0], posicao_barco[1] + posicao_mapa[1]):
                # Aqui, você pode adicionar a lógica para aplicar o efeito do power-up ao jogador
                # Por exemplo, se for um power-up de dano, aumente o dano das balas do jogador
                # Se for um power-up de vida, aumente a vida do jogador, etc.
                powerups.remove(powerup)

        # Atualizar a tela
        pygame.display.flip()

        # Limitar a taxa de quadros
        clock = pygame.time.Clock()
        clock.tick(90)

pygame.quit()
sys.exit()
