# Documentacao do Jogo - BASED

## Visao Geral
Jogo educativo sobre alimentacao saudavel com 4 fases diferentes.

---

## ARQUIVOS PRINCIPAIS

### 1. item.py - Sistema de Itens

```python
class Item(pygame.sprite.Sprite):
```
**O que faz:** Representa todos os itens coletaveis e obstaculos do jogo.

**Dicionario ITEMS:**
- `hamburguer`, `refrigerante`, `sorvete` = Comidas ruins (effect > 0)
- `maca`, `alface`, `banana` = Comidas boas (effect < 0)
- `pedra`, `cacto` = Obstaculos mortais (effect = 0)

**Metodos importantes:**
- `__init__()` - Cria o item, carrega imagem ou desenha placeholder
- `_draw_rock()` - Desenha pedra cinza com pygame.draw.polygon
- `_draw_cactus()` - Desenha cacto verde com pygame.draw.rect
- `is_good_item()` - Retorna True se gravity_effect < 0
- `update()` - Faz o item flutuar (movimento senoidal)

---

### 2. player.py - Jogador

```python
class Player(pygame.sprite.Sprite):
```
**O que faz:** Controla o personagem principal.

**Atributos principais:**
- `direction` - pygame.math.Vector2 para movimento
- `speed` - Velocidade de movimento
- `gravity` - Forca da gravidade
- `on_ground` - Se esta no chao (pode pular)
- `good_items_collected` / `bad_items_collected` - Contadores

**Metodos:**
- `update()` - Atualiza animacao
- `apply_gravity()` - Aplica gravidade (direction.y += gravity)
- `jump()` - Pula (direction.y = -jump_speed)
- `collect_item()` - Coleta item e atualiza contadores

---

### 3. level.py - Fase 1 (Runner)

```python
class Level:
```
**O que faz:** Fase estilo endless runner.

**Constantes:**
```python
SCREEN_WIDTH = 600
TILE_SIZE = SCREEN_WIDTH // 25  # = 24 pixels
SCREEN_HEIGHT = 28 * TILE_SIZE  # = 672 pixels
```

**Sistema de Scroll:**
```python
self.scroll_speed = 3  # Velocidade inicial
# No update():
tile.rect.x -= self.scroll_speed + 4  # Move tiles
obstacle.rect.x -= self.scroll_speed + 4  # Move obstaculos
```

**Sistema de Dificuldade:**
```python
# A cada 5 segundos (300 frames):
self.scroll_speed = min(self.scroll_speed + 0.5, 15)  # Aumenta velocidade
base_interval = max(30, 90 - int(self.scroll_speed * 5))  # Mais obstaculos
```

**Spawn de Obstaculos:**
```python
def spawn_obstacle(self):
    # Tipos: pedra, cacto, hamburguer, refrigerante, sorvete
    # Pedra/cacto = 2.5x tamanho, is_deadly = True (game over)
    # Comidas ruins = 1.5x tamanho, is_deadly = False
```

**Spawn de Comidas Boas:**
```python
def spawn_ground_good_item(self, count=1):
    # Aparece a cada 7 obstaculos
    # Posicao: no ar (y = floor - 3~5 tiles)
    # Jogador precisa pular para pegar
```

**Condicoes de Vitoria/Derrota:**
- Vitoria: `good_items_collected >= 9`
- Derrota: Tocar em pedra/cacto (game over imediato)

---

### 4. level2.py - Fase 2 (Agua)

```python
class WaterLevel:
```
**O que faz:** Fase aquatica com tubaroes.

**Movimento do Jogador:**
```python
# Movimento livre em todas direcoes
if keys[pygame.K_UP]: player.rect.y -= swim_speed
if keys[pygame.K_DOWN]: player.rect.y += swim_speed
if keys[pygame.K_LEFT]: player.rect.x -= swim_speed
if keys[pygame.K_RIGHT]: player.rect.x += swim_speed
```

**Classe Shark:**
```python
class Shark(pygame.sprite.Sprite):
    # Move horizontalmente
    # Inverte direcao ao sair da tela
    # Colisao = game over
```

**Spawn de Itens:**
```python
def spawn_item(self):
    # Itens caem do topo (y aumenta)
    size = (int(TILE_SIZE * 1.8), int(TILE_SIZE * 1.8))  # 1.8x maior
```

---

### 5. level3.py - Fase 3 (Labirinto)

```python
class Level3:
```
**O que faz:** Labirinto com canhoes que atiram comida ruim.

**Layout do Mapa:**
```python
self.layout = [
    "XXXXXXXXX          XXXXXX",
    "X   X   X     X   X     X",
    # X = parede, espaco = passagem, P = spawn do jogador
]
```

**Sistema de Canhoes:**
```python
def place_cannons(self):
    # 29 canhoes posicionados
    # direction: 1 = direita, -1 = esquerda
    cannon_size = (int(TILE_SIZE * 1.5), int(TILE_SIZE * 1.5))

def shoot_from_cannons(self):
    # A cada 1.5 segundos, canhao aleatorio atira
    # Projetil = comida ruim (hamburguer, refrigerante, sorvete)
```

**Condicao de Vitoria:**
- Sair pelo topo do mapa (`player.rect.bottom < 0`)

