import pygame
import sys

# inicia o pygame
pygame.init()

# cria a janela
LARGURA, ALTURA = 1000, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Bloco de Notas")

#icones
icone = pygame.image.load("img/icon.ico")
icone = pygame.transform.scale(icone, (256, 256))
pygame.display.set_icon(icone)

pygame.display.set_caption("PedroNote")

#Configura o segurar do teclado
#pygame.key.set_repeat(300, 40)


tamanho_fonte_texto = 22
tamanho_fonte_aumentar_dominuir = 28

fonte_menu = pygame.font.SysFont('consolas', 15)
fonte_texto = pygame.font.SysFont('consolas', tamanho_fonte_texto)
fonte_botao_menos_mais = pygame.font.SysFont('consolas', tamanho_fonte_aumentar_dominuir)
fonte_sinal_mais = pygame.font.SysFont('consolas', 19) #O sinal de + é muito grande

linhas = [
    {"texto": ""}
]
linha_atual = 0
onde_digitar = pygame.Rect(3, 40, LARGURA - 3, ALTURA - 40)

tempo_piscada = 500
piscou = False
tempo_desligado = 0
cor_piscada = "white"
segurou = False
escreveu_primeira_letra = False
segurou_excluir = False
excluiu_primeira_vez = False
primeira_vez_segurando_tecla = False
mudar_linha_apagar = False
tempo_ultima_letra_modificada = 0
tempo_botao_excluir_clicado = 0
linha_vazia = False
cursor_automatico = True
numero_seta = 0

tempo_que_letra_foi_solta = 0
tempo_backspace_solto = 0

botoes_do_menu_aparecer = False
menu_opcoes = pygame.Rect(0, 30, 200, 150) #Criei essa variavel para ser global e conseguir usar no IF do loop de eventos
mouse_encima_do_menu_de_opcoes = False
abriu_menu_primeira_vez = False #Para nao fechar automaticamente quando fecha 

def desenhar_texto():
    #Criando texto botoes
    texto_arquivo_opcoes =  fonte_menu.render("Menu", True, "black")
    texto_editar_opcoes =  fonte_menu.render("Editar", True, "black")
    texto_fonte_menos =  fonte_botao_menos_mais.render("-", True, "black")
    texto_fonte_mais =  fonte_sinal_mais.render("+", True, "black")
    texto_tamanho_atual_fonte = fonte_menu.render(f"{tamanho_fonte_texto}", True, "black")

    #Centralizar texto nos botoes
    texto_arquivo_opcoes_coordenada =  texto_arquivo_opcoes.get_rect(center=botao_arquivo.center)
    texto_editar_opcoes_coordenada =  texto_editar_opcoes.get_rect(center=botao_editar.center)
    texto_fonte_menos_coordenada =  texto_fonte_menos.get_rect(center=botao_texto_menos.center)
    texto_fonte_mais_coordenada =  texto_fonte_mais.get_rect(center=botao_texto_fonte_mais.center)

    texto_tamanho_atual_fonte_coordenada = texto_tamanho_atual_fonte.get_rect(center=caixa_fonte_tamanho.center)

    tela.blit(texto_arquivo_opcoes, texto_arquivo_opcoes_coordenada)
    tela.blit(texto_editar_opcoes, texto_editar_opcoes_coordenada)
    tela.blit(texto_fonte_menos, texto_fonte_menos_coordenada)
    tela.blit(texto_fonte_mais, texto_fonte_mais_coordenada)
    tela.blit(texto_tamanho_atual_fonte, texto_tamanho_atual_fonte_coordenada)

def desenhar_botoes():
    posicao_mouse = pygame.mouse.get_pos()

    cor_botao_arquivo = cor_botao_editar = cor_fonte_menos = cor_fonte_mais = cor_fundo_caixa_tamanho_fonte = "white"

    #Criando os rects dos botoes
    botao_arquivo = pygame.Rect(0, 10, 70, 20)
    botao_editar = pygame.Rect(70, 10, 70, 20)
    botao_texto_menos = pygame.Rect(200, 5, 25, 25)
    caixa_fonte_tamanho = pygame.Rect(230, 6, 25, 25)
    borda_caixa_fonte_tamanho = pygame.Rect(230, 6, 25, 25)
    botao_texto_fonte_mais = pygame.Rect(265, 5, 25, 25) #Sinal de +

    if botao_arquivo.collidepoint(posicao_mouse):
        cor_botao_arquivo = (229, 241, 251)
    if botao_editar.collidepoint(posicao_mouse):
        cor_botao_editar = (229, 241, 251)
    if botao_texto_menos.collidepoint(posicao_mouse):
        cor_fonte_menos = (229, 241, 251)
    if botao_texto_fonte_mais.collidepoint(posicao_mouse):
        cor_fonte_mais = (229, 241, 251)
    if caixa_fonte_tamanho.collidepoint(posicao_mouse):
        cor_fundo_caixa_tamanho_fonte = (229, 241, 251)

    pygame.draw.rect(tela, cor_botao_arquivo, botao_arquivo)
    pygame.draw.rect(tela, cor_botao_editar, botao_editar)
    pygame.draw.rect(tela, cor_fonte_menos, botao_texto_menos)
    pygame.draw.rect(tela, cor_fonte_mais, botao_texto_fonte_mais)
    pygame.draw.rect(tela, cor_fundo_caixa_tamanho_fonte, caixa_fonte_tamanho) 
    pygame.draw.rect(tela, "gray", borda_caixa_fonte_tamanho, 1) #Borda caixa

    return botao_arquivo, botao_editar, botao_texto_fonte_mais, botao_texto_menos, caixa_fonte_tamanho

