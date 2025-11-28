<<<<<<< HEAD
# BASED - Jogo Educativo sobre Alimentação Saudável

Um jogo desenvolvido em Python com Pygame que ensina sobre alimentação saudável de forma divertida através de 4 fases únicas.

---

## Índice

1. [Requisitos do Sistema](#requisitos-do-sistema)
2. [Instalação](#instalação)
3. [Como Executar](#como-executar)
4. [Controles](#controles)
5. [Menu Principal](#menu-principal)
6. [As 4 Fases do Jogo](#as-4-fases-do-jogo)
7. [Itens do Jogo](#itens-do-jogo)
8. [Dicas de Gameplay](#dicas-de-gameplay)
9. [Estrutura de Arquivos](#estrutura-de-arquivos)
10. [Solução de Problemas](#solução-de-problemas)
11. [Créditos](#créditos)

---

## Requisitos do Sistema

### Software Necessário
- **Python 3.8 ou superior** (recomendado: Python 3.11+)
- **Pygame 2.0 ou superior**
- **Pillow (PIL)** - Para processamento de imagens no boss
---

## Instalação

### Passo 1: Instalar Python

**Windows:**
1. Acesse https://www.python.org/downloads/
2. Baixe a versão mais recente do Python
3. Execute o instalador
4. **IMPORTANTE:** Marque a opção "Add Python to PATH"
5. Clique em "Install Now"

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**macOS:**
```bash
brew install python3
```

### Passo 2: Instalar Dependências

Abra o terminal/prompt de comando na pasta do jogo e execute:

```bash
pip install pygame pillow
```

Ou, se preferir instalar todas de uma vez:
=======
# Projeto **Jog (Based)**

Este projeto consiste em um jogo educativo simples desenvolvido em **Pygame**, criado como requisito da disciplina **Laboratório de Engenharia de Software**, com o objetivo de estimular uma nutrição saudável de uma forma divertida. Ele consiste em um plataformer de **quatro fases** com um **menu de configurações**, onde o jogador pode escolher quais músicas deseja ouvir em cada fase.

## Como Executar

### **Pré-requisitos**
- Python 3.12.16 instalado

### **Passos**
1. Clone o repositório com:
```bash
git clone https://github.com/yuri-iqi/jog.git
```

2. Instale as dependências listadas em `requirements.txt` com o comando:
>>>>>>> e4da0e2a579d4087b3c12eb207389da80fcbcbb0

```bash
pip install -r requirements.txt
```
<<<<<<< HEAD

### Passo 3: Verificar Instalação

```bash
python --version
pip show pygame
```

---

## Como Executar

### Método 1: Terminal/Prompt de Comando

1. Abra o terminal ou prompt de comando
2. Navegue até a pasta do jogo:
   ```bash
   cd caminho/para/jog
   ```
3. Execute o jogo:
   ```bash
   python main.py
   ```

### Método 2: Clique Duplo (Windows)

1. Navegue até a pasta do jogo
2. Clique duas vezes no arquivo `main.py`
3. O jogo abrirá automaticamente

### Método 3: IDE (VSCode, PyCharm)

1. Abra a pasta do projeto na IDE
2. Abra o arquivo `main.py`
3. Pressione F5 ou clique em "Run"

---

## Controles

### Controles Universais

| Tecla | Ação |
|-------|------|
| **P** | Pausar o jogo |
| **Mouse** | Navegar menus e clicar botões |

### Fase 1 - Runner

| Tecla | Ação |
|-------|------|
| **← / A** | Mover para esquerda |
| **→ / D** | Mover para direita |
| **ESPAÇO / ↑ / W** | Pular |

### Fase 2 - Água

| Tecla | Ação |
|-------|------|
| **↑** | Nadar para cima |
| **↓** | Nadar para baixo |
| **←** | Nadar para esquerda |
| **→** | Nadar para direita |

### Fase 3 - Labirinto

| Tecla | Ação |
|-------|------|
| **← / A** | Mover para esquerda |
| **→ / D** | Mover para direita |
| **ESPAÇO / ↑ / W** | Pular |

### Fase 4 - Boss

| Tecla | Ação |
|-------|------|
| **← / A** | Mover para esquerda |
| **→ / D** | Mover para direita |
| **ESPAÇO / ↑ / W** | Pular |
| **F** | Atirar laser |

---

## Menu Principal

Ao iniciar o jogo, você verá o menu principal com as seguintes opções:

### 1. Iniciar Jogo
Começa o jogo pela Fase 1 (Runner).

### 2. Escolher Fase
Permite selecionar qualquer uma das 4 fases:
- **Fase 1:** Runner
- **Fase 2:** Água
- **Fase 3:** Labirinto
- **Fase 4:** Boss

### 3. Configurar Música
Personalize a trilha sonora de cada fase:
- Use as setas **<** e **>** para navegar pelas músicas
- Clique em **Salvar** para confirmar as alterações

### 4. Escutar Músicas
Player de música integrado:
- **<** / **>**: Música anterior/próxima
- **Play/Pause**: Iniciar ou pausar
- **STOP**: Parar a música

### 5. Créditos
Veja a equipe por trás do jogo.

### 6. Sair
Fecha o jogo.

---

## As 4 Fases do Jogo

### FASE 1: Runner (Corrida)

**Objetivo:** Coletar 9 comidas boas enquanto desvia dos obstáculos.

**Mecânicas:**
- O cenário se move automaticamente (estilo endless runner)
- A velocidade aumenta conforme o tempo passa
- Mais obstáculos aparecem quanto mais rápido fica

**Obstáculos:**
- 🪨 **Pedras:** Colisão = Game Over imediato
- 🌵 **Cactos:** Colisão = Game Over imediato
- 🍔 **Comidas ruins:** Prejudicam o jogador

**Comidas Boas:**
- Aparecem no ar a cada 6 obstáculos
- Pule para coletá-las!

**Vitória:** Colete 9 comidas boas
**Derrota:** Toque em pedra ou cacto

---

### FASE 2: Água (Natação)

**Objetivo:** Coletar 9 comidas boas enquanto foge dos tubarões.

**Mecânicas:**
- Movimento livre em todas as direções
- Comidas caem do topo da tela
- Tubarões nadam horizontalmente

**Perigos:**
- 🦈 **Tubarões:** Colisão = Game Over imediato
- 🍔 **Comidas ruins:** Contam como item ruim

**Vitória:** Colete 9 comidas boas
**Derrota:** Toque em tubarão ou colete 8 comidas ruins

---

### FASE 3: Labirinto

**Objetivo:** Subir até o topo do labirinto desviando dos tiros dos canhões.

**Mecânicas:**
- Labirinto com paredes e passagens
- 29 canhões espalhados pelo mapa
- Canhões atiram comidas ruins periodicamente

**Coleta:**
- 35 itens espalhados pelo labirinto (bons e ruins)
- Colete os bons para recuperar energia

**Vitória:** Saia pelo topo do mapa
**Derrota:** Seja atingido 3 vezes pelos projéteis

---

### FASE 4: Boss (Batalha Final)

**Objetivo:** Derrotar o Boss usando lasers.

**Cutscenes:**
- Diálogo de apresentação no início
- Cutscene especial quando o boss entra em Rage Mode

**Mecânicas do Boss:**
- **Vida:** 1800 HP
- Move-se em diagonal pela tela
- Atira comidas ruins em todas as direções
- **Rage Mode (50% HP):** Fica mais rápido e atira mais

**Seu Arsenal:**
- **Laser (F):** 20 de dano (normal) / 40 de dano (forte)
- **PowerUps:** O boss dropa a cada 4 hits
  - Concedem armadura (absorve 2 hits)
  - Ativam laser forte por 8 segundos

**Vitória:** Reduza o HP do boss a 0
**Derrota:** Perca todas as 5 vidas

---

## Itens do Jogo

### Comidas Boas (Colete!)
| Item | Efeito |
|------|--------|
| 🍎 **Maçã** | +1 item bom |
| 🍌 **Banana** | +1 item bom |
| 🥬 **Alface** | +1 item bom |

### Comidas Ruins (Evite!)
| Item | Efeito |
|------|--------|
| 🍔 **Hambúrguer** | +1 item ruim |
| 🥤 **Refrigerante** | +1 item ruim |
| 🍦 **Sorvete** | +1 item ruim |

### Obstáculos Mortais (Fase 1)
| Item | Efeito |
|------|--------|
| 🪨 **Pedra** | Game Over |
| 🌵 **Cacto** | Game Over |

### PowerUps (Fase 4)
| Item | Efeito |
|------|--------|
| 💧 **Garrafa d'água** | Armadura + Laser forte |
| 🏋️ **Halteres** | Armadura + Laser forte |

---

## Dicas de Gameplay

### Fase 1 - Runner
- Fique atento ao ritmo da música para prever obstáculos
- Pule cedo para pegar comidas no ar
- Não se arrisque demais - a velocidade só aumenta!

### Fase 2 - Água
- Fique sempre em movimento
- Observe o padrão dos tubarões antes de atravessar
- Priorize comidas boas, mas não ignore a posição

### Fase 3 - Labirinto
- Memorize as posições dos canhões
- Espere o momento certo para passar
- Colete comidas boas para compensar hits

### Fase 4 - Boss
- Mantenha distância do boss
- Colete os PowerUps imediatamente quando droparem
- Use o laser forte no Rage Mode para dano máximo
- Memorize o padrão de movimento do boss

---

## Estrutura de Arquivos

```
jog/
├── main.py              # Arquivo principal - execute este
├── player.py            # Classe do jogador
├── item.py              # Sistema de itens e obstáculos
├── level.py             # Fase 1 - Runner
├── level2.py            # Fase 2 - Água
├── level3.py            # Fase 3 - Labirinto
├── level4.py            # Fase 4 - Boss
├── menu.py              # Menu principal
├── pause.py             # Menu de pausa
├── music_config.json    # Configurações de música
├── README.md            # Este arquivo
│
├── assets/
│   ├── player/          # Sprites do jogador
│   │   ├── Boneco A1.png
│   │   ├── Boneco A2.png
│   │   └── gordo/
│   │       └── Gordo.png
│   │
│   ├── item/            # Sprites dos itens
│   │   ├── Maçã.png
│   │   ├── Banana.png
│   │   ├── Alface.png
│   │   ├── Hamburguer.png
│   │   ├── Refrigerante.png
│   │   ├── Sorvete.png
│   │   ├── Tubarao1.png
│   │   ├── Tubarao2.png
│   │   └── canhao.png
│   │
│   ├── tiles/           # Tiles do cenário
│   │   ├── Terreno 01.png
│   │   ├── Terreno 02.png
│   │   └── Terreno 03.png
│   │
│   └── backgrounds/     # Fundos e áudio
│       ├── fase1.jpg
│       ├── fase2.jpg
│       ├── fase3.jpg
│       ├── fase4.jpg
│       ├── victory.png
│       ├── gameover.jpg
│       │
│       └── audio/       # Músicas
│           ├── Aquatic Ambience.mp3
│           └── [outras músicas...]
│
└── tests/               # Testes automatizados
    ├── test_item.py
    ├── test_player.py
    └── test_levels.py
```

---

## Solução de Problemas

### "Python não é reconhecido como comando"
- Reinstale o Python marcando "Add Python to PATH"
- Ou adicione manualmente ao PATH do sistema

### "ModuleNotFoundError: No module named 'pygame'"
```bash
pip install pygame
```

### "ModuleNotFoundError: No module named 'PIL'"
```bash
pip install pillow
```

### O jogo abre e fecha imediatamente
- Execute pelo terminal para ver mensagens de erro
- Verifique se todos os arquivos de assets existem

### Sem áudio
- Verifique se a pasta `assets/backgrounds/audio/` contém arquivos .mp3
- Certifique-se que seu sistema tem drivers de áudio instalados

### Performance baixa
- Feche outros programas
- Verifique se está usando Python 3.8+
- Atualize os drivers gráficos

### Tela preta ou em branco
- Verifique se as imagens de background existem
- Reinstale o Pygame: `pip install --upgrade pygame`

---

## Executando os Testes

Para verificar se tudo está funcionando:

```bash
cd caminho/para/jog
python -m pytest tests/ -v
```

Resultado esperado: **52 testes passando**

---

## Créditos

**Desenvolvido por:** Grupo Siensia de Notebuqui

- **Programação:** Rafael Menezes
- **Assets & Design:** Manoel Macedo
- **Equipe Criativa:** Murilo Pedral, Anthony Yuri
- **Product Owner:** Franck Patrick
- **Scrum Master:** Rene Marinho

---

## Licença

Este projeto foi desenvolvido para fins acadêmicos.

---

**Divirta-se jogando e aprendendo sobre alimentação saudável!** 🍎🥬🍌
=======
ou
```bash
pip3 install -r requirements.txt
```

3. Execute o jogo com o comando:

```bash
python -m main
```

## Como Jogar

Ao iniciar o jogo, você será direcionado ao **menu principal**, onde poderá acessar as seguintes opções:

- **Iniciar Jogo**  
  Inicia o jogo na **primeira fase**.

- **Escolher Fase**  
  Permite selecionar uma das **quatro fases** disponíveis.

- **Configurar Música**  
  Define quais músicas serão tocadas em cada fase.

- **Escutar Músicas**  
  Permite ouvir todas as trilhas disponíveis no jogo.

- **Créditos**  
  Exibe o nome dos integrantes da equipe.

- **Sair**  
  Fecha o jogo.

Durante qualquer fase, o jogador pode **pausar** o jogo pressionando a tecla **P**.  
No menu de pausa é possível **continuar jogando**, **retornar ao menu principal** ou **sair do jogo**.

### Controles
O jogador pode se movimentar com:
- **Setas direcionais do teclado**, ou  
- Teclas **W**, **A**, **S**, **D**.

### Fim de Jogo
O jogo é perdido quando o jogador colide com certos obstáculos ou consome muitos itens ruins.  
Ao perder, a tela de **Game Over** será exibida, permitindo reiniciar o jogo desde a primeira fase escolhendo **"Recomeçar"**.

### Fase 1 — **Runner**
Nesta fase, o jogador corre automaticamente em alta velocidade por um cenário lateral. O objetivo é **desviar de obstáculos** e **coletar itens bons** enquanto evita itens ruins.

### Mecânicas principais:
- **Obstáculos (pedras e cactos):**  
  Colidir com qualquer obstáculo resulta em **perda imediata da fase**.
- **Itens ruins (hambúrgueres, refrigerantes e sorvetes):**  
  Aumentam o contador de itens prejudiciais; consumir muitos leva à derrota.
- **Itens bons (bananas, alfaces, maçãs):**  
  Cada item aumenta o progresso da fase.
- **Objetivo:**  
  Coletar **9 itens bons** para avançar para a próxima fase.

---

### Fase 2 — **Fase da Água**
Nesta fase, o jogador nada em uma área submersa, podendo se mover livremente enquanto evita perigos e coleta itens bons.

### Mecânicas principais:
- **Movimentação livre na água:**  
  O jogador pode nadar em todas as direções.
- **Tubarões:**  
  Nadam de um lado ao outro da tela. A colisão com um tubarão resulta em derrota.
- **Itens bons aquáticos:**  
  Itens aparecem ao longo do percurso e devem ser coletados para progredir.

---

### Fase 3 — **Labirinto**
Nesta fase, o jogador deve atravessar um mapa de **baixa visibilidade** e **espaços estreitos**, enquanto desvia de disparos de itens ruins lançados por canhões.  
O objetivo é **alcançar a saída localizada no topo do mapa**.

### Mecânicas principais:
- **Canhões de itens ruins:**  
  Diversos canhões estão posicionados pelo cenário, disparando itens ruins em intervalos constantes.
- **Modificação da altura do pulo:**  
  Consumir itens bons aumenta a altura do pulo do jogador, enquanto itens ruins diminuem essa altura.
- **Vidas limitadas:**  
  O jogador possui **3 vidas**, perdendo uma a cada vez que é atingido por um item ruim.

---

### Fase 4 — **Boss**
Na fase final, o jogador enfrenta uma **marca de refrigerantes** em uma batalha decisiva.

### Mecânicas principais:
- **Boss com dois modos de combate:**  
  Ao atingir metade da vida, o Boss entra em um segundo modo, tornando-se mais rápido e mais agressivo.
- **Disparo do jogador:**  
  O jogador pode atacar o Boss usando disparos, pressionando as teclas **F** ou **K**.
- **Itens especiais:**  
  Ao causar dano ao Boss, novos itens caem no cenário. Eles podem **melhorar o disparo** ou fornecer **armadura**, oferecendo proteção adicional.

## Documentação
A pasta **`docs/`** contém documentos que descrevem as principais funcionalidades da aplicação de forma técnica.  
Eles são recomendados para auxiliar no entendimento da arquitetura e das decisões de implementação do projeto.

## Testes
Na pasta **`tests/`** estão disponíveis quatro suites de teste que cobrem os principais métodos responsáveis pela jogabilidade e pelo funcionamento essencial da aplicação.  
Os testes abrangem:
- Jogador  
- Fases  
- Itens  
- Menu  
>>>>>>> e4da0e2a579d4087b3c12eb207389da80fcbcbb0
