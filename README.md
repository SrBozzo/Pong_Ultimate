# Pong_Ultimate
O clássico de Arcade refeito em Python com uma dose extra de caos! Jogue contra uma IA esperta ou desafie amigos no modo PvP. Com power-ups aleatórios, física de efeito (spin) e sistema de recordes, este não é apenas um Pong comum

# 🏓 Pong Ultimate 3.0

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Concluído-success?style=for-the-badge)
![Licença](https://img.shields.io/badge/Licença-Livre-green?style=for-the-badge)

A evolução do Pong clássico feito do zero em Python (Turtle)! Divirta-se com físicas de efeito (spin), power-ups caóticos e obstáculos dinâmicos. Desafie uma IA inteligente, jogue contra amigos no modo PvP ou tente bater o recorde de trocas de bola. Nostálgico, modular e muito divertido!

<img width="800" height="624" alt="image" src="https://github.com/user-attachments/assets/80a7d6f7-cb7f-4349-8c5c-c490bd913528" />

<img width="799" height="629" alt="image" src="https://github.com/user-attachments/assets/708c263e-e719-4ef4-af57-c341e919cd73" />

---

## ✨ Funcionalidades em Destaque

* 🤖 **IA Preditiva & Fluida:** A inteligência artificial não segue apenas a bola; ela calcula ricochetes e possui uma "Zona Morta" (Deadzone) para movimentos suaves e realistas.
* 🌪️ **Física de Efeito (Spin):** Acerte na bola com as bordas da raquete para alterar drasticamente o ângulo de ressalto.
* 🎁 **Power-Ups Caóticos:** Itens aleatórios que podem deixar a sua raquete Gigante, encolher o inimigo ou ativar o Modo Turbo!
* 🚧 **Obstáculos Dinâmicos:** Em campos maiores, blocos móveis no centro do ecrã criam ricochetes imprevisíveis.
* 🎨 **Personalização (Skins):** Altere as cores do jogo em tempo real (Classic White, Neon Blue, Matrix Green, Sunset Orange).
* 🏆 **Sistema de Campeão & Recordes:** Jogue partidas de "Melhor de X" pontos e compita pelo recorde máximo de "Troca de Bolas" (guardado automaticamente num ficheiro `.txt`).
* 🎵 **Áudio Retro:** Efeitos sonoros clássicos de 8-bits para colisões e golos.

---

## 🎮 Como Jogar

**Navegação nos Menus:**
* **Setas ⬆️ ⬇️:** Escolher a opção.
* **Setas ⬅️ ➡️:** Alterar o valor (Dificuldade, Temas, etc.).
* **ENTER:** Confirmar e Iniciar.

**Controlos de Jogo:**
* **Jogador 1 (Esquerda):** Teclas `W` (Cima) e `S` (Baixo)
* **Jogador 2 (Direita):** `Seta Cima` e `Seta Baixo`
* **Pausar Jogo:** Barra de `ESPAÇO`

---

## 🚀 Como Executar o Jogo

### Opção 1: Jogar Imediatamente (.exe)
A forma mais fácil de jogar com amigos!
1. Vá até à secção **Releases** deste repositório.
2. Faça o download do ficheiro `Pong_Ultimate.exe`.
3. Dê um duplo clique para jogar! *(Nota: O Windows pode dar um aviso por ser um ficheiro novo. Basta clicar em "Mais informações" > "Executar assim mesmo").*

### Opção 2: Pelo Código Fonte (Python)
Se quiser ver ou modificar o código:
1. Certifique-se de que tem o Python instalado.
2. Faça o clone deste repositório.
3. Certifique-se de que os três ficheiros (`main.py`, `configuracoes.py` e `ia_engine.py`) estão na mesma pasta.
4. Execute o ficheiro principal no terminal:
   ```bash
   python main.py

---

## 🏗️ Arquitetura Modular

Este projeto foi construído seguindo boas práticas de modularização em programação:

main.py: Gestão de interface, inputs, gráficos e loop físico.

ia_engine.py: Motor matemático isolado para predição de trajetórias.

configuracoes.py: Central de dicionários e constantes do jogo.

Desenvolvido por [SrBozzo](https://github.com/SrBozzo)