def desenhar_menu_opcoes():
    #Tamanho e posicao sombra = (5, 40, 200, 145)
    for i in range(5):
        sombra_menu_opcoes = pygame.Surface((200 + 2 * i, 145 + 2 * i), pygame.SRCALPHA)
        sombra_menu_opcoes.fill((0,0,0,15))
        tela.blit(sombra_menu_opcoes, (3, 38))

    botao_novo_arquivo = pygame.Rect(0, 30, 200, 30)
    botao_abrir_arquivo = pygame.Rect(0, 50, 200, 30)
    botao_salvar_arquivo = pygame.Rect(0, 70, 200, 30)
    
    pygame.draw.rect(tela, "#DDD4D4", menu_opcoes)
    
    #--------- Desenhar Botões --------
    pygame.draw.rect(tela, "#DDD4D4", botao_novo_arquivo)
    texto_botao_novo_arquivo =  fonte_menu.render("Novo        Ctrl + n", True, "black")
    coordenada_texto_botao_novo_arquivo = texto_botao_novo_arquivo.get_rect(center=botao_novo_arquivo.center)
    tela.blit(texto_botao_novo_arquivo, coordenada_texto_botao_novo_arquivo)

    pygame.draw.rect(tela, "#DDD4D4", botao_abrir_arquivo)
    texto_botao_abrir_arquivo =  fonte_menu.render("Abrir...    Ctrl + O", True, "black")
    coordenada_texto_abrir_arquivo = texto_botao_abrir_arquivo.get_rect(center=botao_abrir_arquivo.center)
    tela.blit(texto_botao_abrir_arquivo, coordenada_texto_abrir_arquivo)

    pygame.draw.rect(tela, "#DDD4D4", botao_salvar_arquivo)
    texto_botao_salvar_arquivo =  fonte_menu.render("Salvar...   Ctrl + S", True, "black")
    coordenada_texto_salvar_arquivo = texto_botao_salvar_arquivo.get_rect(center=botao_salvar_arquivo.center)
    tela.blit(texto_botao_salvar_arquivo, coordenada_texto_salvar_arquivo)

def escrever(letra):
    linhas[linha_atual]["texto"] += letra

def mexer_cursor(numero_seta, fonte, linha_atual, onde_digitar, y_distancia):
    cima = 1073741906
    baixo = 1073741905
    direita = 1073741903
    esquerda = 1073741904

    print(onde_digitar, largura_texto)
    
    if numero_seta == esquerda:
        cursor_y = y_distancia - fonte.get_height()
        cursor_x = (onde_digitar.x + largura_texto) - fonte.size("A")[0]
    if numero_seta == direita:
        cursor_y = y_distancia - fonte.get_height()
        cursor_x = (onde_digitar.x + largura_texto) + fonte.size("A")[0]

    return cursor_x, cursor_y, onde_digitar

