# ==============================================================================
# FICHEIRO: main.py
# ==============================================================================

import turtle
import time
import random
import webbrowser
import os # Para lidar com o ficheiro de recordes
import configuracoes as cfg
from ia_engine import calcular_movimento_ia

# Tentar importar biblioteca de sons (Apenas funciona no Windows)
try:
    import winsound
    tem_som = True
except ImportError:
    tem_som = False

# --- CONFIGURAÇÃO DO ECRÃ ---
ecra = turtle.Screen()
ecra.title("Pong Ultimate 3.0")
ecra.bgcolor("black")
ecra.tracer(0)

LARGURA, ALTURA = 800, 600
ecra.setup(width=LARGURA, height=ALTURA)

# Variáveis de Estado
jogo_ativo = False
jogo_pausado = False
indice_menu = 0 
sel = {
    "Inteligência IA": 2, "Velocidade Bola": 1, "Tamanho Campo": 0, 
    "Modo de Jogo": 0, "Pontos para Vencer": 1, "Tema Visual": 0,
    "Power-Ups": 0, "Obstáculos": 0
}
pontos_1, pontos_2 = 0, 0
rastros_bola = []
ultimo_batedor = None
cor_atual = "white"

# SISTEMA DE RECORDES (Maior Troca de Bolas)
FICHEIRO_RECORDE = "recorde_pong.txt"
trocas_atuais = 0
recorde_maximo = 0

def carregar_recorde():
    global recorde_maximo
    if os.path.exists(FICHEIRO_RECORDE):
        with open(FICHEIRO_RECORDE, "r") as ficheiro:
            try: recorde_maximo = int(ficheiro.read())
            except: recorde_maximo = 0

def guardar_recorde():
    with open(FICHEIRO_RECORDE, "w") as ficheiro:
        ficheiro.write(str(recorde_maximo))

carregar_recorde() # Carrega o recorde mal o jogo abre

# SISTEMA DE SONS 8-BIT
def tocar_som(tipo):
    if not tem_som: return
    # MessageBeep toca sons assíncronos (não trava o jogo)
    if tipo == "raquete": winsound.MessageBeep(winsound.MB_OK)
    elif tipo == "parede": winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
    elif tipo == "golo": winsound.MessageBeep(winsound.MB_ICONHAND)

# --- ELEMENTOS DO JOGO ---
def criar_objeto(forma, cor):
    obj = turtle.Turtle()
    obj.speed(0); obj.shape(forma); obj.color(cor); obj.penup(); obj.hideturtle()
    return obj

raquete_esq = criar_objeto("square", "white"); raquete_esq.shapesize(5, 1)
raquete_dir = criar_objeto("square", "white"); raquete_dir.shapesize(5, 1)
bola = criar_objeto("square", "white")
placar = criar_objeto("square", "white")
caneta_menu = criar_objeto("square", "yellow")
caneta_rede = criar_objeto("square", "gray"); caneta_rede.pensize(2)

obs_cima = criar_objeto("square", "gray"); obs_cima.shapesize(4, 1); obs_cima.dy = 0.2
obs_baixo = criar_objeto("square", "gray"); obs_baixo.shapesize(4, 1); obs_baixo.dy = -0.2
powerup_item = criar_objeto("circle", "yellow"); powerup_item.shapesize(1.5, 1.5)

# Variáveis Power-Up
tempo_proximo_powerup = 0
powerup_ativo = False
efeito_ativo = None
fim_efeito = 0

# --- FUNÇÕES DE SUPORTE ---
def aplicar_tema():
    global cor_atual
    cor_atual = cfg.CORES_TEMA[cfg.VALORES["Tema Visual"][sel["Tema Visual"]]]
    for obj in [raquete_esq, raquete_dir, placar, caneta_rede, bola]: obj.color(cor_atual)

