from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 14)
        self.cell(0, 10, 'Documentacao do Jogo - BASED '
        , align='C', new_x='LMARGIN', new_y='NEXT')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', align='C')

    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 8, title, fill=True, new_x='LMARGIN', new_y='NEXT')
        self.ln(3)

    def chapter_subtitle(self, title):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(50, 50, 150)
        self.cell(0, 6, title, new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def body_text(self, text):
        self.set_font('Helvetica', '', 9)
        self.multi_cell(0, 5, text)
        self.ln(2)

    def code_block(self, code):
        self.set_font('Courier', '', 8)
        self.set_fill_color(240, 240, 240)
        self.multi_cell(0, 4, code, fill=True)
        self.ln(2)

pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()



pdf.chapter_title("1. VISAO GERAL")
pdf.body_text("Jogo educativo sobre alimentacao saudavel com 4 fases diferentes. Desenvolvido em Python com Pygame.")


pdf.chapter_title("2. ITEM.PY - Sistema de Itens")
pdf.body_text("Representa todos os itens coletaveis e obstaculos do jogo.")
pdf.chapter_subtitle("Tipos de Itens:")
pdf.body_text("- hamburguer, refrigerante, sorvete = Comidas ruins (prejudicam)\n- maca, alface, banana = Comidas boas (coletaveis)\n- pedra, cacto = Obstaculos mortais (game over)")
pdf.chapter_subtitle("Metodos:")
pdf.body_text("- __init__(): Cria item, carrega imagem\n- _draw_rock(): Desenha pedra\n- _draw_cactus(): Desenha cacto\n- is_good_item(): Verifica se e comida boa\n- update(): Faz item flutuar")


pdf.chapter_title("3. PLAYER.PY - Jogador")
pdf.body_text("Controla o personagem principal.")
pdf.chapter_subtitle("Atributos:")
pdf.body_text("- direction: Vetor de movimento (x, y)\n- speed: Velocidade\n- gravity: Forca da gravidade\n- on_ground: Se pode pular\n- good/bad_items_collected: Contadores")
pdf.chapter_subtitle("Metodos:")
pdf.body_text("- apply_gravity(): Aplica gravidade\n- jump(): Faz o jogador pular\n- collect_item(): Coleta item")


pdf.chapter_title("4. LEVEL.PY - Fase 1 (Runner)")
pdf.body_text("Fase estilo endless runner. Jogador corre automaticamente.")
pdf.chapter_subtitle("Mecanicas:")
pdf.body_text("- Scroll automatico que acelera com o tempo\n- Obstaculos: pedras e cactos (game over ao tocar)\n- Comidas ruins no caminho\n- A cada 7 obstaculos: 2 comidas boas no ar")
pdf.chapter_subtitle("Dificuldade Progressiva:")
pdf.code_block("# A cada 5 segundos:\nscroll_speed += 0.5  # Mais rapido\nobstacle_interval -= 5  # Mais obstaculos")
pdf.chapter_subtitle("Vitoria/Derrota:")
pdf.body_text("- Vitoria: Coletar 9 comidas boas\n- Derrota: Tocar em pedra ou cacto")

pdf.add_page()
pdf.chapter_title("5. LEVEL2.PY - Fase 2 (Agua)")
pdf.body_text("Fase aquatica com movimento livre.")
pdf.chapter_subtitle("Mecanicas:")
pdf.body_text("- Movimento: setas para todas direcoes\n- Tubaroes que se movem horizontalmente\n- Comidas caem do topo\n- Colisao com tubarao = game over")
pdf.chapter_subtitle("Vitoria/Derrota:")
pdf.body_text("- Vitoria: Coletar 9 comidas boas\n- Derrota: Tocar em tubarao ou 8 comidas ruins")

pdf.chapter_title("6. LEVEL3.PY - Fase 3 (Labirinto)")
pdf.body_text("Labirinto com canhoes que atiram comida ruim.")
pdf.chapter_subtitle("Mecanicas:")
pdf.body_text("- Layout em grid (X = parede, espaco = passagem)\n- 29 canhoes posicionados pelo mapa\n- Canhoes atiram comidas ruins periodicamente\n- Movimento: setas + pulo")
pdf.chapter_subtitle("Vitoria/Derrota:")
pdf.body_text("- Vitoria: Sair pelo topo do mapa\n- Derrota: Ser atingido 3 vezes")

pdf.chapter_title("7. LEVEL4.PY - Fase 4 (Boss)")
pdf.body_text("Batalha final contra o Boss.")
pdf.chapter_subtitle("Boss:")
pdf.body_text("- Vida: 1800 HP\n- Move em diagonal pela tela\n- Atira comidas ruins em todas direcoes\n- Rage Mode: 50% HP - fica mais rapido")
pdf.chapter_subtitle("Jogador:")
pdf.body_text("- Tecla F: Atira laser (20 dano)\n- PowerUps: Armadura + Laser forte (40 dano)")
pdf.chapter_subtitle("Cutscenes:")
pdf.body_text("- Inicio: Dialogo de apresentacao\n- Rage Mode: Boss fala 'Eu vou vencer!'")

pdf.add_page()
pdf.chapter_title("8. CONCEITOS PYGAME")

pdf.chapter_subtitle("Sprites e Groups:")
pdf.code_block("class Item(pygame.sprite.Sprite):\n    self.image = pygame.Surface(size)  # Visual\n    self.rect = self.image.get_rect()   # Posicao\n\nself.items = pygame.sprite.Group()\nself.items.add(item)   # Adiciona\nself.items.draw(screen) # Desenha todos")

pdf.chapter_subtitle("Colisoes:")
pdf.code_block("# Sprite vs Group\npygame.sprite.spritecollide(player, items, True)\n\n# Rect vs Rect\nplayer.rect.colliderect(tile.rect)")

pdf.chapter_subtitle("Desenho:")
pdf.code_block("pygame.draw.rect(surface, cor, rect)\npygame.draw.circle(surface, cor, centro, raio)\npygame.draw.polygon(surface, cor, pontos)")

pdf.chapter_subtitle("Teclas:")
pdf.code_block("keys = pygame.key.get_pressed()\nif keys[pygame.K_LEFT]:   # Esquerda\nif keys[pygame.K_SPACE]:  # Pular\nif keys[pygame.K_f]:      # Atirar")

pdf.chapter_subtitle("Audio:")
pdf.code_block("pygame.mixer.music.load('musica.mp3')\npygame.mixer.music.play(-1)  # Loop\npygame.mixer.music.stop()")


pdf.chapter_title("9. FUNCOES PYTHON USADAS")
pdf.chapter_subtitle("random:")
pdf.code_block("random.choice(lista)     # Item aleatorio\nrandom.randint(min, max) # Inteiro aleatorio\nrandom.shuffle(lista)    # Embaralha")

pdf.chapter_subtitle("math:")
pdf.code_block("math.cos(angulo)  # Cosseno\nmath.sin(angulo)  # Seno\nmath.pi           # 3.14159...")

pdf.chapter_subtitle("getattr / hasattr:")
pdf.code_block("# Pega atributo ou valor padrao\ngetattr(self, 'timer', 0)\n\n# Verifica se existe\nif hasattr(item, 'is_falling'):")


pdf.add_page()
pdf.chapter_title("10. FLUXO DO JOGO")
pdf.body_text("1. Menu inicial\n2. Fase 1: Runner - Coletar 9 comidas, desviar obstaculos\n3. Fase 2: Agua - Coletar 9 comidas, fugir tubaroes\n4. Fase 3: Labirinto - Subir ao topo, desviar tiros\n5. Fase 4: Boss - Derrotar com lasers\n6. Vitoria!")

pdf.chapter_title("11. ESTRUTURA DE ARQUIVOS")
pdf.code_block("jog/\n  main.py       # Loop principal\n  player.py     # Classe jogador\n  item.py       # Itens/obstaculos\n  level.py      # Fase 1\n  level2.py     # Fase 2\n  level3.py     # Fase 3\n  level4.py     # Fase 4\n  assets/       # Imagens e sons")

pdf.chapter_title("12. DICAS DE PROGRAMACAO")
pdf.body_text("1. Sempre herde de pygame.sprite.Sprite para objetos visuais\n\n2. Separe logica (update) de visual (draw)\n\n3. Use constantes no topo (SCREEN_WIDTH, TILE_SIZE)\n\n4. Use Groups para gerenciar multiplos sprites\n\n5. hasattr() e getattr() evitam erros de atributos inexistentes")


pdf.output("documentacao_jogo.pdf")
print("PDF gerado com sucesso: documentacao_jogo.pdf")
