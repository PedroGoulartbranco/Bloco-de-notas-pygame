import pygame
import sys
from tkinter import filedialog
import os 
from fpdf import FPDF
from pypdf import PdfReader

pygame.init()

# cria a janela
LARGURA, ALTURA = 1000, 600
nome_arquivo = tipo_arquivo = None
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("PedroNote")
clock = pygame.time.Clock()
cor_principal_geral = "white"
cor_botoes_geral = "white"
cor_fonte_geral = "black"
cor_botoes_complementares = "#E0E0E0"
mudancas = False
pode_mexer = True
arquivo_atual = None
texto_surface = None

#icones
icone = pygame.image.load("img/icon.ico")
icone = pygame.transform.scale(icone, (256, 256))
pygame.display.set_icon(icone)


tamanho_fonte_texto = 22
tamanho_fonte_aumentar_dominuir = 28
fonte_atual = 'ARIAL.TTF'

PASTA_ATUAL = os.path.dirname(__file__)
caminho_fonte_texto = os.path.join(PASTA_ATUAL, "fonts", fonte_atual)

fonte_menu = pygame.font.SysFont('consolas', 15)
fonte_botoes_opcoes_menu = pygame.font.SysFont('consolas', 13)
fonte_texto = pygame.font.Font(caminho_fonte_texto, tamanho_fonte_texto)
fonte_botao_menos_mais = pygame.font.SysFont('consolas', tamanho_fonte_aumentar_dominuir)
fonte_sinal_mais = pygame.font.SysFont('consolas', 19) #O sinal de + é muito grande

cor_fonte_botao = "black"

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

mostrar_janela_sair_salvar = False
clicou_no_botao_novo = False

tempo_que_letra_foi_solta = 0
tempo_backspace_solto = 0

botoes_do_menu_aparecer = False
menu_opcoes = pygame.Rect(0, 30, 250, 150) #Criei essa variavel para ser global e conseguir usar no IF do loop de eventos
mouse_encima_do_menu_de_opcoes = False
abriu_menu_primeira_vez = False #Para nao fechar automaticamente quando fecha 
botao_novo_arquivo = botao_abrir_arquivo = botao_salvar_arquivo = pygame.Rect(0, 35, 200, 20) #Rect provisorio só para usar no loop de eventos
botao_salvar = botao_nao_salvar = botao_cancelar = botao_X_sair = pygame.Rect(0, 35, 200, 20) #Rect provisorio só para usar no loop de eventos

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
    posicao_mouse = pygame.mouse.get_pos()

    for i in range(5):
        sombra_menu_opcoes = pygame.Surface((200 + 2 * i, 145 + 2 * i), pygame.SRCALPHA)
        sombra_menu_opcoes.fill((0,0,0,15))
        tela.blit(sombra_menu_opcoes, (3, 38))

    cor_botao_novo = cor_botao_abrir = cor_botao_salvar = cor_botao_salvar_como = "#F8EDED"

    botao_novo_arquivo = pygame.Rect(0, 35, 200, 20)
    botao_abrir_arquivo = pygame.Rect(0, 55, 200, 20)
    botao_salvar_arquivo = pygame.Rect(0, 75, 200, 20)
    botao_salvar_arquivo_como = pygame.Rect(0, 95, 200, 20)
    
    pygame.draw.rect(tela, "#F8EDED", menu_opcoes)

    if botao_novo_arquivo.collidepoint(posicao_mouse):
        cor_botao_novo = (229, 241, 251)
    if botao_abrir_arquivo.collidepoint(posicao_mouse):
        cor_botao_abrir = (229, 241, 251)
    if botao_salvar_arquivo.collidepoint(posicao_mouse):
        cor_botao_salvar = (229, 241, 251)
    if botao_salvar_arquivo_como.collidepoint(posicao_mouse):
        cor_botao_salvar_como = (229, 241, 251)

    #--------- Desenhar Botões --------
    pygame.draw.rect(tela, cor_botao_novo, botao_novo_arquivo)
    texto_botao_novo_arquivo =  fonte_botoes_opcoes_menu.render("Novo                 Ctrl + n", True, "black")
    coordenada_texto_botao_novo_arquivo = texto_botao_novo_arquivo.get_rect(midleft=botao_novo_arquivo.midleft)
    coordenada_texto_botao_novo_arquivo.x += 10
    tela.blit(texto_botao_novo_arquivo, coordenada_texto_botao_novo_arquivo)

    pygame.draw.rect(tela, cor_botao_abrir, botao_abrir_arquivo)
    texto_botao_abrir_arquivo =  fonte_botoes_opcoes_menu.render("Abrir...             Ctrl + O", True, "black")
    coordenada_texto_abrir_arquivo = texto_botao_abrir_arquivo.get_rect(midleft=botao_abrir_arquivo.midleft)
    coordenada_texto_abrir_arquivo.x += 10
    tela.blit(texto_botao_abrir_arquivo, coordenada_texto_abrir_arquivo)

    pygame.draw.rect(tela, cor_botao_salvar, botao_salvar_arquivo)
    texto_botao_salvar_arquivo =  fonte_botoes_opcoes_menu.render("Salvar               Ctrl + S", True, "black")
    coordenada_texto_salvar_arquivo = texto_botao_salvar_arquivo.get_rect(midleft=botao_salvar_arquivo.midleft)
    coordenada_texto_salvar_arquivo.x += 10
    tela.blit(texto_botao_salvar_arquivo, coordenada_texto_salvar_arquivo)

    pygame.draw.rect(tela, cor_botao_salvar_como, botao_salvar_arquivo_como)
    texto_botao_salvar_arquivo_como =  fonte_botoes_opcoes_menu.render("Salvar Como...   Ctrl + Shift + S", True, "black")
    coordenada_texto_salvar_arquivo_como = texto_botao_salvar_arquivo_como.get_rect(midleft=botao_salvar_arquivo_como.midleft)
    coordenada_texto_salvar_arquivo_como.x += 10
    tela.blit(texto_botao_salvar_arquivo_como, coordenada_texto_salvar_arquivo_como)

    return botao_novo_arquivo, botao_abrir_arquivo, botao_salvar_arquivo, botao_salvar_arquivo_como