---

### 6. level4.py - Fase 4 (Boss)

```python
class BossLevel:
```
**O que faz:** Batalha contra o Boss.

**Classe Boss:**
```python
class Boss(pygame.sprite.Sprite):
    self.health = 1800
    self.speed_x = 3  # Normal
    self.speed_y = 2

    def activate_rage_mode(self):
        self.speed_x = 7  # 2x mais rapido
        self.speed_y = 6
        self.shoot_interval = 800  # Atira mais rapido
```

**Sistema de Laser:**
```python
class Laser(pygame.sprite.Sprite):
    # Jogador atira com tecla F
    # Dano normal: 20, Dano forte: 40
```

**Sistema de Cutscene:**
```python
class Cutscene:
    # Exibe dialogos na tela
    # Avanca com qualquer tecla/clique

# Cutscenes:
# 1. Inicio da fase (apresentacao)
# 2. Rage mode ("Eu vou vencer!")
```

**PowerUps:**
```python
class PowerUp:
    # Boss dropa a cada 4 danos
    # Efeito: armadura (2 hits) + laser forte por 8 segundos
```

---

## CONCEITOS PYGAME USADOS

### Sprites e Groups
```python
# Sprite = objeto visual com image e rect
class Item(pygame.sprite.Sprite):
    self.image = pygame.Surface(size)  # Visual
    self.rect = self.image.get_rect()  # Posicao/colisao

# Group = colecao de sprites
self.items = pygame.sprite.Group()
self.items.add(item)  # Adiciona
self.items.draw(screen)  # Desenha todos
self.items.update()  # Atualiza todos
```

### Colisoes
```python
# Sprite vs Group (remove ao colidir)
pygame.sprite.spritecollide(player, items, True)

# Sprite vs Group (so detecta)
pygame.sprite.spritecollideany(player, sharks)

# Rect vs Rect
player.rect.colliderect(tile.rect)
```

### Desenho
```python
# Formas basicas
pygame.draw.rect(surface, cor, rect)
pygame.draw.circle(surface, cor, centro, raio)
pygame.draw.polygon(surface, cor, pontos)
pygame.draw.line(surface, cor, inicio, fim, espessura)

# Texto
font = pygame.font.Font(None, 36)
text = font.render("Texto", True, (255,255,255))
screen.blit(text, (x, y))
```

### Teclas
```python
keys = pygame.key.get_pressed()
if keys[pygame.K_LEFT]:   # Seta esquerda
if keys[pygame.K_RIGHT]:  # Seta direita
if keys[pygame.K_UP]:     # Seta cima
if keys[pygame.K_SPACE]:  # Espaco (pular)
if keys[pygame.K_f]:      # F (atirar)
```

### Audio
```python
pygame.mixer.music.load("arquivo.mp3")
pygame.mixer.music.play(-1)  # -1 = loop infinito
pygame.mixer.music.stop()

# Efeitos sonoros
sound = pygame.mixer.Sound("efeito.mp3")
sound.play()
```

---

## FUNCOES PYTHON IMPORTANTES

### random
```python
random.choice(lista)  # Escolhe item aleatorio
random.randint(min, max)  # Numero inteiro aleatorio
random.uniform(min, max)  # Numero decimal aleatorio
random.shuffle(lista)  # Embaralha lista
```

### math
```python
math.cos(angulo)  # Cosseno (movimento circular)
math.sin(angulo)  # Seno
math.pi  # 3.14159...
```

### getattr
```python
# Pega atributo ou valor padrao se nao existir
self.difficulty_timer = getattr(self, 'difficulty_timer', 0) + 1
```

### hasattr
```python
# Verifica se atributo existe
if hasattr(item, 'is_falling') and item.is_falling:
```

---

## ESTRUTURA DE ARQUIVOS

```
jog/
├── main.py          # Loop principal do jogo
├── player.py        # Classe do jogador
├── item.py          # Itens e obstaculos
├── level.py         # Fase 1 (Runner)
├── level2.py        # Fase 2 (Agua)
├── level3.py        # Fase 3 (Labirinto)
├── level4.py        # Fase 4 (Boss)
├── assets/
│   ├── player/      # Sprites do jogador
│   ├── item/        # Sprites dos itens
│   ├── tiles/       # Tiles do cenario
│   └── backgrounds/ # Fundos e musicas
```

---

## FLUXO DO JOGO

1. Menu inicial
2. Fase 1: Runner - Coletar 9 comidas boas, desviar de obstaculos
3. Fase 2: Agua - Coletar 9 comidas boas, fugir dos tubaroes
4. Fase 3: Labirinto - Subir ate o topo, desviar dos tiros
5. Fase 4: Boss - Derrotar o boss com lasers
6. Vitoria!

---

## DICAS DE PROGRAMACAO

### Heranca de Sprite
Sempre herde de `pygame.sprite.Sprite` para objetos visuais.

### Separacao de Responsabilidades
- `update()` = logica (movimento, colisao)
- `draw()` = visual (desenhar na tela)

### Constantes no Topo
Defina SCREEN_WIDTH, TILE_SIZE etc no inicio do arquivo.

### Groups para Gerenciar Sprites
Use Groups para facilitar update/draw de multiplos objetos.