import pygame
import sys

# inicia o pygame
pygame.init()

# cria a janela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Bloco de Notas")

fonte_menu = pygame.font.Font(None, 18)

def desenhar_texto():
    #Criando texto botoes
    texto_arquivo_opcoes =  fonte_menu.render("Menu", True, "black")
    texto_editar_opcoes =  fonte_menu.render("Editar", True, "black")
    texto_formatar_opcoes =  fonte_menu.render("Formatar", True, "black")
    texto_exibir_opcoes =  fonte_menu.render("Exibir", True, "black")

    #Centralizar texto nos botoes
    texto_arquivo_opcoes_coordenada =  texto_arquivo_opcoes.get_rect(center=botao_arquivo.center)
    texto_editar_opcoes_coordenada =  texto_editar_opcoes.get_rect(center=botao_editar.center)
    texto_formatar_opcoes_coordenada =  texto_formatar_opcoes.get_rect(center=botao_formatar.center)
    texto_exibir_opcoes_coordenada =  texto_exibir_opcoes.get_rect(center=botao_exibir.center)

    tela.blit(texto_arquivo_opcoes, texto_arquivo_opcoes_coordenada)
    tela.blit(texto_editar_opcoes, texto_editar_opcoes_coordenada)
    tela.blit(texto_formatar_opcoes, texto_formatar_opcoes_coordenada)
    tela.blit(texto_exibir_opcoes, texto_exibir_opcoes_coordenada)

def desenhar_botoes():
    posicao_mouse = pygame.mouse.get_pos()

    cor_botao_arquivo = cor_botao_editar = cor_botao_formatar = cor_botao_exibir = "white"

    #Criando os rects dos botoes
    botao_arquivo = pygame.Rect(0, 10, 70, 20)
    botao_editar = pygame.Rect(70, 10, 70, 20)
    botao_formatar = pygame.Rect(140, 10, 70, 20)
    botao_exibir = pygame.Rect(210, 10, 70, 20)

    if botao_arquivo.collidepoint(posicao_mouse):
        cor_botao_arquivo = (229, 241, 251)
    if botao_editar.collidepoint(posicao_mouse):
        cor_botao_editar = (229, 241, 251)
    if botao_formatar.collidepoint(posicao_mouse):
        cor_botao_formatar = (229, 241, 251)
    if botao_exibir.collidepoint(posicao_mouse):
        cor_botao_exibir = (229, 241, 251)

    pygame.draw.rect(tela, cor_botao_arquivo, botao_arquivo)
    pygame.draw.rect(tela, cor_botao_editar, botao_editar)
    pygame.draw.rect(tela, cor_botao_formatar, botao_formatar)
    pygame.draw.rect(tela, cor_botao_exibir, botao_exibir)

    return botao_arquivo, botao_editar, botao_exibir, botao_formatar

# loop principal
rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    posicao_mouse = pygame.mouse.get_pos()

    tela.fill("white")  
    linha = pygame.draw.line(tela, ("gray"), (0, 30), (LARGURA, 30), 2)

    botao_arquivo, botao_editar, botao_formatar, botao_exibir = desenhar_botoes()
    desenhar_texto()

    pygame.display.flip()   # atualiza a tela

pygame.quit()
sys.exit()