def escrever(letra):
    linhas[linha_atual]["texto"] += letra

def mexer_cursor(numero_seta, fonte, linha_atual, onde_digitar, y_distancia):
    cima = 1073741906
    baixo = 1073741905
    direita = 1073741903
    esquerda = 1073741904
    
    if numero_seta == esquerda:
        cursor_y = y_distancia - fonte.get_height()
        cursor_x = (onde_digitar.x + largura_texto) - fonte.size("A")[0]
    if numero_seta == direita:
        cursor_y = y_distancia - fonte.get_height()
        cursor_x = (onde_digitar.x + largura_texto) + fonte.size("A")[0]

    return cursor_x, cursor_y, onde_digitar

def pular_linha(linhas, linha_atual):
    linhas.append({
        "texto": ""
    })
    linha_atual += 1
    return linhas, linha_atual

def verificar_se_ta_vazio():
    global linhas
    vazio = False
    for linha_for in linhas:
        numero_caracteres = len(linha_for['texto'])
        if numero_caracteres > 0:
            vazio = False
            break
        else:
            vazio = True
    return vazio

def decidir_cor_linha():
    global cor_principal_geral
    if (cor_principal_geral != "black"):
        return "gray"
    return "white"

def criar_janela_de_saida():
    global cor_principal_geral, cor_botoes_geral, cor_fonte_geral
    posicao_mouse = pygame.mouse.get_pos()
    cor_janela = cor_principal_geral
    cor_linha = decidir_cor_linha()

    janela_sair = pygame.Rect(300, 150, 400, 100)

    texto_na_janela_sair = fonte_menu.render("Deseja Salvar As Alterações ?", True, cor_fonte_geral)
    texto_titulo_janela_sair = fonte_menu.render("PedroNote", True, cor_fonte_geral)
    coordenada_texto_titulo_janela_sair = (310, 155)
    coordenada_texto_botao_janela_sair = (310, 180) 

    for i in range(7):
        sombra_janela_sair = pygame.Surface((400 + 2 * i, 100 + 2 * i), pygame.SRCALPHA)
        sombra_janela_sair.fill((0,0,0,30))
        tela.blit(sombra_janela_sair, (300 - i, 150 - i))

    pygame.draw.rect(tela, cor_janela, janela_sair)

    tela.blit(texto_titulo_janela_sair, coordenada_texto_titulo_janela_sair )
    pygame.draw.line(tela, cor_linha, (300, 170), (700, 170), 1)
    pygame.draw.line(tela, cor_linha, (300, 220), (700, 220), 1)

    tela.blit(texto_na_janela_sair, coordenada_texto_botao_janela_sair)
    botao_salvar, botao_nao_salvar, botao_cancelar, botao_X_sair = criar_botoes_sair_salvar_janela()
    return botao_salvar, botao_nao_salvar, botao_cancelar, botao_X_sair