# loop principal
rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                #linhas.insert(linha_atual+1, "")
                linhas.append({
                    "texto": ""
                })
                linha_atual += 1
            elif event.key == pygame.K_BACKSPACE: #Apagar
                #linhas[linha_atual]["texto"]= linhas[linha_atual]["texto"][:-1] 
                segurou_excluir = True
            else:
                if event.key != pygame.K_LSHIFT and event.key != pygame.K_RSHIFT:
                    tempo_que_letra_clicada = pygame.time.get_ticks()
                    segurou = True
                    letra = event.unicode
                if event.key == pygame.K_BACKSPACE:
                    tempo_botao_excluir_clicado = pygame.time.get_ticks()
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    cursor_automatico = False
                    numero_seta = event.key
                    print(event.key)
                #linhas[linha_atual]["texto"] += event.unicode
        if event.type == pygame.KEYUP:
            segurou = False
            escreveu_primeira_letra = False
            segurou_excluir = False
            excluiu_primeira_vez =False
            primeira_vez_segurando_tecla  = False
            tempo_que_letra_foi_solta = pygame.time.get_ticks()
            tempo_backspace_solto = pygame.time.get_ticks()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if botao_texto_menos.collidepoint(posicao_mouse):
                if tamanho_fonte_texto > 12:
                    tamanho_fonte_texto -= 1
                    fonte_texto = pygame.font.SysFont('consolas', tamanho_fonte_texto) #Atualiza a fonte
            if botao_texto_fonte_mais.collidepoint(posicao_mouse):
                if tamanho_fonte_texto < 120:
                    tamanho_fonte_texto += 1
                    fonte_texto = pygame.font.SysFont('consolas', tamanho_fonte_texto) #Atualiza a fonte
            if botao_arquivo.collidepoint(posicao_mouse):
                botoes_do_menu_aparecer = not botoes_do_menu_aparecer
                print(botoes_do_menu_aparecer)
                abriu_menu_primeira_vez = True
            if mouse_encima_do_menu_de_opcoes == False and botoes_do_menu_aparecer == True and abriu_menu_primeira_vez == False:
                botoes_do_menu_aparecer = False
                mouse_encima_do_menu_de_opcoes = False
            

    fonte_texto = pygame.font.SysFont('consolas', tamanho_fonte_texto) #Atualiza a fonte
    posicao_mouse = pygame.mouse.get_pos()

    tela.fill("white")  
    linha = pygame.draw.line(tela, ("gray"), (0, 30), (LARGURA, 30), 1)

    botao_arquivo, botao_editar, botao_texto_fonte_mais, botao_texto_menos, caixa_fonte_tamanho = desenhar_botoes()
    desenhar_texto()

    pygame.draw.rect(tela, "white", onde_digitar) 

    y_distancia = onde_digitar.y #Serve pra criar a distancia de cada

    tempo_atual = pygame.time.get_ticks() #Pega o tick atual

    if segurou:
        if not escreveu_primeira_letra:
            linhas[linha_atual]["texto"] += letra
            escreveu_primeira_letra = True
        if (tempo_atual - tempo_que_letra_clicada >= 500):
            if not primeira_vez_segurando_tecla :
                tempo_ultima_letra_modificada = pygame.time.get_ticks()
                linhas[linha_atual]["texto"] += letra
                primeira_vez_segurando_tecla = True
            else:
                if (tempo_atual - tempo_ultima_letra_modificada >= 50):
                    tempo_ultima_letra_modificada = pygame.time.get_ticks()
                    linhas[linha_atual]["texto"] += letra
            #escrever(letra)
    if segurou_excluir:
        if len(linhas[linha_atual]["texto"]) == 0:
            if(linha_atual != 0) and not linha_vazia:
                mudar_linha_apagar = False
                tempo_botao_excluir_clicado = pygame.time.get_ticks()
                segurou_excluir = False
                linha_vazia = True
            elif linha_vazia:
                print("linha final ", len(linhas[linha_atual]["texto"]))
                linhas.pop(linha_atual) #Exclui a linha
                linha_atual -= 1
                linha_vazia = False
            #if not mudar_linha_apagar:
                #mudar_linha_apagar = True
                #segurou_excluir = False
        else:
            if not excluiu_primeira_vez:
                excluiu_primeira_vez = True
                linhas[linha_atual]["texto"]= linhas[linha_atual]["texto"][:-1]
            if (tempo_atual - tempo_backspace_solto >= 700):
                if not primeira_vez_segurando_tecla :
                    tempo_ultima_letra_modificada  = pygame.time.get_ticks()
                    linhas[linha_atual]["texto"]= linhas[linha_atual]["texto"][:-1]
                    primeira_vez_segurando_tecla = True
                else:
                    if (tempo_atual - tempo_ultima_letra_modificada  >= 50):
                        tempo_ultima_letra_modificada  = pygame.time.get_ticks()
                        linhas[linha_atual]["texto"]= linhas[linha_atual]["texto"][:-1]

    for linha in linhas:
        texto_surface = fonte_texto.render(linha["texto"], True, "black")
        tela.blit(texto_surface, (onde_digitar.x, y_distancia))
        y_distancia += fonte_texto.get_height()

    largura_texto, altura_texto = fonte_texto.size(linhas[linha_atual]["texto"])

    if cursor_automatico:
        cursor_y = y_distancia - fonte_texto.get_height()
        cursor_x = onde_digitar.x + largura_texto
    else:
        cursor_x, cursor_y, onde_digitar = mexer_cursor(numero_seta, fonte_texto, linhas[linha_atual]["texto"], onde_digitar, y_distancia)

    if piscou == False:
        if tempo_atual - tempo_desligado >= tempo_piscada:
            cor_piscada = "black"
            piscou = True
            tempo_desligado = tempo_atual
    else:
        if tempo_atual - tempo_desligado >= tempo_piscada:
            cor_piscada = "white"
            piscou = False
            tempo_desligado = tempo_atual
    linha_texto = pygame.draw.line(tela, cor_piscada, (cursor_x, cursor_y), (cursor_x, cursor_y + fonte_texto.get_height()), 2)

    
    if botoes_do_menu_aparecer:
        desenhar_menu_opcoes()
        if menu_opcoes.collidepoint(posicao_mouse):
            mouse_encima_do_menu_de_opcoes = True
            abriu_menu_primeira_vez = False
        else:
            mouse_encima_do_menu_de_opcoes = False
            abriu_menu_primeira_vez = False
    

    pygame.display.flip()   # atualiza a tela

pygame.quit()
sys.exit()