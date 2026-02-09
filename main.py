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


tamanho_fonte_texto = 15
tamanho_fonte_aumentar_dominuir = 28

fonte_menu = pygame.font.SysFont('arial', 15)
fonte_texto = pygame.font.SysFont('arial', tamanho_fonte_texto)
fonte_botao_menos_mais = pygame.font.SysFont('arial', tamanho_fonte_aumentar_dominuir)
fonte_sinal_mais = pygame.font.SysFont('arial', 19) #O sinal de + é muito grande

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

tempo_que_letra_foi_solta = 0

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

def escrever(letra):
    linhas[linha_atual]["texto"] += letra

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
            elif event.key == pygame.K_BACKSPACE:
                linhas[linha_atual]["texto"]= linhas[linha_atual]["texto"][:-1] 
            else:
                tempo_que_letra_clicada = pygame.time.get_ticks()
                segurou = True
                letra = event.unicode
                #linhas[linha_atual]["texto"] += event.unicode
        if event.type == pygame.KEYUP:
            segurou = False
            escreveu_primeira_letra = False
            tempo_que_letra_foi_solta = pygame.time.get_ticks()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if botao_texto_menos.collidepoint(posicao_mouse):
                tamanho_fonte_texto -= 1
                fonte_texto = pygame.font.SysFont('arial', tamanho_fonte_texto) #Atualiza a fonte
            if botao_texto_fonte_mais.collidepoint(posicao_mouse):
                tamanho_fonte_texto += 1
                fonte_texto = pygame.font.SysFont('arial', tamanho_fonte_texto) #Atualiza a fonte

    fonte_texto = pygame.font.SysFont('arial', tamanho_fonte_texto) #Atualiza a fonte
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
            escrever(letra)

    for linha in linhas:
        texto_surface = fonte_texto.render(linha["texto"], True, "black")
        tela.blit(texto_surface, (onde_digitar.x, y_distancia))
        y_distancia += fonte_texto.get_height()

    cursor_y = y_distancia - fonte_texto.get_height()
    largura_texto, altura_texto = fonte_texto.size(linhas[linha_atual]["texto"])
    cursor_x = onde_digitar.x + largura_texto

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
    

    pygame.display.flip()   # atualiza a tela

pygame.quit()
sys.exit()