def criar_botoes_sair_salvar_janela():
    global cor_botoes_geral, cor_principal_geral, cor_botoes_complementares, arquivo_atual
    posicao_mouse = pygame.mouse.get_pos()
    cor_botao_salvar = cor_botao_nao_salvar = cor_botao_cancelar = cor_botoes_complementares
    cor_botao_X = cor_botoes_geral

    
    botao_salvar = pygame.Rect(380, 225, 90, 20)
    botao_nao_salvar = pygame.Rect(480, 225, 100, 20)
    botao_cancelar = pygame.Rect(590, 225, 100, 20)
    botao_X_sair = pygame.Rect(680, 150, 20, 20) #Botao X

    texto_botao_salvar = fonte_menu.render("Salvar", True, cor_fonte_geral)
    texto_botao_nao_salvar = fonte_menu.render("Não Salvar", True, cor_fonte_geral)
    texto_botao_cancelar = fonte_menu.render("Cancelar", True, cor_fonte_geral)
    texto_botao_X = fonte_menu.render("X", True, cor_fonte_geral)

    coordenada_texto_botao_salvar = texto_botao_salvar.get_rect(center=botao_salvar.center)
    coordenada_texto_botao_nao_salvar = texto_botao_nao_salvar.get_rect(center=botao_nao_salvar.center)
    coordenada_texto_botao_cancelar = texto_botao_cancelar.get_rect(center=botao_cancelar.center)
    coordenada_texto_botao_X = texto_botao_X.get_rect(center=botao_X_sair.center)

    if botao_salvar.collidepoint(posicao_mouse):
        cor_botao_salvar = (229, 241, 251)
    if botao_nao_salvar.collidepoint(posicao_mouse):
        cor_botao_nao_salvar = (229, 241, 251)
    if botao_cancelar.collidepoint(posicao_mouse):
        cor_botao_cancelar = (229, 241, 251)
    if botao_X_sair.collidepoint(posicao_mouse):
        cor_botao_X = "#F00A0A"

    pygame.draw.rect(tela, cor_botao_salvar, botao_salvar)
    pygame.draw.rect(tela, cor_botao_nao_salvar, botao_nao_salvar)
    pygame.draw.rect(tela, cor_botao_cancelar, botao_cancelar)
    pygame.draw.rect(tela, cor_botao_X, botao_X_sair)

    tela.blit(texto_botao_salvar, coordenada_texto_botao_salvar)
    tela.blit(texto_botao_nao_salvar, coordenada_texto_botao_nao_salvar)
    tela.blit(texto_botao_cancelar, coordenada_texto_botao_cancelar)
    tela.blit(texto_botao_X, coordenada_texto_botao_X)

    return  botao_salvar, botao_nao_salvar, botao_cancelar, botao_X_sair

def salvar():
    global arquivo_atual, nome_arquivo, tamanho_fonte_texto, clicou_no_botao_novo
    mostrar_janela_sair_salvar = True
    if arquivo_atual == None:
        caminho = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivos de texto", "*.txt"), ("Arquivo PDFs", "*.pdf")],
            title="Escolha onde salvar seu arquivo"
        )
        arquivo_atual = caminho
        if not clicou_no_botao_novo:
            nome_arquivo = os.path.basename(arquivo_atual)
    if arquivo_atual:
        _ , tipo_arquivo = os.path.splitext(arquivo_atual)
        tipo_arquivo = tipo_arquivo.lower()
        if tipo_arquivo == ".txt":
            mostrar_janela_sair_salvar = salvar_txt(arquivo_atual, linhas)
        if tipo_arquivo == ".pdf":
            mostrar_janela_sair_salvar = salvar_pdf(arquivo_atual, linhas, tamanho_fonte_texto)
    return mostrar_janela_sair_salvar

