# ==============================================================================
# FICHEIRO: ia_engine.py
# OBJETIVO: Processar a Inteligência Artificial preditiva do jogo.
# ==============================================================================

def calcular_movimento_ia(raquete, bola, velocidade, margem_erro, altura_campo):
    """
    IA Preditiva: Calcula onde a bola vai estar no futuro e move a raquete.
    """
    
    # 1. IDENTIFICAR A DIREÇÃO: A bola está a ir em direção à IA?
    # Se a raquete está na direita (x > 0) e a bola vai para a direita (dx > 0) -> Sim!
    esta_a_vir = (raquete.xcor() > 0 and bola.dx > 0) or (raquete.xcor() < 0 and bola.dx < 0)

    if esta_a_vir:
        # 2. CALCULAR TEMPO: Tempo = Distância / Velocidade
        distancia_x = abs(raquete.xcor() - bola.xcor())
        tempo_estimado = distancia_x / abs(bola.dx)
        
        # 3. PROJEÇÃO: Posição Y se o campo fosse infinito
        alvo_y = bola.ycor() + (bola.dy * tempo_estimado)
        
        # 4. FÍSICA DE RICOCHETE: Calcular os "tombos" nas paredes de cima e baixo
        limite_teto = (altura_campo / 2) - 15
        limite_chao = -limite_teto
        
        # Dobra a linha de projeção mentalmente sempre que bate num limite
        while alvo_y > limite_teto or alvo_y < limite_chao:
            if alvo_y > limite_teto:
                alvo_y = limite_teto - (alvo_y - limite_teto) # Bate no teto e desce
            if alvo_y < limite_chao:
                alvo_y = limite_chao + (limite_chao - alvo_y) # Bate no chão e sobe
    else:
        # ESTRATÉGIA: Se a bola foi rebatida, a IA volta ao centro para defender melhor
        alvo_y = 0

    # 5. SEGURANÇA: Impedir que a IA tente sair visualmente do ecrã
    margem_ecra = (altura_campo / 2) - 60
    if alvo_y > margem_ecra: alvo_y = margem_ecra
    if alvo_y < -margem_ecra: alvo_y = -margem_ecra

    # --------------------------------------------------------------------------
    # 6. OTIMIZAÇÃO (CORREÇÃO DE JITTER): ZONA MORTA
    # Em vez de aleatoriedade louca, usamos a margem_erro como tolerância.
    # A IA só se move se estiver fora dessa zona morta.
    # Se o erro for alto (Iniciante), ela acha que já está boa e pára longe da bola!
    # --------------------------------------------------------------------------
    zona_morta = 10 + margem_erro

    # 7. EXECUTAR MOVIMENTO: Move-se de forma suave com base na sua "velocidade"
    if raquete.ycor() < alvo_y - zona_morta:
        raquete.sety(raquete.ycor() + velocidade)
    elif raquete.ycor() > alvo_y + zona_morta:
        raquete.sety(raquete.ycor() - velocidade)