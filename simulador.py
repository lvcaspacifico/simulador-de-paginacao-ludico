from customtkinter import *
from tkinter import Canvas
from PIL import Image, ImageTk
import time

# Definindo janela
app = CTk()
app.geometry("1200x676")
app.resizable(False,False)
app.title("Simulador de Paginação: Delivery Edition v.0.1| @lvcspacifico")




class SimuladorDePaginacao:
    def __init__(self,mestre, destruir,rota, rota_enderecos):
        self.mestre = mestre
        self.rota = rota
        self.rota_enderecos = rota_enderecos
        destruir.destroy()
        # Carregar a imagem de fundo e redimensionar
        self.image_bg = Image.open("assets/img/bg.png").resize((1200, 676), Image.Resampling.LANCZOS)
        self.image_bg = ImageTk.PhotoImage(self.image_bg)

        ### CAMINHÃO | SPRITES
        # Carregar a imagem do caminhão INDO
        self.img_caminhao_indo = Image.open("assets/img/truck_l.png").resize((100, 100), Image.Resampling.LANCZOS)
        self.img_caminhao_indo = ImageTk.PhotoImage(self.img_caminhao_indo)
        # Carregar a imagem do caminhão VOLTANDO
        self.img_caminhao_vindo = Image.open("assets/img/truck_r.png").resize((100, 100), Image.Resampling.LANCZOS)
        self.img_caminhao_vindo = ImageTk.PhotoImage(self.img_caminhao_vindo)

        # Criar o canvas (div principal)
        self.canvas_simulador = Canvas(app, width=1200, height=676)
        self.canvas_simulador.pack(fill="both", expand=True,anchor='center')

        # Adicionar a imagem de fundo no canvas
        self.canvas_simulador.create_image(0, 0, image=self.image_bg, anchor=NW)
        self.caminhao_sprite_indo = self.canvas_simulador.create_image(70, 490, image=self.img_caminhao_indo, anchor=NW)
        self.caminhao_sprite_vindo = self.canvas_simulador.create_image(2000, 2000, image=self.img_caminhao_vindo, anchor=NW)

        ### SPRITES PILHAS DE CAIXAS
        # Carregar as imagens
        self.img_pilha_01 = Image.open("assets/img/box1.png").resize((50, 50), Image.Resampling.LANCZOS)
        self.img_pilha_01 = ImageTk.PhotoImage(self.img_pilha_01)
        self.sprite_pilha_01 = self.canvas_simulador.create_image(170, 305, image=self.img_pilha_01, anchor=NW)

        self.img_pilha_02 = Image.open("assets/img/box2.png").resize((50, 50), Image.Resampling.LANCZOS)
        self.img_pilha_02 = ImageTk.PhotoImage(self.img_pilha_02)
        self.sprite_pilha_02 = self.canvas_simulador.create_image(170, 355, image=self.img_pilha_02, anchor=NW)

        self.img_pilha_03 = Image.open("assets/img/box3.png").resize((50, 50), Image.Resampling.LANCZOS)
        self.img_pilha_03 = ImageTk.PhotoImage(self.img_pilha_03)
        self.sprite_pilha_03 = self.canvas_simulador.create_image(170, 405, image=self.img_pilha_03, anchor=NW)
        # definindo relação semantica entre as variaveis para poder animar (dicionário)
        self.cargas_e_pilhas = {'carga_1': self.sprite_pilha_01, 'carga_2': self.sprite_pilha_02, 'carga_3': self.sprite_pilha_03}

        # Variáveis para a posição x e y do caminhão
        self.caminhao_eixo_x = 70
        self.caminhao_eixo_y = 490
        self.cargas_no_caminhao = ['','']

        # Velocidade que ele se move
        self.velocidade = 20
        # PARADA PRINCIPAL ENCRUZILHADA
        self.posicao_x_encruzilhada = 680
        # PARADA PRINCIPAL DEPOSITO
        self.posicao_x_deposito = 130
        # TEMPOS PARADOS NAS PARADAS
        self.tempo_de_espera_casas = 1000  # 1s
        self.tempo_de_espera_deposito = 2500  # 5s
        self.tempo_de_espera_encruzilhada = 1000  # 3s
        # VARIAVEIS DE PAGE IN PAGE OUT ETC

        self.carga_meta_pacotes = 4
        self.carga_total_pacotes = 12
        self.carga_limite_pacotes = 4

        self.carga_in = 0
        self.carga_out = 0
        self.carga_fault = 0



        #### CRIANDO TEXTOS QUE APARECEM NA TELA
        ## UI | textos variáveis que NÃO vão ser atualizados (mas podem rs)
        ## unico que não atualiza é "LOGS" pois ta fixo na imagem de fundo
        self.tam_txt_UI = 8
        self.cor_txt_UI = 'white' # aceita hexcode
        self.font_txt_UI = 'Open Sans extrabold'
        self.texto_UI_DESCRICAO = self.canvas_simulador.create_text(720, 75, text="DESCRIÇÃO DA ROTA", font=(self.font_txt_UI, 13), fill=self.cor_txt_UI, tag="texto_ui_desc")

        self.texto_UI_LIMITE = self.canvas_simulador.create_text(200, 75, text="Limite Pacotes por Pilha", font=(self.font_txt_UI, self.tam_txt_UI), fill=self.cor_txt_UI, tag="texto_ui_limi")
        self.texto_UI_TOTAL = self.canvas_simulador.create_text(200, 121, text="Total Pacotes à Espera", font=(self.font_txt_UI, self.tam_txt_UI), fill=self.cor_txt_UI, tag="texto_ui_total")
        self.texto_UI_META = self.canvas_simulador.create_text(200, 166, text="Meta Entregas por Rota", font=(self.font_txt_UI, self.tam_txt_UI), fill=self.cor_txt_UI, tag="texto_ui_meta")

        self.texto_UI_PACOTE_FALTOU = self.canvas_simulador.create_text(409, 75, text="Pacote Faltou", font=(self.font_txt_UI, self.tam_txt_UI), fill=self.cor_txt_UI, tag="texto_ui_pac_falt")
        self.texto_UI_PACOTE_CARREG = self.canvas_simulador.create_text(406, 121, text="Pacote Carregado", font=(self.font_txt_UI, self.tam_txt_UI), fill=self.cor_txt_UI, tag="texto_ui_pac_carreg")
        self.texto_UI_PACOTE_DESCAR = self.canvas_simulador.create_text(406, 166, text="Pacote Descarregado", font=(self.font_txt_UI, self.tam_txt_UI), fill=self.cor_txt_UI, tag="texto_ui_pac_descar")

        ## VAR | textos variáveis que vão ser atualizados
        ## textos variáveis que vão ser atualizados
        self.tam_txt_VAR = 10
        self.cor_txt_VAR = 'blue4' # aceita hexcode
        self.font_txt_VAR = 'Open Sans extrabold'
        self.texto_DESCRICAO = self.canvas_simulador.create_text(720, 135, text="", font=(self.font_txt_VAR, 17), fill=self.cor_txt_VAR, tag="texto_desc")
        self.texto_VAR_LIMITE = self.canvas_simulador.create_text(299, 75, text=self.carga_limite_pacotes, font=(self.font_txt_VAR, self.tam_txt_VAR), fill=self.cor_txt_VAR, tag="texto_var_limi")
        self.texto_VAR_TOTAL = self.canvas_simulador.create_text(299, 121, text=self.carga_total_pacotes, font=(self.font_txt_VAR, self.tam_txt_VAR), fill=self.cor_txt_VAR, tag="texto_var_total")
        self.texto_VAR_META = self.canvas_simulador.create_text(299, 166, text=self.carga_meta_pacotes, font=(self.font_txt_VAR, self.tam_txt_VAR), fill=self.cor_txt_VAR, tag="texto_var_meta")

        self.texto_VAR_PACOTE_FALTOU = self.canvas_simulador.create_text(508, 75, text=self.carga_fault, font=(self.font_txt_VAR, self.tam_txt_VAR), fill=self.cor_txt_VAR, tag="texto_var_pac_falt")
        self.texto_VAR_PACOTE_CARREG = self.canvas_simulador.create_text(508, 121, text=self.carga_in, font=(self.font_txt_VAR, self.tam_txt_VAR), fill=self.cor_txt_VAR, tag="texto_var_pac_carreg")
        self.texto_VAR_PACOTE_DESCAR = self.canvas_simulador.create_text(508, 166, text=self.carga_out, font=(self.font_txt_VAR, self.tam_txt_VAR), fill=self.cor_txt_VAR, tag="texto_var_pac_descar")

        # BOTÃO VOLTAR AO MENU
        self.botao_voltar = CTkButton(self.mestre,width=80,height=40,text="VOLTAR",
                                border_color='black',fg_color='grey',corner_radius=2,
                                border_width=3, command= self.botao_voltar_menu,
                                hover_color='#77B255',font=("Open Sans extrabold italic",11))

        # Construindo o texto automaticamente na PRANCHETA
        texto_rota = "      ROTA: \n"
        for endereco in self.rota_enderecos:
                texto_rota += f"Endereço {endereco} \n"

        # Criando o texto no canvas
        
        self.texto_VAR_ROTA_PRANCHETA = self.canvas_simulador.create_text(
                                                                            1073, 135,
                                                                            text=texto_rota,
                                                                            font=(self.font_txt_VAR, 8),
                                                                            fill=self.cor_txt_VAR,
                                                                            tag="texto_var_rota"
                                                                        )
        
        def print_truck_positions(): # para debugar printa posições do caminhão
            print(f"Posição x: {self.caminhao_eixo_x} | Posição y: {self.caminhao_eixo_y}")
            app.after(50, print_truck_positions)

        def atualizar_texto(qual_texto, texto): # atualiza os textos que estão na tela quando chamado
            self.canvas_simulador.itemconfig(qual_texto, text=texto)

        def mover_para_casa(posicao_x_da_casa, posicao_y_da_casa, callback, casa): # vai para a determinada casa

            if self.caminhao_eixo_x < self.posicao_x_encruzilhada:
                self.caminhao_eixo_x += self.velocidade       

            if self.caminhao_eixo_y > posicao_y_da_casa and self.caminhao_eixo_x >= self.posicao_x_encruzilhada:
                self.caminhao_eixo_x = self.posicao_x_encruzilhada
                self.caminhao_eixo_y -= self.velocidade
                if self.caminhao_eixo_y - posicao_y_da_casa < 0:
                    self.caminhao_eixo_y = posicao_y_da_casa

            if self.caminhao_eixo_x >= self.posicao_x_encruzilhada and self.caminhao_eixo_y <= posicao_y_da_casa:
                self.caminhao_eixo_x += self.velocidade

            # ajustar caixas a posicao nova x QUANDO CHEGA NA CASA
            if self.caminhao_eixo_x >= posicao_x_da_casa:
                conta_cargas = 0
                for carga in self.cargas_no_caminhao:
                    if carga:
                        self.canvas_simulador.coords(self.cargas_e_pilhas[carga], self.caminhao_eixo_x-19, self.caminhao_eixo_y)
                        if conta_cargas > 0:
                            self.canvas_simulador.coords(self.cargas_e_pilhas[carga], self.caminhao_eixo_x+1, self.caminhao_eixo_y)
                        conta_cargas += 1
                atualizar_texto(self.texto_DESCRICAO,f"Chegou na {casa}")
                app.after(self.tempo_de_espera_casas, callback)
                return

            # Trocar a imagem para o caminhão indo
            self.canvas_simulador.coords(self.caminhao_sprite_vindo, 2000, 2000)
            self.canvas_simulador.coords(self.caminhao_sprite_indo, self.caminhao_eixo_x, self.caminhao_eixo_y)
            conta_cargas = 0
            for carga in self.cargas_no_caminhao:
                if carga:
                    self.canvas_simulador.coords(self.cargas_e_pilhas[carga], self.caminhao_eixo_x, self.caminhao_eixo_y)
                    if conta_cargas > 0:
                        self.canvas_simulador.coords(self.cargas_e_pilhas[carga], self.caminhao_eixo_x+20, self.caminhao_eixo_y)
                    conta_cargas += 1
            app.after(50, lambda: mover_para_casa(posicao_x_da_casa, posicao_y_da_casa, callback, casa))

        def voltar_encruzilhada(callback):
            atualizar_texto(self.texto_DESCRICAO,"Indo para ENCRUZILHADA")

            # Trocar a imagem para o caminhão voltando
            self.canvas_simulador.coords(self.caminhao_sprite_indo, 2000, 2000)
            self.canvas_simulador.coords(self.caminhao_sprite_vindo, self.caminhao_eixo_x, self.caminhao_eixo_y)

            if self.caminhao_eixo_x > 700:
                self.caminhao_eixo_x -= self.velocidade


            if self.caminhao_eixo_y < 490 and self.caminhao_eixo_x <= 700:
                caminhao_eixo_x = self.posicao_x_encruzilhada
                self.caminhao_eixo_y += self.velocidade
                conta_cargas = 0
                # alterando caixas
                for carga in self.cargas_no_caminhao:
                    if carga:
                        self.canvas_simulador.coords(self.cargas_e_pilhas[carga], self.posicao_x_encruzilhada, self.caminhao_eixo_y)
                        if conta_cargas > 0:
                            self.canvas_simulador.coords(self.cargas_e_pilhas[carga], self.posicao_x_encruzilhada+20, self.caminhao_eixo_y)
                        conta_cargas += 1


            if self.caminhao_eixo_y >= 490 and self.caminhao_eixo_x <= 700:
                self.caminhao_eixo_y = 490
                self.caminhao_eixo_x -= self.velocidade

            if self.caminhao_eixo_x <= 600:
                # alterando caixas quando CHEGAR na encruzilhada
                conta_cargas = 0
                for carga in self.cargas_no_caminhao:
                    if carga:
                        self.canvas_simulador.coords(self.cargas_e_pilhas[carga], self.caminhao_eixo_x+59, self.caminhao_eixo_y)
                        if conta_cargas > 0:
                            self.canvas_simulador.coords(self.cargas_e_pilhas[carga], self.caminhao_eixo_x+79, self.caminhao_eixo_y)
                        conta_cargas += 1
                atualizar_texto(self.texto_DESCRICAO,"Chegou na ENCRUZILHADA")
                app.after(self.tempo_de_espera_encruzilhada, callback)  # Aguarda na encruzilhada pelo tempo definido
                return

            self.canvas_simulador.coords(self.caminhao_sprite_indo, 2000, 2000)
            self.canvas_simulador.coords(self.caminhao_sprite_vindo, self.caminhao_eixo_x, self.caminhao_eixo_y)
            conta_cargas = 0
            for carga in self.cargas_no_caminhao:
                if carga:
                    self.canvas_simulador.coords(self.cargas_e_pilhas[carga], self.caminhao_eixo_x+43, self.caminhao_eixo_y)
                    if conta_cargas > 0:
                        self.canvas_simulador.coords(self.cargas_e_pilhas[carga], self.caminhao_eixo_x+63, self.caminhao_eixo_y)
                    conta_cargas += 1
            app.after(50, lambda: voltar_encruzilhada(callback))


        def voltar_deposito(callback,acao):
            atualizar_texto(self.texto_DESCRICAO,"Indo para depósito")
            carga_ou_descarga = acao
            ja_fez_carga_ou_descarga = False

            contador_de_acoes_fazer = 0
            contador_de_acoes_feitas = 0

            if self.caminhao_eixo_y < 490:
                self.caminhao_eixo_y += self.velocidade

            if self.caminhao_eixo_y >= 490:
                self.caminhao_eixo_x -= self.velocidade

            # ja atualiza as caixas
            if self.caminhao_eixo_x <= self.posicao_x_deposito:
                self.canvas_simulador.coords(self.caminhao_sprite_vindo, 2000, 2000)
                caminhao_eixo_x = 130
                caminhao_eixo_y = 490
                self.canvas_simulador.coords(self.caminhao_sprite_indo, self.caminhao_eixo_x, self.caminhao_eixo_y)
                atualizar_texto(self.texto_DESCRICAO,"Chegou no DEPÓSITO")
                # AQUI DENTRO TEREI QUE TESTAR O BRABO
                if 'descarregar' in carga_ou_descarga:
                    contador_de_acoes_fazer += 1
                    # ...
                    # lógica da descarga
                    print(f"====================== DESCARREGOU: {carga_ou_descarga['descarregar']}")
                                        # carga_ou_descarga['descarregar'] = ['carga_1']

                    # pra cada posição na lista 
                    for carga in carga_ou_descarga['descarregar']:
                        if carga == 'carga_1':
                            if self.cargas_no_caminhao[0] == carga:
                               self.cargas_no_caminhao[self.cargas_no_caminhao.index(carga)] = ''
                            if self.cargas_no_caminhao[1] == carga:
                               self.cargas_no_caminhao[self.cargas_no_caminhao.index(carga)] = ''
                            self.carga_out +=1
                            print(f"====================== DESCARREGOU 1? ERA {carga_ou_descarga['descarregar']}")
                            print(self.cargas_no_caminhao)
                            atualizar_texto(self.texto_VAR_PACOTE_DESCAR,self.carga_out)
                            self.canvas_simulador.coords(self.sprite_pilha_01, 170, 305)
                        if carga == 'carga_2':
                            if self.cargas_no_caminhao[0] == carga:
                               self.cargas_no_caminhao[self.cargas_no_caminhao.index(carga)] = ''
                            if self.cargas_no_caminhao[1] == carga:
                               self.cargas_no_caminhao[self.cargas_no_caminhao.index(carga)] = ''
                            self.carga_out +=1
                            print(f"====================== DESCARREGOU 2? ERA {carga_ou_descarga['descarregar']}")
                            print(self.cargas_no_caminhao)
                            atualizar_texto(self.texto_VAR_PACOTE_DESCAR,self.carga_out)
                            self.canvas_simulador.coords(self.sprite_pilha_02, 170, 355)
                        if carga == 'carga_3':
                            if self.cargas_no_caminhao[0] == carga:
                               self.cargas_no_caminhao[self.cargas_no_caminhao.index(carga)] = ''
                            if self.cargas_no_caminhao[1] == carga:
                               self.cargas_no_caminhao[self.cargas_no_caminhao.index(carga)] = ''
                            self.carga_out +=1
                            print(f"====================== DESCARREGOU 3? ERA {carga_ou_descarga['descarregar']}")
                            print(self.cargas_no_caminhao)
                            atualizar_texto(self.texto_VAR_PACOTE_DESCAR,self.carga_out)
                            self.canvas_simulador.coords(self.sprite_pilha_03, 170, 405)

                    contador_de_acoes_feitas += 1
                if 'carregar' in carga_ou_descarga:
                    
                    atualizar_texto(self.texto_VAR_PACOTE_CARREG,self.carga_in)
                    # ...
                    # lógica da carga
                    print(f"====================== CARREGOU: {carga_ou_descarga['carregar']}")
                                            # ('deposito', {'carregar': ['carga_2', 'carga_3'], 'descarregar': ['carga_1']}),                                    
                                                # 170, 305 - 170, 355 - 170, 405
                    
                    for i in carga_ou_descarga['carregar']: # para as 3 cargas possíveis
                            if self.cargas_no_caminhao[0] == '': # se a primeira parte vazia
                                self.cargas_no_caminhao[0] = i #carrega CARGA_X nela
                                print(f"CARREGUEI A CARGA {i} NA PARTE 1 de 2")
                                contador_de_acoes_fazer += 1
                                self.carga_in += 1
                                atualizar_texto(self.texto_VAR_PACOTE_CARREG,self.carga_in)
                                self.canvas_simulador.coords(self.cargas_e_pilhas[i], caminhao_eixo_x, caminhao_eixo_y)
                            else: # se não, a outra deve estar
                                print(self.cargas_no_caminhao)
                                self.cargas_no_caminhao[1] = i
                                print(f"CARREGUEI A CARGA {i} NA PARTE 2 de 2")
                                print("Ambas as partes preenchidas")
                                contador_de_acoes_fazer += 1
                                self.carga_in += 1
                                atualizar_texto(self.texto_VAR_PACOTE_CARREG,self.carga_in)
                                self.canvas_simulador.coords(self.cargas_e_pilhas[i], (self.caminhao_eixo_x+20), self.caminhao_eixo_y)

                        
                                                    
                    contador_de_acoes_feitas += 1

                if contador_de_acoes_fazer == contador_de_acoes_feitas:
                    ja_fez_carga_ou_descarga = True

                if ja_fez_carga_ou_descarga:
                    self.carga_fault+=1
                    atualizar_texto(self.texto_VAR_PACOTE_FALTOU,self.carga_fault)
                    app.after(self.tempo_de_espera_deposito, callback)  # Aguarda no depósito pelo tempo definido
                return

            self.canvas_simulador.coords(self.caminhao_sprite_indo, 2000, 2000)
            self.canvas_simulador.coords(self.caminhao_sprite_vindo, self.caminhao_eixo_x, self.caminhao_eixo_y)
            conta_cargas = 0
            for carga in self.cargas_no_caminhao:
                if carga:
                    self.canvas_simulador.coords(self.cargas_e_pilhas[carga], self.caminhao_eixo_x+40, self.caminhao_eixo_y)
                    if conta_cargas > 0:
                        self.canvas_simulador.coords(self.cargas_e_pilhas[carga], self.caminhao_eixo_x+60, self.caminhao_eixo_y)
                    conta_cargas += 1
            app.after(50, lambda: voltar_deposito(callback,acao))




        def executar_rota(rota):
            if not rota:
                atualizar_texto(self.texto_DESCRICAO, "Rota concluída.")
                self.botao_voltar.place(x=820,y=120)
                
                return
            instrucao_atual = rota.pop(0)
            destino = instrucao_atual[0]
            carga_ou_descarga = instrucao_atual[1]
            if destino == 'CASA_I':
                atualizar_texto(self.texto_DESCRICAO,"Indo para CASA I")
                mover_para_casa(930, 225, lambda: voltar_encruzilhada(lambda: executar_rota(rota)), "CASA I")
            elif destino == 'CASA_II':
                atualizar_texto(self.texto_DESCRICAO,"Indo para CASA II")
                mover_para_casa(930, 310, lambda: voltar_encruzilhada(lambda: executar_rota(rota)), "CASA II")
            elif destino == 'CASA_III':
                atualizar_texto(self.texto_DESCRICAO,"Indo para CASA III")
                mover_para_casa(930, 400, lambda: voltar_encruzilhada(lambda: executar_rota(rota)), "CASA III")
            elif destino == 'CASA_IV':
                atualizar_texto(self.texto_DESCRICAO,"Indo para CASA IV")
                mover_para_casa(930, 490, lambda: voltar_encruzilhada(lambda: executar_rota(rota)), "CASA IV")
            elif destino == 'deposito':
                atualizar_texto(self.texto_DESCRICAO,"Indo para depósito")
                voltar_deposito(lambda: executar_rota(rota),acao=carga_ou_descarga)

        executar_rota(self.rota)

        print_truck_positions()

    def limpar_tudo(self):
        for widget in self.mestre.winfo_children():
            widget.destroy()
    
    def botao_voltar_menu(self):
        self.limpar_tudo()
        app.after(500,TelaDeMenu(self.mestre))

