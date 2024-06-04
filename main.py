from customtkinter import *
from tkinter import Canvas
from PIL import Image, ImageTk

# Definindo janela
app = CTk()
app.geometry("1200x676")
app.resizable(False,False)



# Carregar a imagem de fundo do menu e redimensionar
img_bg_menu = Image.open("assets/img/bg_menu.png").resize((1200, 676), Image.Resampling.LANCZOS)
img_bg_menu = ImageTk.PhotoImage(img_bg_menu)
canvas_menu = Canvas(app, width=1200, height=676)
canvas_menu.pack(fill="both", expand=True,anchor='center')
canvas_menu.create_image(0, 0, image=img_bg_menu, anchor=NW)


opcao = 0

if opcao == 1:
    # Carregar a imagem de fundo e redimensionar
    img_bg = Image.open("assets/img/bg.png").resize((1200, 676), Image.Resampling.LANCZOS)
    img_bg = ImageTk.PhotoImage(img_bg)

    ### CAMINHÃO | SPRITES
    # Carregar a imagem do caminhão INDO
    img_caminhao_indo = Image.open("assets/img/truck_l.png").resize((100, 100), Image.Resampling.LANCZOS)
    img_caminhao_indo = ImageTk.PhotoImage(img_caminhao_indo)
    # Carregar a imagem do caminhão VOLTANDO
    img_caminhao_vindo = Image.open("assets/img/truck_r.png").resize((100, 100), Image.Resampling.LANCZOS)
    img_caminhao_vindo = ImageTk.PhotoImage(img_caminhao_vindo)

    # Criar o canvas (div principal)
    canvas = Canvas(app, width=1200, height=676)
    canvas.pack(fill="both", expand=True,anchor='center')

    # Adicionar a imagem de fundo no canvas
    canvas.create_image(0, 0, image=img_bg, anchor=NW)
    caminhao_sprite_indo = canvas.create_image(70, 490, image=img_caminhao_indo, anchor=NW)
    caminhao_sprite_vindo = canvas.create_image(2000, 2000, image=img_caminhao_vindo, anchor=NW)

    ### SPRITES PILHAS DE CAIXAS
    # Carregar as imagens
    img_pilha_01 = Image.open("assets/img/box1.png").resize((50, 50), Image.Resampling.LANCZOS)
    img_pilha_01 = ImageTk.PhotoImage(img_pilha_01)
    sprite_pilha_01 = canvas.create_image(170, 305, image=img_pilha_01, anchor=NW)

    img_pilha_02 = Image.open("assets/img/box2.png").resize((50, 50), Image.Resampling.LANCZOS)
    img_pilha_02 = ImageTk.PhotoImage(img_pilha_02)
    sprite_pilha_02 = canvas.create_image(170, 355, image=img_pilha_02, anchor=NW)

    img_pilha_03 = Image.open("assets/img/box3.png").resize((50, 50), Image.Resampling.LANCZOS)
    img_pilha_03 = ImageTk.PhotoImage(img_pilha_03)
    sprite_pilha_03 = canvas.create_image(170, 405, image=img_pilha_03, anchor=NW)
    # definindo relação semantica entre as variaveis para poder animar (dicionário)
    cargas_e_pilhas = {'carga_1': sprite_pilha_01, 'carga_2': sprite_pilha_02, 'carga_3': sprite_pilha_03}

    # Variáveis para a posição x e y do caminhão
    caminhao_eixo_x = 70
    caminhao_eixo_y = 490
    cargas_no_caminhao = ['','']

    # Velocidade que ele se move
    velocidade = 15
    # PARADA PRINCIPAL ENCRUZILHADA
    posicao_x_encruzilhada = 680
    # PARADA PRINCIPAL DEPOSITO
    posicao_x_deposito = 130
    # TEMPOS PARADOS NAS PARADAS
    tempo_de_espera_casas = 1000  # 1s
    tempo_de_espera_deposito = 2500  # 5s
    tempo_de_espera_encruzilhada = 1000  # 3s
    # VARIAVEIS DE PAGE IN PAGE OUT ETC

    carga_meta_pacotes = 4
    carga_total_pacotes = 12
    carga_limite_pacotes = 4

    carga_in = 0
    carga_out = 0
    carga_fault = 0



    #### CRIANDO TEXTOS QUE APARECEM NA TELA
    ## UI | textos variáveis que NÃO vão ser atualizados (mas podem rs)
    ## unico que não atualiza é "LOGS" pois ta fixo na imagem de fundo
    tam_txt_UI = 8
    cor_txt_UI = 'white' # aceita hexcode
    font_txt_UI = 'Open Sans extrabold'
    texto_UI_DESCRICAO = canvas.create_text(720, 75, text="DESCRIÇÃO DA ROTA", font=(font_txt_UI, 13), fill=cor_txt_UI, tag="texto_ui_desc")

    texto_UI_LIMITE = canvas.create_text(200, 75, text="Limite Pacotes por Pilha", font=(font_txt_UI, tam_txt_UI), fill=cor_txt_UI, tag="texto_ui_limi")
    texto_UI_TOTAL = canvas.create_text(200, 121, text="Total Pacotes à Espera", font=(font_txt_UI, tam_txt_UI), fill=cor_txt_UI, tag="texto_ui_total")
    texto_UI_META = canvas.create_text(200, 166, text="Meta Entregas por Rota", font=(font_txt_UI, tam_txt_UI), fill=cor_txt_UI, tag="texto_ui_meta")

    texto_UI_PACOTE_FALTOU = canvas.create_text(409, 75, text="Pacote Faltou", font=(font_txt_UI, tam_txt_UI), fill=cor_txt_UI, tag="texto_ui_pac_falt")
    texto_UI_PACOTE_CARREG = canvas.create_text(406, 121, text="Pacote Carregado", font=(font_txt_UI, tam_txt_UI), fill=cor_txt_UI, tag="texto_ui_pac_carreg")
    texto_UI_PACOTE_DESCAR = canvas.create_text(406, 166, text="Pacote Descarregado", font=(font_txt_UI, tam_txt_UI), fill=cor_txt_UI, tag="texto_ui_pac_descar")

    ## VAR | textos variáveis que vão ser atualizados
    ## textos variáveis que vão ser atualizados
    tam_txt_VAR = 10
    cor_txt_VAR = 'deep pink' # aceita hexcode
    font_txt_VAR = 'Open Sans extrabold'
    texto_DESCRICAO = canvas.create_text(720, 135, text="", font=(font_txt_VAR, 17), fill=cor_txt_VAR, tag="texto_desc")
    texto_VAR_LIMITE = canvas.create_text(299, 75, text=carga_limite_pacotes, font=(font_txt_VAR, tam_txt_VAR), fill=cor_txt_VAR, tag="texto_var_limi")
    texto_VAR_TOTAL = canvas.create_text(299, 121, text=carga_total_pacotes, font=(font_txt_VAR, tam_txt_VAR), fill=cor_txt_VAR, tag="texto_var_total")
    texto_VAR_META = canvas.create_text(299, 166, text=carga_meta_pacotes, font=(font_txt_VAR, tam_txt_VAR), fill=cor_txt_VAR, tag="texto_var_meta")

    texto_VAR_PACOTE_FALTOU = canvas.create_text(508, 75, text=carga_fault, font=(font_txt_VAR, tam_txt_VAR), fill=cor_txt_VAR, tag="texto_var_pac_falt")
    texto_VAR_PACOTE_CARREG = canvas.create_text(508, 121, text=carga_in, font=(font_txt_VAR, tam_txt_VAR), fill=cor_txt_VAR, tag="texto_var_pac_carreg")
    texto_VAR_PACOTE_DESCAR = canvas.create_text(508, 166, text=carga_out, font=(font_txt_VAR, tam_txt_VAR), fill=cor_txt_VAR, tag="texto_var_pac_descar")

    texto_VAR_ROTA_PRANCHETA = canvas.create_text(1073, 135, text="    ROTA: \n"
                                                                "Endereço ? \n"
                                                                "Endereço ? \n"
                                                                "Endereço ? \n"
                                                                "Endereço ? \n", #aqui poderia gerar conforme endereços na list[] de rota
                                                            
                                                            font=(font_txt_VAR, 9), fill=cor_txt_VAR, tag="texto_var_rota")

    def print_truck_positions(): # para debugar
        print(f"Posição x: {caminhao_eixo_x} | Posição y: {caminhao_eixo_y}")
        app.after(50, print_truck_positions)

    def atualizar_texto(qual_texto, texto):
        canvas.itemconfig(qual_texto, text=texto)

    def mover_para_casa(posicao_x_da_casa, posicao_y_da_casa, callback, casa):
        global caminhao_eixo_x, caminhao_eixo_y, posicao_x_encruzilhada

        if caminhao_eixo_x < posicao_x_encruzilhada:
            caminhao_eixo_x += velocidade       

        if caminhao_eixo_y > posicao_y_da_casa and caminhao_eixo_x >= posicao_x_encruzilhada:
            caminhao_eixo_x = posicao_x_encruzilhada
            caminhao_eixo_y -= velocidade
            if caminhao_eixo_y - posicao_y_da_casa < 0:
                caminhao_eixo_y = posicao_y_da_casa

        if caminhao_eixo_x >= posicao_x_encruzilhada and caminhao_eixo_y <= posicao_y_da_casa:
            caminhao_eixo_x += velocidade

        # ajustar caixas a posicao nova x QUANDO CHEGA NA CASA
        if caminhao_eixo_x >= posicao_x_da_casa:
            conta_cargas = 0
            for carga in cargas_no_caminhao:
                if carga:
                    canvas.coords(cargas_e_pilhas[carga], caminhao_eixo_x-19, caminhao_eixo_y)
                    if conta_cargas > 0:
                        canvas.coords(cargas_e_pilhas[carga], caminhao_eixo_x+1, caminhao_eixo_y)
                    conta_cargas += 1
            atualizar_texto(texto_DESCRICAO,f"Chegou na {casa}")
            app.after(tempo_de_espera_casas, callback)
            return

        # Trocar a imagem para o caminhão indo
        canvas.coords(caminhao_sprite_vindo, 2000, 2000)
        canvas.coords(caminhao_sprite_indo, caminhao_eixo_x, caminhao_eixo_y)
        conta_cargas = 0
        for carga in cargas_no_caminhao:
            if carga:
                canvas.coords(cargas_e_pilhas[carga], caminhao_eixo_x, caminhao_eixo_y)
                if conta_cargas > 0:
                    canvas.coords(cargas_e_pilhas[carga], caminhao_eixo_x+20, caminhao_eixo_y)
                conta_cargas += 1
        app.after(50, lambda: mover_para_casa(posicao_x_da_casa, posicao_y_da_casa, callback, casa))

    def voltar_encruzilhada(callback):
        atualizar_texto(texto_DESCRICAO,"Indo para ENCRUZILHADA")
        global caminhao_eixo_x, caminhao_eixo_y, posicao_x_encruzilhada, posicao_x_deposito, tempo_de_espera_encruzilhada

        # Trocar a imagem para o caminhão voltando
        canvas.coords(caminhao_sprite_indo, 2000, 2000)
        canvas.coords(caminhao_sprite_vindo, caminhao_eixo_x, caminhao_eixo_y)

        if caminhao_eixo_x > 700:
            caminhao_eixo_x -= velocidade


        if caminhao_eixo_y < 490 and caminhao_eixo_x <= 700:
            caminhao_eixo_x = posicao_x_encruzilhada
            caminhao_eixo_y += velocidade
            conta_cargas = 0
            # alterando caixas
            for carga in cargas_no_caminhao:
                if carga:
                    canvas.coords(cargas_e_pilhas[carga], posicao_x_encruzilhada, caminhao_eixo_y)
                    if conta_cargas > 0:
                        canvas.coords(cargas_e_pilhas[carga], posicao_x_encruzilhada+20, caminhao_eixo_y)
                    conta_cargas += 1


        if caminhao_eixo_y >= 490 and caminhao_eixo_x <= 700:
            caminhao_eixo_y = 490
            caminhao_eixo_x -= velocidade

        if caminhao_eixo_x <= 600:
            # alterando caixas quando CHEGAR na encruzilhada
            conta_cargas = 0
            for carga in cargas_no_caminhao:
                if carga:
                    canvas.coords(cargas_e_pilhas[carga], caminhao_eixo_x+59, caminhao_eixo_y)
                    if conta_cargas > 0:
                        canvas.coords(cargas_e_pilhas[carga], caminhao_eixo_x+79, caminhao_eixo_y)
                    conta_cargas += 1
            atualizar_texto(texto_DESCRICAO,"Chegou na ENCRUZILHADA")
            app.after(tempo_de_espera_encruzilhada, callback)  # Aguarda na encruzilhada pelo tempo definido
            return

        canvas.coords(caminhao_sprite_indo, 2000, 2000)
        canvas.coords(caminhao_sprite_vindo, caminhao_eixo_x, caminhao_eixo_y)
        conta_cargas = 0
        for carga in cargas_no_caminhao:
            if carga:
                canvas.coords(cargas_e_pilhas[carga], caminhao_eixo_x+43, caminhao_eixo_y)
                if conta_cargas > 0:
                    canvas.coords(cargas_e_pilhas[carga], caminhao_eixo_x+63, caminhao_eixo_y)
                conta_cargas += 1
        app.after(50, lambda: voltar_encruzilhada(callback))


    def voltar_deposito(callback,acao):
        atualizar_texto(texto_DESCRICAO,"Indo para depósito")
        global caminhao_eixo_x, caminhao_eixo_y, posicao_x_encruzilhada,posicao_x_deposito, tempo_de_espera_deposito, cargas_no_caminhao, cargas_e_pilhas,carga_in,carga_out,carga_fault
        carga_ou_descarga = acao
        ja_fez_carga_ou_descarga = False

        contador_de_acoes_fazer = 0
        contador_de_acoes_feitas = 0

        if caminhao_eixo_y < 490:
            caminhao_eixo_y += velocidade

        if caminhao_eixo_y >= 490:
            caminhao_eixo_x -= velocidade

        # ja atualiza as caixas
        if caminhao_eixo_x <= posicao_x_deposito:
            canvas.coords(caminhao_sprite_vindo, 2000, 2000)
            caminhao_eixo_x = 130
            caminhao_eixo_y = 490
            canvas.coords(caminhao_sprite_indo, caminhao_eixo_x, caminhao_eixo_y)
            atualizar_texto(texto_DESCRICAO,"Chegou no DEPÓSITO")
            # AQUI DENTRO TEREI QUE TESTAR O BRABO
            if 'descarregar' in carga_ou_descarga:
                contador_de_acoes_fazer += 1
                # ...
                # lógica da descarga
                print(f"====================== DESCARREGOU: {carga_ou_descarga['descarregar']}")
                                    
                if cargas_no_caminhao[0] == 'carga_1':
                    cargas_no_caminhao[0] = ''  # corrigido de == para =
                    carga_out +=1
                    atualizar_texto(texto_VAR_PACOTE_DESCAR,carga_out)
                    canvas.coords(sprite_pilha_01, 170, 305)
                elif cargas_no_caminhao[1] == 'carga_1':
                    cargas_no_caminhao[1] = ''  # corrigido de == para =
                    carga_out +=1
                    atualizar_texto(texto_VAR_PACOTE_DESCAR,carga_out)
                    canvas.coords(sprite_pilha_01, 170, 305)

                if cargas_no_caminhao[0] == 'carga_2':
                    cargas_no_caminhao[0] = ''  # corrigido de == para =
                    carga_out +=1
                    atualizar_texto(texto_VAR_PACOTE_DESCAR,carga_out)
                    canvas.coords(sprite_pilha_02, 170, 355)
                elif cargas_no_caminhao[1] == 'carga_2':
                    cargas_no_caminhao[1] = ''  # corrigido de == para =
                    carga_out +=1
                    atualizar_texto(texto_VAR_PACOTE_DESCAR,carga_out)
                    canvas.coords(sprite_pilha_02, 170, 355)

                if cargas_no_caminhao[0] == 'carga_3':
                    cargas_no_caminhao[0] = ''  # corrigido de == para =
                    carga_out +=1
                    atualizar_texto(texto_VAR_PACOTE_DESCAR,carga_out)
                    canvas.coords(sprite_pilha_03, 170, 405)
                elif cargas_no_caminhao[1] == 'carga_3':
                    cargas_no_caminhao[1] = ''  # corrigido de == para =
                    carga_out +=1
                    atualizar_texto(texto_VAR_PACOTE_DESCAR,carga_out)
                    canvas.coords(sprite_pilha_03, 170, 405)

                contador_de_acoes_feitas += 1
            if 'carregar' in carga_ou_descarga:
                
                atualizar_texto(texto_VAR_PACOTE_CARREG,carga_in)
                # ...
                # lógica da carga
                print(f"====================== CARREGOU: {carga_ou_descarga['carregar']}")
                                        # ('deposito', {'carregar': ['carga_2', 'carga_3'], 'descarregar': ['carga_1']}),                                    
                                            # 170, 305 - 170, 355 - 170, 405
                
                for i in carga_ou_descarga['carregar']: # para as 3 cargas possíveis
                        if cargas_no_caminhao[0] == '': # se a primeira parte vazia
                            cargas_no_caminhao[0] = i #carrega CARGA_X nela
                            print(f"CARREGUEI A CARGA {i} NA PARTE 1 de 2")
                            contador_de_acoes_fazer += 1
                            carga_in += 1
                            atualizar_texto(texto_VAR_PACOTE_CARREG,carga_in)
                            canvas.coords(cargas_e_pilhas[i], caminhao_eixo_x, caminhao_eixo_y)
                        else: # se não, a outra deve estar
                            print(cargas_no_caminhao)
                            cargas_no_caminhao[1] = i
                            print(f"CARREGUEI A CARGA {i} NA PARTE 2 de 2")
                            print("Ambas as partes preenchidas")
                            contador_de_acoes_fazer += 1
                            carga_in += 1
                            atualizar_texto(texto_VAR_PACOTE_CARREG,carga_in)
                            canvas.coords(cargas_e_pilhas[i], (caminhao_eixo_x+20), caminhao_eixo_y)

                    
                                                
                contador_de_acoes_feitas += 1

            if contador_de_acoes_fazer == contador_de_acoes_feitas:
                ja_fez_carga_ou_descarga = True

            if ja_fez_carga_ou_descarga:
                carga_fault+=1
                atualizar_texto(texto_VAR_PACOTE_FALTOU,carga_fault)
                app.after(tempo_de_espera_deposito, callback)  # Aguarda no depósito pelo tempo definido
            return

        canvas.coords(caminhao_sprite_indo, 2000, 2000)
        canvas.coords(caminhao_sprite_vindo, caminhao_eixo_x, caminhao_eixo_y)
        conta_cargas = 0
        for carga in cargas_no_caminhao:
            if carga:
                canvas.coords(cargas_e_pilhas[carga], caminhao_eixo_x+40, caminhao_eixo_y)
                if conta_cargas > 0:
                    canvas.coords(cargas_e_pilhas[carga], caminhao_eixo_x+60, caminhao_eixo_y)
                conta_cargas += 1
        app.after(50, lambda: voltar_deposito(callback,acao))




    def executar_rota(rota):
        if not rota:
            atualizar_texto(texto_DESCRICAO, "Rota concluída")
            return
        instrucao_atual = rota.pop(0)
        destino = instrucao_atual[0]
        carga_ou_descarga = instrucao_atual[1]
        if destino == 'CASA_I':
            atualizar_texto(texto_DESCRICAO,"Indo para CASA I")
            mover_para_casa(930, 225, lambda: voltar_encruzilhada(lambda: executar_rota(rota)), "CASA I")
        elif destino == 'CASA_II':
            atualizar_texto(texto_DESCRICAO,"Indo para CASA II")
            mover_para_casa(930, 310, lambda: voltar_encruzilhada(lambda: executar_rota(rota)), "CASA II")
        elif destino == 'CASA_III':
            atualizar_texto(texto_DESCRICAO,"Indo para CASA III")
            mover_para_casa(930, 400, lambda: voltar_encruzilhada(lambda: executar_rota(rota)), "CASA III")
        elif destino == 'CASA_IV':
            atualizar_texto(texto_DESCRICAO,"Indo para CASA IV")
            mover_para_casa(930, 490, lambda: voltar_encruzilhada(lambda: executar_rota(rota)), "CASA IV")
        elif destino == 'deposito':
            atualizar_texto(texto_DESCRICAO,"Indo para depósito")
            voltar_deposito(lambda: executar_rota(rota),acao=carga_ou_descarga)

    # Definir a rota

    rota = [
        ('CASA_I',{}),
        ('deposito', {'carregar': ['carga_1']}),
        ('CASA_I',{}),
        ('CASA_II',{}),
        ('deposito', {'carregar': ['carga_2']}),
        ('CASA_II',{}),
    ]
    # Iniciar a execução da rota
    executar_rota(rota)

    print_truck_positions()

botao_op_01 = CTkButton(canvas_menu,width=100,height=40,text="OPÇÃO 01", border_color='black',fg_color='grey',border_width=1)
botao_op_01.place(x=100,y=100)

app.mainloop()
