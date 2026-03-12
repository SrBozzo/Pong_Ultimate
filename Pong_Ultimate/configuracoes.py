# ==============================================================================
# FICHEIRO: configuracoes.py
# OBJETIVO: Guardar todas as constantes e definições do jogo.
# VANTAGEM: Se quiseres equilibrar a velocidade ou mudar uma cor, 
#           só precisas de alterar aqui, sem tocar no código complexo.
# ==============================================================================

# Listas que definem a ordem e o texto dos menus
MENU_INICIAL = [
    "Inteligência IA", "Velocidade Bola", "Tamanho Campo", 
    "Modo de Jogo", "Pontos para Vencer", "Tema Visual", 
    "Power-Ups", "Obstáculos", "INICIAR JOGO", "SAIR"
]

MENU_PAUSA = ["RETORNAR AO JOGO", "NOVO JOGO (MENU)", "SAIR DO JOGO"]

# Dicionário que guarda as opções disponíveis para cada categoria do menu
VALORES = {
    "Inteligência IA": ["Iniciante", "Amador", "Profissional", "Lenda", "Máquina"],
    "Velocidade Bola": ["Lenta", "Média", "Rápida", "Turbo"],
    "Tamanho Campo": ["800x600", "1000x700", "1400x850"],
    "Modo de Jogo": ["Jogador vs IA", "Jogador vs Jogador", "IA vs IA"],
    "Pontos para Vencer": ["3", "5", "10", "Infinito"],
    "Tema Visual": ["Classic White", "Neon Blue", "Matrix Green", "Sunset Orange"],
    "Power-Ups": ["Ligado", "Desligado"],
    "Obstáculos": ["Ligado", "Desligado"]
}

# Dicionário de cores hexadecimais (Skins do Jogo)
CORES_TEMA = {
    "Classic White": "white",
    "Neon Blue": "#00ffff",    # Ciano brilhante/Néon
    "Matrix Green": "#33ff33", # Verde estilo Matrix
    "Sunset Orange": "#ff6600" # Laranja vibrante
}

# Perfil da IA -> Formato: (Velocidade_Movimento, Margem_de_Erro_Pixels)
DADOS_IA = {
    "Iniciante": (0.15, 70),   # Move-se devagar e tem uma zona morta enorme
    "Amador": (0.25, 40),      # Erra um bocado
    "Profissional": (0.35, 15),# Erra pouco
    "Lenda": (0.5, 5),         # Quase perfeita
    "Máquina": (0.8, 0)        # Reage instantaneamente, erro zero
}

# Perfil da Bola -> Velocidade base (Movimento por frame)
DADOS_BOLA = {
    "Lenta": 0.25, 
    "Média": 0.4, 
    "Rápida": 0.65, 
    "Turbo": 0.9
}