class TelaDeMenu:
    def __init__(self, app):
        self.app = app
            # CRIAR ROTAS PARA CADA TIPO e informar na função do botao o nome novo | ex: rota2 ou rota_dem_fifo
        self.rota_enderecos_teste = ['1']
        self.rota_teste = [
                ('CASA_I',{}),
                ('CASA_II',{}),
            ]

        self.rota_enderecos_demanda_fifo = ['1','2','6','10']
        self.rota_demanda_fifo = [
                ('CASA_I',{}),
                ('deposito', {'carregar': ['carga_1']}),
                ('CASA_I',{}),
                ('CASA_I',{}),
                ('CASA_II',{}),
                ('deposito', {'carregar': ['carga_2']}),
                ('CASA_II',{}),

                ('CASA_III',{}),
                ('deposito', {'descarregar': ['carga_1'],'carregar': ['carga_3']}),
                ('CASA_III',{})
            ]
        
        self.rota_enderecos_demanda_lru = ['1','2','6','10'] #carga 1 é tanto a primeira quanto a menos recentemente usada
        self.rota_demanda_lru = [
                ('CASA_I',{}),
                ('deposito', {'carregar': ['carga_1']}),
                ('CASA_I',{}),
                ('CASA_I',{}),
                ('CASA_II',{}),
                ('deposito', {'carregar': ['carga_2']}),
                ('CASA_II',{}),

                ('CASA_III',{}),
                ('deposito', {'descarregar': ['carga_1'],'carregar': ['carga_3']}),
                ('CASA_III',{})
            ]
        
        self.rota_enderecos_demanda_lfu = ['1','2','6','10']
        self.rota_demanda_lfu = [
                ('CASA_I',{}),
                ('deposito', {'carregar': ['carga_1']}),
                ('CASA_I',{}),
                ('CASA_I',{}),
                ('CASA_II',{}),
                ('deposito', {'carregar': ['carga_2']}),
                ('CASA_II',{}),

                ('CASA_III',{}),
                ('deposito', {'descarregar': ['carga_2'],'carregar': ['carga_3']}),
                ('CASA_III',{})
            ]
        
        self.rota_enderecos_antecipada_fifo = ['1','2','6','10']
        self.rota_antecipada_fifo = [
                ('CASA_I',{}),
                ('deposito', {'carregar': ['carga_1']}),
                ('deposito', {'carregar': ['carga_2']}),
                ('CASA_I',{}),
                ('CASA_I',{}),
                ('CASA_II',{}),
                ('CASA_II',{}),

                ('CASA_III',{}),
                ('deposito', {'descarregar': ['carga_1'],'carregar': ['carga_3']}),
                ('CASA_III',{})
            ]
        
        self.rota_enderecos_antecipada_lru = ['1','2','6','10']  #carga 1 é tanto a primeira quanto a menos recentemente usada
        self.rota_antecipada_lru = [
                ('CASA_I',{}),
                ('deposito', {'carregar': ['carga_1']}),
                ('deposito', {'carregar': ['carga_2']}),
                ('CASA_I',{}),
                ('CASA_I',{}),
                ('CASA_II',{}),
                ('CASA_II',{}),

                ('CASA_III',{}),
                ('deposito', {'descarregar': ['carga_1'],'carregar': ['carga_3']}),
                ('CASA_III',{})
            ]
        
        self.rota_enderecos_antecipada_lfu = ['1','2','6','10']
        self.rota_antecipada_lfu = [
                ('CASA_I',{}),
                ('deposito', {'carregar': ['carga_1']}),
                ('deposito', {'carregar': ['carga_2']}),
                ('CASA_I',{}),
                ('CASA_I',{}),
                ('CASA_II',{}),
                ('CASA_II',{}),

                ('CASA_III',{}),
                ('deposito', {'descarregar': ['carga_2'],'carregar': ['carga_3']}),
                ('CASA_III',{})
            ]
        
        self.rota_enderecos_thrashing_fifo = ['1','2','6','10','3','5','11']
        self.rota_thrashing_fifo = [
                ('CASA_I',{}),
                ('deposito', {'carregar': ['carga_1']}),
                ('CASA_I',{}),
                ('CASA_I',{}),
                ('CASA_II',{}),
                ('deposito', {'carregar': ['carga_2']}),
                ('CASA_II',{}),

                ('CASA_III',{}),
                ('deposito', {'descarregar': ['carga_1'],'carregar': ['carga_3']}),
                ('CASA_III',{}),
                
                ('CASA_I',{}),
                ('deposito', {'descarregar': ['carga_2'],'carregar': ['carga_1']}),
                ('CASA_I',{}),
                
                ('CASA_II',{}),
                ('deposito', {'descarregar': ['carga_3'],'carregar': ['carga_2']}),
                ('CASA_II',{}),
                
                ('CASA_III',{}),
                ('deposito', {'descarregar': ['carga_1'],'carregar': ['carga_3']}),
                ('CASA_III',{})
            ]
        
        
        self.fonte = 'Open Sans extrabold italic'
        self.tam_fonte = 16
        # Carregar a imagem de fundo do menu e redimensionar
        self.img_bg_menu = Image.open("assets/img/bg_menu.png").resize((1200, 676), Image.Resampling.LANCZOS)
        self.img_bg_menu = ImageTk.PhotoImage(self.img_bg_menu)
        self.canvas_menu = Canvas(app, width=1200, height=676)
        self.canvas_menu.pack(fill="both", expand=True,anchor='center')
        self.canvas_menu.create_image(0, 0, image=self.img_bg_menu, anchor=NW)

        self.botao_op_01 = CTkButton(self.canvas_menu,width=200,height=60,text="DEMANDA | FIFO",
                                border_color='black',fg_color='grey',corner_radius=2,
                                border_width=3, command= lambda: SimuladorDePaginacao(app,self.canvas_menu,self.rota_demanda_fifo, self.rota_enderecos_demanda_fifo), font=(self.fonte,self.tam_fonte),
                                hover_color='#77B255')
        self.botao_op_01.place(x=390,y=260)

        self.botao_op_02 = CTkButton(self.canvas_menu,width=200,height=60,text="ANTECIPADA | FIFO",
                                border_color='black',fg_color='grey',corner_radius=2,
                                border_width=3, command= lambda: SimuladorDePaginacao(app,self.canvas_menu,self.rota_antecipada_fifo, self.rota_enderecos_antecipada_fifo), font=(self.fonte,self.tam_fonte),
                                hover_color='#77B255')
        self.botao_op_02.place(x=610,y=260)

        self.botao_op_03 = CTkButton(self.canvas_menu,width=200,height=60,text="DEMANDA | LRU",
                                border_color='black',fg_color='grey',corner_radius=2,
                                border_width=3, command= lambda: SimuladorDePaginacao(app,self.canvas_menu,self.rota_demanda_lru, self.rota_enderecos_demanda_lru), font=(self.fonte,self.tam_fonte),
                                hover_color='#77B255')
        self.botao_op_03.place(x=390,y=340)

        self.botao_op_04 = CTkButton(self.canvas_menu,width=200,height=60,text="ANTECIPADA | LRU",
                                border_color='black',fg_color='grey',corner_radius=2,
                                border_width=3, command= lambda: SimuladorDePaginacao(app,self.canvas_menu,self.rota_antecipada_lru, self.rota_enderecos_antecipada_lru), font=(self.fonte,self.tam_fonte),
                                hover_color='#77B255')
        self.botao_op_04.place(x=610,y=340)

        self.botao_op_05 = CTkButton(self.canvas_menu,width=200,height=60,text="DEMANDA | LFU",
                                border_color='black',fg_color='grey',corner_radius=2, border_width=3,
                                command= lambda: SimuladorDePaginacao(app,self.canvas_menu,self.rota_demanda_lfu, self.rota_enderecos_demanda_lfu), font=(self.fonte,self.tam_fonte),
                                hover_color='#77B255')
        self.botao_op_05.place(x=390,y=420)

        self.botao_op_06 = CTkButton(self.canvas_menu,width=200,height=60,text="ANTECIPADA | LFU",
                                border_color='black',fg_color='grey',corner_radius=2, border_width=3,
                                command= lambda: SimuladorDePaginacao(app,self.canvas_menu,self.rota_antecipada_lfu, self.rota_enderecos_antecipada_lfu), font=(self.fonte,self.tam_fonte),
                                hover_color='#77B255')
        self.botao_op_06.place(x=610,y=420)

        self.botao_op_07 = CTkButton(self.canvas_menu,width=200,height=60,text="TRASHING (FIFO)",
                                border_color='black',fg_color='grey',corner_radius=2,
                                border_width=3, command= lambda: SimuladorDePaginacao(app,self.canvas_menu,self.rota_thrashing_fifo, self.rota_enderecos_thrashing_fifo), font=(self.fonte,self.tam_fonte),
                                hover_color='#77B255')
        self.botao_op_07.place(x=390,y=500)

        self.botao_op_08 = CTkButton(self.canvas_menu,width=200,height=60,text="[ROTA TESTE]",
                                border_color='black',fg_color='grey',corner_radius=2,
                                border_width=3, command= lambda: SimuladorDePaginacao(app,self.canvas_menu,self.rota_teste, self.rota_enderecos_teste), font=(self.fonte,self.tam_fonte),
                                hover_color='#77B255')
        self.botao_op_08.place(x=610,y=500)

        self.label_titulo_do_projeto = CTkLabel(self.canvas_menu, width=450,height=90, fg_color='black',text='SIMULADOR DE PAGINAÇÃO', font=("Open Sans extrabold",28))
        self.label_titulo_do_projeto.place(x=373,y=100)

        self.label_subtitulo_do_projeto = CTkLabel(self.canvas_menu, width=310,height=50, fg_color='#77B255',text='Delivery Sim Edition', font=(self.fonte,22,"underline"))
        self.label_subtitulo_do_projeto.place(x=445,y=175)

TelaDeMenu(app)

app.mainloop()