def salvar_txt(arquivo_atual, linhas_arquivo):
    with open(arquivo_atual, 'w', encoding='utf-8') as arquivo:
            for linha in linhas_arquivo:
                arquivo.write(f'{linha["texto"]}\n')
    return False

def salvar_pdf(caminho, linhas_arquivo, tamanho_fonte):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15) #Quando chega perto do final da folha ele cria uma nova pagina
    pdf.add_page()
    pdf.set_margins(10, 10, 10)

    pasta_fontes = os.path.join(os.path.dirname(__file__), "fonts")
    pdf.add_font("Arial", "", os.path.join(pasta_fontes, "ARIAL.TTF"))

    pdf.set_char_spacing(0)
    largura_para_texto = pdf.epw
    pdf.set_font('Arial', size=tamanho_fonte)
    altura_linha = (tamanho_fonte / 2) - 1.5
    texto_completo = ""
    for linha in linhas_arquivo:
        linha_agora = ""
        if linha["texto"] == "":
            linha_agora += " "
        else:
            linha_agora += linha["texto"]
        texto_completo += linha_agora + "\n"
    pdf.multi_cell(w=0, h=altura_linha, text=texto_completo)
    pdf.output(caminho)

def abrir():
    global arquivo_atual, nome_arquivo, tipo_arquivo
    caminho = filedialog.askopenfilename(
        title="Selecione um arquivo",
        filetypes=(("Arquivos de Texto", "*.txt"), ("Documentos PDF", "*.pdf*"))
    )
    arquivo_atual , tipo_arquivo = os.path.splitext(caminho)
    tipo_arquivo = tipo_arquivo.lower()
    nome_arquivo = os.path.basename(arquivo_atual)
    ler_arquivo(caminho, tipo_arquivo)
    
    return False

def ler_arquivo(arquivo_atual, tipo_arquivo):
    if tipo_arquivo == ".txt":
        ler_arquivo_txt(arquivo_atual)
    if tipo_arquivo == '.pdf':
        ler_arquivo_pdf(arquivo_atual)

def ler_arquivo_txt(caminho):
    global linhas, linha_atual
    linha_atual = 0
    print(caminho)
    limpar_texto()
    with open(caminho, 'r') as arquivo:
        linhas_arquivo = arquivo.readlines()
    for l in linhas_arquivo:
        linha_atual_arquivo = ""
        for indice, caracter in enumerate(l):
            print(caracter)
            if caracter != "\n":
                linha_atual_arquivo += caracter
                linhas[linha_atual]["texto"] = linha_atual_arquivo
            else:
                linha_atual += 1
                linhas.append({
                "texto": f""
                })

def ler_arquivo_pdf(caminho):
    global linhas, linha_atual
    leitor = PdfReader(caminho)
    texto = ""
    for pagina in leitor.pages:
        texto += pagina.extract_text()
    linha_atual = 0
    for linha in texto:
        if linha != "\n":
            linhas[linha_atual]["texto"] += linha
        else:
            linha_atual += 1
            linhas.append({
                "texto": f""
                })

def limpar_texto():
    global linhas
    linhas = [
        {"texto": ""}
    ]

rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if not mudancas:
                rodando = False
            else:
                mostrar_janela_sair_salvar = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                #linhas.insert(linha_atual+1, "")
                if pode_mexer:
                    linhas, linha_atual = pular_linha(linhas, linha_atual)
            elif event.key == pygame.K_BACKSPACE: #Apagar
                #linhas[linha_atual]["texto"]= linhas[linha_atual]["texto"][:-1] 
                if pode_mexer:
                    segurou_excluir = True
            else:
                if pode_mexer:
                    if event.key != pygame.K_LSHIFT and event.key != pygame.K_RSHIFT:
                        tempo_que_letra_clicada = pygame.time.get_ticks()
                        segurou = True
                        letra = event.unicode
                    if event.key == pygame.K_BACKSPACE:
                        tempo_botao_excluir_clicado = pygame.time.get_ticks()
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        cursor_automatico = False
                        numero_seta = event.key
                #linhas[linha_atual]["texto"] += event.unicode
        if event.type == pygame.KEYUP:
            if pode_mexer:
                segurou = False
                escreveu_primeira_letra = False
                segurou_excluir = False
                excluiu_primeira_vez =False
                primeira_vez_segurando_tecla  = False
                tempo_que_letra_foi_solta = pygame.time.get_ticks()
                tempo_backspace_solto = pygame.time.get_ticks()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mostrar_janela_sair_salvar:
                if botao_salvar.collidepoint(posicao_mouse):
                        mostrar_janela_sair_salvar = salvar()
                        if clicou_no_botao_novo:
                            limpar_texto()
                            clicou_no_botao_novo = False
                            arquivo_atual = None
                            mostrar_janela_sair_salvar = False
                if botao_nao_salvar.collidepoint(posicao_mouse):
                    if clicou_no_botao_novo:
                        limpar_texto()
                        mostrar_janela_sair_salvar = False
                        arquivo_atual = None
                    else:
                        rodando = False
                if botao_cancelar.collidepoint(posicao_mouse) or botao_X_sair.collidepoint(posicao_mouse):
                    mostrar_janela_sair_salvar = False
            if pode_mexer:
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
                    abriu_menu_primeira_vez = True
                if mouse_encima_do_menu_de_opcoes == False and botoes_do_menu_aparecer == True and abriu_menu_primeira_vez == False:
                    botoes_do_menu_aparecer = False
                    mouse_encima_do_menu_de_opcoes = False
                if botoes_do_menu_aparecer:
                    esta_vazio = verificar_se_ta_vazio()
                    if botao_novo_arquivo.collidepoint(posicao_mouse):
                        if esta_vazio:
                            botoes_do_menu_aparecer = False
                            mouse_encima_do_menu_de_opcoes = False
                        else:
                            clicou_no_botao_novo = True
                            mostrar_janela_sair_salvar = True
                    if botao_salvar_arquivo.collidepoint(posicao_mouse):
                        if esta_vazio:
                            botoes_do_menu_aparecer = False
                            mouse_encima_do_menu_de_opcoes = False
                        else:
                            botoes_do_menu_aparecer = salvar()
                    if botao_abrir_arquivo.collidepoint(posicao_mouse):
                        botoes_do_menu_aparecer = abrir()
    if nome_arquivo != None:
        pygame.display.set_caption(f"{nome_arquivo:.30} - PedroNote")
    fonte_texto = pygame.font.Font(caminho_fonte_texto, tamanho_fonte_texto)#Atualiza a fonte
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
            if cursor_x >= 970:
                linhas, linha_atual = pular_linha(linhas, linha_atual)
            linhas[linha_atual]["texto"] += letra
            escreveu_primeira_letra = True
        if (tempo_atual - tempo_que_letra_clicada >= 500):
            if not primeira_vez_segurando_tecla :
                if cursor_x >= 970:
                    linhas, linha_atual = pular_linha(linhas, linha_atual)
                tempo_ultima_letra_modificada = pygame.time.get_ticks()
                linhas[linha_atual]["texto"] += letra
                primeira_vez_segurando_tecla = True
            else:
                if (tempo_atual - tempo_ultima_letra_modificada >= 50):
                    if cursor_x >= 970:
                        linhas, linha_atual = pular_linha(linhas, linha_atual)
                    tempo_ultima_letra_modificada = pygame.time.get_ticks()
                    linhas[linha_atual]["texto"] += letra
    if segurou_excluir:
        if len(linhas[linha_atual]["texto"]) == 0:
            if(linha_atual != 0) and not linha_vazia:
                mudar_linha_apagar = False
                tempo_botao_excluir_clicado = pygame.time.get_ticks()
                segurou_excluir = False
                linha_vazia = True
            elif linha_vazia:
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
        botao_novo_arquivo, botao_abrir_arquivo, botao_salvar_arquivo, botao_salvar_arquivo_como = desenhar_menu_opcoes()

        if menu_opcoes.collidepoint(posicao_mouse):
            mouse_encima_do_menu_de_opcoes = True
            abriu_menu_primeira_vez = False
        else:
            mouse_encima_do_menu_de_opcoes = False
            abriu_menu_primeira_vez = False
    if mostrar_janela_sair_salvar:
        pode_mexer = False
        botoes_do_menu_aparecer = False
        botao_salvar, botao_nao_salvar, botao_cancelar, botao_X_sair = criar_janela_de_saida()
    else:
        pode_mexer = True
    

    pygame.display.flip()   # atualiza a tela
    clock.tick(30) #Roda o loop 30 vezes por segundo

pygame.quit()
sys.exit()