# Projeto **Jog (Based)**

Este projeto consiste em um jogo educativo simples desenvolvido em **Pygame**, criado como requisito da disciplina **Laboratório de Engenharia de Software**. Ele consiste em um plataformer de **quatro fases** com um **menu de configurações**, onde o jogador pode escolher quais músicas deseja ouvir em cada fase.

## Como Executar

### **Pré-requisitos**
- Python 3.12.16 instalado

### **Passos**
1. Clone o repositório com:
```bash
git clone https://github.com/yuri-iqi/jog.git
```

2. Instale as dependências listadas em `requirements.txt` com o comando:

```bash
pip install -r requirements.txt
```
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

## Documentação
A pasta **`docs/`** contém documentos que descrevem as principais funcionalidades da aplicação.  
Eles são recomendados para auxiliar no entendimento da arquitetura e das decisões de implementação do projeto.

## Testes
Na pasta **`tests/`** estão disponíveis quatro suites de teste que cobrem os principais métodos responsáveis pela jogabilidade e pelo funcionamento essencial da aplicação.  
Os testes abrangem:
- Jogador  
- Fases  
- Itens  
- Menu  