def desenhar_rede():
    caneta_rede.clear(); caneta_rede.penup(); caneta_rede.goto(0, ALTURA/2); caneta_rede.setheading(270)
    for _ in range(int(ALTURA // 30)):
        caneta_rede.pendown(); caneta_rede.forward(15); caneta_rede.penup(); caneta_rede.forward(15)

def limpar_rastro():
    for carimbo in rastros_bola: bola.clearstamp(carimbo)
    rastros_bola.clear()

def atualizar_cor_bola():
    if abs(bola.dx) > 0.8: bola.color("white")
    else: bola.color(cor_atual)

def atualizar_placar():
    if jogo_ativo:
        placar.clear()
        texto = f"P1: {pontos_1}  P2: {pontos_2}\nRecorde de Trocas: {recorde_maximo}"
        placar.write(texto, align="center", font=("Courier", 18, "normal"))

def mostrar_golo(quem):
    global trocas_atuais
    tocar_som("golo")
    trocas_atuais = 0 # Reinicia a contagem de trocas no golo
    
    caneta_menu.clear(); caneta_rede.clear()
    caneta_menu.goto(0, 50); caneta_menu.color("red")
    caneta_menu.write("GooooLL!!!!!!!", align="center", font=("Courier", 45, "bold"))
    caneta_menu.goto(0, -20); caneta_menu.color(cor_atual)
    caneta_menu.write(f"PONTO PARA: {quem.upper()}", align="center", font=("Courier", 20, "bold"))
    ecra.update(); time.sleep(3); caneta_menu.clear()
    
    limite = cfg.VALORES["Pontos para Vencer"][sel["Pontos para Vencer"]]
    if limite != "Infinito" and (pontos_1 >= int(limite) or pontos_2 >= int(limite)):
        mostrar_game_over(quem)
    else:
        desenhar_rede(); reposicionar_elementos(quem)

def mostrar_game_over(vencedor):
    global jogo_ativo, indice_menu
    jogo_ativo = False; indice_menu = 0
    esconder_elementos_jogo()
    caneta_menu.goto(0, 50); caneta_menu.color("gold")
    caneta_menu.write("🏆 TEMOS UM CAMPEÃO! 🏆", align="center", font=("Courier", 40, "bold"))
    caneta_menu.goto(0, -10); caneta_menu.color("white")
    caneta_menu.write(f"Vitória de {vencedor.upper()}", align="center", font=("Courier", 22, "bold"))
    caneta_menu.goto(0, -70); caneta_menu.color("yellow")
    caneta_menu.write("Pressione ENTER para voltar ao Menu", align="center", font=("Courier", 16, "normal"))
    ecra.update()

def esconder_elementos_jogo():
    for obj in [raquete_esq, raquete_dir, bola, obs_cima, obs_baixo, powerup_item]: obj.hideturtle()
    placar.clear(); caneta_rede.clear(); limpar_rastro()

# --- POWER-UPS ---
def resetar_efeitos():
    global efeito_ativo
    efeito_ativo = None
    raquete_esq.shapesize(5, 1); raquete_dir.shapesize(5, 1)
    powerup_item.hideturtle()

def aplicar_powerup():
    global efeito_ativo, fim_efeito, powerup_ativo
    efeito_ativo = random.choice(["GIGANTE", "FORMIGA", "TURBO"])
    fim_efeito = time.time() + 10 
    powerup_ativo = False; powerup_item.hideturtle()

    if efeito_ativo == "GIGANTE":
        if ultimo_batedor == "Esquerda": raquete_esq.shapesize(10, 1)
        else: raquete_dir.shapesize(10, 1)
    elif efeito_ativo == "FORMIGA":
        if ultimo_batedor == "Esquerda": raquete_dir.shapesize(2, 1) 
        else: raquete_esq.shapesize(2, 1)
    elif efeito_ativo == "TURBO":
        bola.dx *= 1.5; bola.dy *= 1.5

# --- FLUXO DE MENUS E NAVEGAÇÃO ---
def desenhar_menu():
    caneta_menu.clear()
    if not jogo_ativo: esconder_elementos_jogo()

    lista = cfg.MENU_PAUSA if jogo_pausado else cfg.MENU_INICIAL
    titulo = "PAUSA" if jogo_pausado else "PONG ULTIMATE 3.0"
    
    caneta_menu.goto(0, 220); caneta_menu.color(cor_atual if jogo_ativo else "cyan")
    caneta_menu.write(titulo, align="center", font=("Courier", 35, "bold"))
    
    for i, opcao in enumerate(lista):
        caneta_menu.goto(0, 140 - (i * 35))
        caneta_menu.color("yellow" if i == indice_menu else "white")
        texto = f"--> {opcao}" if i == indice_menu else f"    {opcao}"
        if not jogo_pausado and i < 8: texto += f": {cfg.VALORES[opcao][sel[opcao]]}"
        caneta_menu.write(texto, align="center", font=("Courier", 16, "bold" if i == indice_menu else "normal"))
    
    caneta_menu.goto(0, -ALTURA/2 + 30); caneta_menu.color("#4da6ff")
    caneta_menu.write("by: SrBozzo (Clique para o GitHub)", align="center", font=("Courier", 12, "italic"))
    ecra.update()

def confirmar():
    global jogo_ativo, jogo_pausado, indice_menu, pontos_1, pontos_2, trocas_atuais
    if not jogo_ativo and not jogo_pausado:
        if indice_menu == 8: # INICIAR
            pontos_1 = pontos_2 = trocas_atuais = 0
            jogo_ativo = True
            reposicionar_elementos()
            # Contagem Regressiva
            caneta_menu.clear(); raquete_esq.showturtle(); raquete_dir.showturtle(); bola.showturtle()
            if cfg.VALORES["Obstáculos"][sel["Obstáculos"]] == "Ligado" and LARGURA > 800: obs_cima.showturtle(); obs_baixo.showturtle()
            atualizar_placar(); aplicar_tema()
            for i in ["3", "2", "1", "LUTA!!"]:
                caneta_menu.goto(0, 0); caneta_menu.color("white")
                caneta_menu.write(i, align="center", font=("Courier", 50, "bold"))
                ecra.update(); time.sleep(1); caneta_menu.clear()
            desenhar_rede()
        elif indice_menu == 9: ecra.bye()
            
    elif jogo_pausado:
        if indice_menu == 0: jogo_pausado = False; caneta_menu.clear()
        elif indice_menu == 1: jogo_ativo = jogo_pausado = False; indice_menu = 0; desenhar_menu()
        elif indice_menu == 2: ecra.bye()

def tecla_cima():
    global indice_menu
    if not jogo_ativo or jogo_pausado:
        indice_menu = (indice_menu - 1) % len(cfg.MENU_PAUSA if jogo_pausado else cfg.MENU_INICIAL)
        desenhar_menu()
    elif cfg.VALORES["Modo de Jogo"][sel["Modo de Jogo"]] == "Jogador vs Jogador":
        if raquete_dir.ycor() < (ALTURA/2 - 60): raquete_dir.sety(raquete_dir.ycor() + 45)

def tecla_baixo():
    global indice_menu
    if not jogo_ativo or jogo_pausado:
        indice_menu = (indice_menu + 1) % len(cfg.MENU_PAUSA if jogo_pausado else cfg.MENU_INICIAL)
        desenhar_menu()
    elif cfg.VALORES["Modo de Jogo"][sel["Modo de Jogo"]] == "Jogador vs Jogador":
        if raquete_dir.ycor() > -(ALTURA/2 - 60): raquete_dir.sety(raquete_dir.ycor() - 45)

def alterar_valor(dir):
    global LARGURA, ALTURA
    if not jogo_ativo and not jogo_pausado and indice_menu < 8:
        cat = cfg.MENU_INICIAL[indice_menu]
        sel[cat] = (sel[cat] + dir) % len(cfg.VALORES[cat])
        if cat == "Tamanho Campo":
            res = cfg.VALORES["Tamanho Campo"][sel["Tamanho Campo"]].split('x')
            LARGURA, ALTURA = int(res[0]), int(res[1])
            ecra.setup(width=LARGURA, height=ALTURA)
        elif cat == "Tema Visual": aplicar_tema()
        desenhar_menu()

def reposicionar_elementos(quem_marcou=None):
    global tempo_proximo_powerup, powerup_ativo
    raquete_esq.goto(-(LARGURA/2 - 50), 0); raquete_dir.goto((LARGURA/2 - 50), 0)
    placar.goto(0, (ALTURA/2 - 50)); bola.goto(0, 0)
    obs_cima.goto(0, ALTURA/4); obs_baixo.goto(0, -ALTURA/4)
    
    resetar_efeitos(); powerup_ativo = False
    tempo_proximo_powerup = time.time() + random.randint(5, 15) 
    limpar_rastro()
    
    if jogo_ativo:
        vel_b = cfg.VALORES["Velocidade Bola"][sel["Velocidade Bola"]]
        if quem_marcou == "Esquerda": bola.dx = cfg.DADOS_BOLA[vel_b]
        elif quem_marcou == "Direita": bola.dx = -cfg.DADOS_BOLA[vel_b]
        else: bola.dx = cfg.DADOS_BOLA[vel_b] * random.choice([-1, 1])
        bola.dy = cfg.DADOS_BOLA[vel_b] * random.choice([-1, 1])
        atualizar_cor_bola()

# Binds do Teclado e Rato
ecra.listen()
def abrir_github(x, y):
    if not jogo_ativo or jogo_pausado:
        if -200 < x < 200 and -ALTURA/2 + 10 < y < -ALTURA/2 + 60: webbrowser.open("https://github.com/SrBozzo")
ecra.onclick(abrir_github)

ecra.onkeypress(tecla_cima, "Up")
ecra.onkeypress(tecla_baixo, "Down")
ecra.onkeypress(lambda: alterar_valor(-1), "Left")
ecra.onkeypress(lambda: alterar_valor(1), "Right")
ecra.onkeypress(confirmar, "Return")
ecra.onkeypress(lambda: globals().update(jogo_pausado=True, indice_menu=0) or desenhar_menu() if jogo_ativo else None, "space")

ecra.onkeypress(lambda: raquete_esq.sety(raquete_esq.ycor()+45) if jogo_ativo and not jogo_pausado and raquete_esq.ycor() < (ALTURA/2-60) else None, "w")
ecra.onkeypress(lambda: raquete_esq.sety(raquete_esq.ycor()-45) if jogo_ativo and not jogo_pausado and raquete_esq.ycor() > -(ALTURA/2-60) else None, "s")

aplicar_tema(); desenhar_menu()

# ---------------------------------------------------------
# 7. MOTOR FÍSICO DO JOGO
# ---------------------------------------------------------
while True:
    ecra.update()
    if jogo_ativo and not jogo_pausado:
        
        rastros_bola.append(bola.stamp())
        if len(rastros_bola) > 5: bola.clearstamp(rastros_bola.pop(0))

        bola.setx(bola.xcor() + bola.dx)
        bola.sety(bola.ycor() + bola.dy)

        # Colisão Bordas Topo/Baixo (Som Parede)
        if abs(bola.ycor()) > (ALTURA/2 - 15): 
            bola.dy *= -1
            tocar_som("parede")
        
        # Obstáculos Dinâmicos
        if cfg.VALORES["Obstáculos"][sel["Obstáculos"]] == "Ligado" and LARGURA > 800:
            for obs in [obs_cima, obs_baixo]:
                obs.sety(obs.ycor() + obs.dy)
                if abs(obs.ycor()) > (ALTURA/2 - 50) or abs(obs.ycor()) < 20: obs.dy *= -1
                if (obs.xcor() - 20 < bola.xcor() < obs.xcor() + 20) and (obs.ycor() - 50 < bola.ycor() < obs.ycor() + 50):
                    bola.dx *= -1; bola.setx(bola.xcor() + bola.dx * 2)
                    tocar_som("parede")

        # Power-Ups
        if cfg.VALORES["Power-Ups"][sel["Power-Ups"]] == "Ligado":
            if not powerup_ativo and efeito_ativo is None and time.time() > tempo_proximo_powerup:
                powerup_item.goto(random.randint(-200, 200), random.randint(-200, 200))
                powerup_item.color(random.choice(["red", "blue", "yellow", "green"]))
                powerup_item.showturtle(); powerup_ativo = True
                
            if powerup_ativo and bola.distance(powerup_item) < 25: aplicar_powerup()
            if efeito_ativo and time.time() > fim_efeito:
                resetar_efeitos(); tempo_proximo_powerup = time.time() + random.randint(10, 20)

        # COLISÕES COM RAQUETES E VERIFICAÇÃO DE RECORDE
        dist_r = LARGURA/2 - 60
        tamanho_dir = 55 * (2 if raquete_dir.shapesize()[0] > 5 else 1)
        if (bola.xcor() > dist_r and bola.xcor() < dist_r + 10) and (abs(bola.ycor() - raquete_dir.ycor()) < tamanho_dir):
            bola.dx *= -1.05; bola.setx(dist_r)
            bola.dy += ((bola.ycor() - raquete_dir.ycor()) / 55) * 0.3
            ultimo_batedor = "Direita"; atualizar_cor_bola()
            tocar_som("raquete")
            
            trocas_atuais += 1
            if trocas_atuais > recorde_maximo:
                recorde_maximo = trocas_atuais
                guardar_recorde()
            atualizar_placar()
            
        tamanho_esq = 55 * (2 if raquete_esq.shapesize()[0] > 5 else 1)
        if (bola.xcor() < -dist_r and bola.xcor() > -dist_r - 10) and (abs(bola.ycor() - raquete_esq.ycor()) < tamanho_esq):
            bola.dx *= -1.05; bola.setx(-dist_r)
            bola.dy += ((bola.ycor() - raquete_esq.ycor()) / 55) * 0.3
            ultimo_batedor = "Esquerda"; atualizar_cor_bola()
            tocar_som("raquete")
            
            trocas_atuais += 1
            if trocas_atuais > recorde_maximo:
                recorde_maximo = trocas_atuais
                guardar_recorde()
            atualizar_placar()

        # IA Lógica
        modo = cfg.VALORES["Modo de Jogo"][sel["Modo de Jogo"]]
        v_ia, erro_ia = cfg.DADOS_IA[cfg.VALORES["Inteligência IA"][sel["Inteligência IA"]]]
        if "IA" in modo:
            if modo != "Jogador vs Jogador": calcular_movimento_ia(raquete_dir, bola, v_ia, erro_ia, ALTURA)
            if modo == "IA vs IA": calcular_movimento_ia(raquete_esq, bola, v_ia, erro_ia, ALTURA)

        # Golos
        if abs(bola.xcor()) > (LARGURA/2):
            if bola.xcor() > 0: pontos_1 += 1; mostrar_golo("Esquerda")
            else: pontos_2 += 1; mostrar_golo("Direita")
            atualizar_placar()