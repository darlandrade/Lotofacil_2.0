import locale
import random
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview, Style, Combobox, Progressbar
import json
from scraping import buscar_ultimo_concurso, salvar_concursos

locale.setlocale(locale.LC_MONETARY, 'pt-BR.UTF-8')
fonte = ("Verdana", 10)
FUNDO = '#000022'
FUNDOATIVO = "#001f5c"
LETRAS = 'white'
GRAY = 'gray'
CORBOTAO = "#0C044D"


class Loteria(Tk):
    def __init__(self):
        Tk.__init__(self)
        x = 1250
        y = 640
        self.resizable(False, False)
        # Cria o objeto que utilizaremos para configurar o estilo da árvore, tal como a cor da linha selecionada
        estilo = Style()

        # Configura o tamanho da janela e posicionamento
        self.geometry(f"{x}x{y}+"
                      f"{int(self.winfo_screenwidth() / 2 - x / 2) + 1600}+"
                      f"{int(self.winfo_screenheight() / 2 - y / 2)}")
        self.title("Loto fácil 2.0")
        self.configure(background=FUNDO)

        # ############################################################################################################ #
        # #####################             Leitura do arquivo com jogos 20%             ############################# #
        # ############################################################################################################ #
        # Frame que posiciona o conteúdo de leitura do arquivo com os jogos a serem escolhidos para formação dos
        # 12 jogos que serão apostados
        f_esquerda = Frame(self, background=FUNDO)
        f_esquerda.grid(row=0, column=0)

        # Mostras quais os jogos que tiveram algum resultado em 20% de todos os jogos já sorteados
        # Frame jogos 20 porcento
        f_jogos20 = Frame(f_esquerda,
                          height=10,
                          background=FUNDO, )
        f_jogos20.pack(fill=X, padx=2)

        l_jogos20 = Label(f_jogos20,
                          text="Jogos para escolher e gerar uma sequência de números\n"
                               "que serão utilizados para gerar nossos jogos.",
                          background=FUNDO,
                          fg=LETRAS,
                          font=fonte)
        l_jogos20.pack()
        # Criação do scrollbar
        scroll_jogos20 = Scrollbar(f_jogos20)
        scroll_jogos20.pack(side=RIGHT, fill=Y, pady=5)

        # Árvore para mostrar todos os jogos
        self.t_jogos20 = Treeview(f_jogos20,
                                  columns=("c1", "c2"),
                                  height=10,
                                  show="headings",
                                  yscrollcommand=scroll_jogos20
                                  )
        # Configura Headings, largura da coluna, e posicionamento do texto
        self.t_jogos20.column("#1",
                              anchor=CENTER,
                              width=50, )
        self.t_jogos20.heading("#1",
                               text="Jogo")

        self.t_jogos20.column("#2",
                              anchor=CENTER,
                              width=500, )
        self.t_jogos20.heading("#2",
                               text="Números")

        self.t_jogos20.pack(padx=10, ipadx=10, pady=5)

        estilo.configure("Treeview", font=fonte)
        estilo.map("Treeview",
                   background=[("selected", CORBOTAO)],
                   )

        scroll_jogos20.config(command=self.t_jogos20.yview)

        # Carrega os jogos no arquivo 'jogos20porcento.txt' para ser escolhido quais jogos se tornarão 1
        self.carrega_jogos20_na_arvore(le_arquivo_20())
        self.lista_ids_arvore = self.t_jogos20.get_children()

        # ############################################################################################################ #
        # ########################             Seção para gerar os números            ################################ #
        # ############################################################################################################ #

        # Frame para suportar o botão que irá pegar os jogos selecionado e gerar os números para as apostas
        f_numeros_gerados = Frame(f_esquerda, background=FUNDO)
        f_numeros_gerados.pack()
        # Sempre que este botão for clicado, dos itens da lista serão escolhidos aleatóriamente para criação
        # da lista que irá gerar os números.
        b_gera_os_numeros = Button(f_numeros_gerados,
                                   text="Gerar sequência de números",
                                   background=CORBOTAO,
                                   activebackground=FUNDOATIVO,
                                   fg=LETRAS,
                                   activeforeground=LETRAS,
                                   font=fonte,
                                   borderwidth=4,
                                   width=30,
                                   command=self.cria_lista_com_numeros_dos_jogos_a_serem_escolhidos)
        b_gera_os_numeros.grid(pady=10, row=0, column=1, padx=(0, 30))

        b_carregar_jogos_salvos = Button(f_numeros_gerados,
                                         text="Carregar jogos salvos",
                                         background=CORBOTAO,
                                         activebackground=FUNDOATIVO,
                                         fg=LETRAS,
                                         activeforeground=LETRAS,
                                         font=fonte,
                                         borderwidth=4,
                                         width=30,
                                         command=self.carregar_jogos)
        b_carregar_jogos_salvos.grid(row=0, column=2, padx=(30, 0))

        # Label para exibir quais foram os números escolhidos baseado na seleção
        self.numeros_gerados = Label(f_numeros_gerados,
                                     text="Os jogos serão baseados nos seguintes números...\n\n ",
                                     background=FUNDO,
                                     fg=LETRAS,
                                     font=fonte,
                                     )
        self.numeros_gerados.grid(row=1, column=0, columnspan=3,)

        # ############################################################################################################ #
        # ######################            Pergunta quantos jogos serão gerado           ############################ #
        # ############################################################################################################ #
        # Posicionamento da entrada onde será informado quantos jogos devem ser gerados, como o programa é para jogos
        # feitos via 'web', o mínimo de jogos é 12.
        f_quantidade_jogos = Frame(f_esquerda, background=FUNDO)
        f_quantidade_jogos.pack()

        # Label perguntando a quantidade de jogos a serem gerados
        l_info_quantidade = Label(f_quantidade_jogos,
                                  text="Informe quantos jogos serão gerados: ",
                                  font=fonte,
                                  background=FUNDO,
                                  foreground=LETRAS)
        l_info_quantidade.pack(side=LEFT, pady=15)
        # Entrada para informar quantos jogos serão gerados
        self.e_quantidade_jogos = Entry(f_quantidade_jogos,
                                        width=4,
                                        justify=CENTER,
                                        font=fonte)
        self.e_quantidade_jogos.pack(side=RIGHT)
        self.e_quantidade_jogos.insert(0, "12")  # Inicia com 12, se apagar e colocar menor que 12, volta para 12.
        self.e_quantidade_jogos.bind("<ButtonRelease-1>", self.seleciona_tudo)  # Sempre seleciona tudo ao clicar
        # ############################################################################################################ #
        # ######################             Árvore que irá mostrar os números            ############################ #
        # ############################################################################################################ #

        # Posiciona a árvore com os jogos criados
        f_arvore_jogos = Frame(f_esquerda, background=FUNDO)
        f_arvore_jogos.pack()

        # Criação de um 'scroll', mas pode rolar com o 'scroll' do mouse
        scroll_apostas = Scrollbar(f_arvore_jogos)
        scroll_apostas.pack(side=RIGHT, fill=Y, pady=5)

        # Criação da árvore e suas colunas
        self.t_arvore_jogos = Treeview(f_arvore_jogos,
                                       yscrollcommand=scroll_apostas,
                                       columns=("c1", "c2"),
                                       show="headings",
                                       height=7,
                                       )
        self.t_arvore_jogos.column("#1",
                                   anchor=CENTER,
                                   width=50, )
        self.t_arvore_jogos.column("#2",
                                   anchor=CENTER,
                                   width=500)

        self.t_arvore_jogos.heading("#1",
                                    text="Jogo nº")
        self.t_arvore_jogos.heading("#2",
                                    text="Aposta")
        self.t_arvore_jogos.pack(padx=10, ipadx=10, pady=5)

        # Scroll para rolagem das apostas
        scroll_apostas.config(command=self.t_arvore_jogos.yview)

        # ############################################################################################################ #
        # #########################             Layout busca de resultados            ############################### #
        # ############################################################################################################ #

        # Cria uma linha para divir a disposição dos outros frames
        f_divisor = LabelFrame(self, background='#000822', width=2, height=y, )
        f_divisor.grid(row=0, column=1, padx=15)
        # ############################################################################################################ #

        # Este frame posiciona onde escolheremos o jogo para validar se algum de nossos jogos fez pontos ou não.
        f_direita = Frame(self, background=FUNDO)
        f_direita.grid(row=0, column=2)

        # Exibe se o concurso está atualizado ou não
        f_atualizar = Frame(f_direita, background=FUNDO)
        f_atualizar.pack()
        self.l_concurso_atualizado = Label(f_atualizar,
                                           text="",
                                           background=FUNDO,
                                           fg=LETRAS,
                                           font=fonte,
                                           anchor=CENTER)
        self.l_concurso_atualizado.pack(side=LEFT, )

        self.b_atualizar = Button(f_atualizar,
                                  text="Atualizar",
                                  font=fonte,
                                  background=CORBOTAO,
                                  foreground=LETRAS)
        # self.b_atualizar.pack()

        self.progress_bar = Progressbar(f_atualizar,
                                        orient=HORIZONTAL,
                                        length=100,
                                        mode='indeterminate')

        self.atualizar_mensagem()

        # Aqui informamos quantos números dentro da nossa lista, estão contidos no resultado do concurso escolhido
        l_comparacao_texto = Label(f_direita,
                                   width=70,
                                   text="Escolha um concurso para ver quantos números em nossa lista estão nele.",
                                   background=FUNDO,
                                   fg=LETRAS,
                                   font=fonte,
                                   anchor=CENTER)
        l_comparacao_texto.pack()

        # Posiciona a combobox para escolher algum jogo e comparar
        f_combobox = Frame(f_direita,
                           background=FUNDO)
        f_combobox.pack()
        # Cria a combobox e preenche com os últimos jogos
        self.c_resultados = Combobox(f_combobox, font=fonte, background=FUNDO, justify=CENTER)
        self.c_resultados.pack(side=LEFT, pady=5)
        self.c_resultados["state"] = "readonly"  # Fica como somente leitura
        # self.c_resultados.set("Escolha um concurso")  # Mensagem iniciar, antes da escolha do jogo
        self.c_resultados.option_add('*TCombobox*Listbox.Justify', 'center')  # Posiciona o texto no centro

        # Ao clicar, vai mostrar o jogo e quantos pontos foram feitos, com o montando feito e o quanto foi gasto
        # no jogo conforme a quantidade de jogos gerados
        self.c_resultados.bind("<<ComboboxSelected>>", self.compara_numero_resultado)
        # Carrega o arquivo com os concursos
        self.arquivo = le_arquivo_resultados()
        self.carrega_concursos()

        # Caso queira gerar outros jogos, não precisa escolher o mesmo concurso na combobox
        # Basta clicar no botão e a tela irá atualizar
        b_combobox_check = Button(f_combobox,
                                  text="Verificar",
                                  font=fonte,
                                  activebackground=FUNDOATIVO,
                                  background=CORBOTAO,
                                  fg=LETRAS,
                                  activeforeground=LETRAS,
                                  borderwidth=4,
                                  command=self.compara_numero_resultado)
        b_combobox_check.pack(side=RIGHT, padx=10)

        # Cria label para mostrar quantos números temos dos 15.
        self.l_comparacao_resultado = Label(f_direita,
                                            width=70,
                                            text="...",
                                            background=FUNDO,
                                            fg=LETRAS,
                                            font=fonte,
                                            anchor=CENTER)
        self.l_comparacao_resultado.pack(pady=5)

        # Lista para armazenar os números gerados para a criação dos jogos.
        self.numeros_gerados_comparar = []

        # Label que mostra o número do concurso
        self.l_jogo_concurso = Label(f_direita,
                                     width=70,
                                     text=" ",
                                     background=FUNDO,
                                     fg=LETRAS,
                                     font=fonte,
                                     anchor=CENTER)
        self.l_jogo_concurso.pack()
        # Label que mostra o jogo do concurso selecionado
        self.l_jogo_concurso_resultado = Label(f_direita,
                                               text=" ",
                                               background=FUNDO,
                                               fg=LETRAS,
                                               font=fonte,
                                               anchor=CENTER)
        self.l_jogo_concurso_resultado.pack()
        self.l_mensagem_qnt_jogos = Label(f_direita,
                                          text=" ",
                                          background=FUNDO,
                                          fg=LETRAS,
                                          font=fonte,
                                          anchor=CENTER)

        self.l_mensagem_qnt_jogos.pack(pady=5)

        # Posiciona os resultados
        self.lf_mensagem_qnt_jogos = LabelFrame(f_direita, width=150, height=105, background=FUNDO, borderwidth=0)
        self.lf_mensagem_qnt_jogos.pack()
        # Label onde consta a quantidade de pontos feitos, se nenhum tiver mais que 11, mostra o número máximo.
        self.l_mensagem_qnt_resultados = Label(self.lf_mensagem_qnt_jogos,
                                               text=" \n\n\n\n\n",
                                               background=FUNDO,
                                               fg=LETRAS,
                                               font=fonte,
                                               anchor=CENTER
                                               )
        # Mostra o quanto foi gasto nos jogos conforme a quantidade informada
        self.l_valor_gasto = Label(f_direita,
                                   text=" ",
                                   background=FUNDO,
                                   fg=LETRAS,
                                   font=fonte,
                                   anchor=CENTER
                                   )
        self.l_valor_gasto.pack(pady=10)
        # Mostra, conforme os resultados, o quanto fizemos de lucro ou o quanto perdemos.
        self.l_lucro_despesa = Label(f_direita,
                                     text=" \n",
                                     background=FUNDO,
                                     fg=LETRAS,
                                     font=fonte,
                                     anchor=CENTER
                                     )
        self.l_lucro_despesa.pack()

        # ############################################################################################################ #
        # ######################             Funções para busca de resultados            ############################# #
        # ############################################################################################################ #

    def carregar_jogos(self):
        """Caso queira utilizar os últimos jogos salvos para validar com o resultado"""
        jogos = le_arquivo_jogos_gerados()
        self.t_arvore_jogos.delete(*self.t_arvore_jogos.get_children())
        for jogo, aposta in jogos.items():
            exibir = []
            for numero in aposta:
                exibir.append(str(numero))
            self.t_arvore_jogos.insert("", END, values=(jogo, ", ".join(exibir)))

    def atualizar_mensagem(self):
        """Ao iniciar o programa, verifica se está com o número do último concurso ou não e mostra
        uma mensagem"""
        ultimo_concurso = buscar_ultimo_concurso()
        if ultimo_concurso == le_ultimo_lotofacil_arquivo():
            self.l_concurso_atualizado['fg'] = 'green'
            self.l_concurso_atualizado['text'] = f"Programa atualizado"
        else:
            self.l_concurso_atualizado['fg'] = 'red'
            self.l_concurso_atualizado['text'] = f"Programa desatualizado, clique em atualizar"
            self.b_atualizar.pack(padx=5, side=RIGHT)
            self.b_atualizar['command'] = self.atualizar

    def atualizar(self):
        """Efetua uma atualização em nossa base"""

        salvar_concursos()
        self.b_atualizar.pack_forget()
        self.arquivo = le_arquivo_resultados()
        self.l_concurso_atualizado['fg'] = 'green'
        self.l_concurso_atualizado['text'] = f"Programa atualizado"
        self.carrega_concursos()

    def carrega_concursos(self):
        """
        Cria uma lista com o número de todos os jogos que temos no arquivo
        'JogosLotofcail.json' previavamento carregado na váriavel 'self.arquivo' e carrega-os na combobox
        """
        self.c_resultados.delete(0, END)
        lista_de_jogos = []
        for jogo, resultado in sorted(self.arquivo.items(), reverse=True):
            lista_de_jogos.append(jogo)
        self.c_resultados.set(lista_de_jogos[0])
        self.c_resultados["values"] = lista_de_jogos

    def compara_numero_resultado(self, e=None):
        """
        1 — Faz uma comparação entre os números gerados na seleção dos dois jogos anteriores.
        2 — Configura o texto da variável 'self.l_comparacao_resultado' informa a quantidade de números existentes
        3 — Configura o texto da variável 'self.l_jogo_concurso' informando o número do concurso selecionado
        4 — Configura o texto da variável 'self.l_jogo_concurso_resultado' informa o resultado do concurso
        5 — Configura o texto da variável 'self.l_mensagem_qnt_jogos' informa a quantidade de jogos feitos
        6 — Faz a contagem dos pontos e armezana na lista chamda 'pontos'
        7 — Configura o texto da variável 'self.l_mensagem_qnt_resultados' mostrando todos os pontos feitos
        8 — Por fim, mostra se tivemos lucro ou prejuízo

        —
        Se por acaso não for escolhido uma lista de números, antes de escolher o concurso, usamos o 'raise' para
        mostrar uma mensagem de erro, informando que não existe uma lista de números para comparar.
        """
        lista_numero = le_lista_numeros()
        if lista_numero:
            concurso = self.c_resultados.get()
            if concurso == "Escolha um concurso":
                messagebox.showinfo("Concurso", "Escolha um concurso")
            else:
                jogo = self.arquivo.get(concurso)
                numeros_divergentes = set(jogo).difference(lista_numero.get("jogo"))
                diferenca = 15 - len(numeros_divergentes)
                self.l_comparacao_resultado["text"] = f"Temos {diferenca} dos 15 números em nossa lista"
                self.l_jogo_concurso["text"] = f"O resultado do concurso {concurso} foi:"
                self.l_jogo_concurso_resultado["text"] = f"{jogo}"
                self.l_mensagem_qnt_jogos["text"] = f"Com {self.e_quantidade_jogos.get()} jogos conseguiríamos fazer..."

                jogos = le_arquivo_jogos_gerados()

                pontos = []
                for jg in jogos.values():
                    pontuacao = len(set(jg).intersection(jogo))
                    if pontuacao == 15:
                        pontos.append(15)
                    elif pontuacao == 14:
                        pontos.append(14)
                    elif pontuacao == 13:
                        pontos.append(13)
                    elif pontuacao == 12:
                        pontos.append(12)
                    elif pontuacao == 11:
                        pontos.append(11)
                    else:
                        pontos.append(pontuacao)
                self.l_mensagem_qnt_resultados.pack(padx=10, pady=10)
                self.l_mensagem_qnt_resultados["text"] = f"15 pontos = {pontos.count(15)}\n" \
                                                         f"14 pontos = {pontos.count(14)}\n" \
                                                         f"13 pontos = {pontos.count(13)}\n" \
                                                         f"12 pontos = {pontos.count(12)}\n" \
                                                         f"11 pontos = {pontos.count(11)}\n" \
                                                         f"Máximo de pontos: {max(pontos)}"

                valor_gasto = 2.5 * int(self.e_quantidade_jogos.get())
                self.l_valor_gasto["text"] = f"Valor gasto: {valor_gasto}"

                lucro = (pontos.count(13) * 25 + pontos.count(12) * 10 + pontos.count(11) * 5) - valor_gasto
                if pontos.count(14):
                    lucro += 1300 * pontos.count(14)
                self.l_lucro_despesa["text"] = f"Resultado financeiro: {locale.currency(lucro)}"

        else:
            raise ValueError("Não temos nenhuma lista ainda")

        # ############################################################################################################ #
        # ########################             Funções para gerar os números            ############################## #
        # ############################################################################################################ #

    def seleciona_tudo(self, e):
        """
        Faz a seleção de toda a caixa de entrada com o número de jogos a serem gerados
        """
        _nada = e
        self.e_quantidade_jogos.select_range(0, END)

    def gera_os_jogos(self, numeros_apostar):
        """
        Faz a criação dos jogos, adiciona na árvore e salva os jogos em um arquivo chamado 'JogosGerados.json'
        """
        # Apaga toda a árvore para adicionar novos jogos.
        self.t_arvore_jogos.delete(*self.t_arvore_jogos.get_children())

        jogos = []
        quantidade_jogos = int(self.e_quantidade_jogos.get())

        if quantidade_jogos < 12:
            quantidade_jogos = 12
            self.e_quantidade_jogos.delete(0, END)
            self.e_quantidade_jogos.insert(0, '12')

        if quantidade_jogos:
            # Enquanto não tivermos a quantidade de jogos solicitados na lista jogos, continua gerando jogos
            while len(jogos) < quantidade_jogos:
                jogo = []
                # Quinze números precisam ser escolhidos, e não podem repetir
                while len(jogo) < 15:
                    numero_aleatorio = random.choice(numeros_apostar)
                    if numero_aleatorio not in jogo:
                        jogo.append(numero_aleatorio)

                jogo.sort()

                if jogo in jogos:
                    # Se o jogo já existir na lista, não faz nada
                    print("Jogo já existe na lista. **** Jogo Apagado ****")
                else:
                    jogos.append(jogo)

            # Código para exibir os jogos na árvore
            salvar = {}
            for i, jogo in enumerate(jogos):
                texto_exibir = []
                salvar[f"{i+1}"] = jogo
                for n in jogo:
                    texto_exibir.append(str(n))
                self.t_arvore_jogos.insert("", END, values=(i + 1, ", ".join(texto_exibir)))

            with open("JogosGerados.json", "w") as arquivo:
                obj = json.dumps(salvar)
                arquivo.write(obj)

    def cria_lista_com_numeros_dos_jogos_a_serem_escolhidos(self):
        """
        Para a criação da nossa lista com números para gerar nossos jogos, usamos jogos antigos.
        Carregamos os jogos antigos em uma lista (numeros) e verificamos quantos jogos serão gerados.

        """
        numeros = self.recebe_os_jogos_para_escolha_dos_numeros()
        qnt_jogos = self.e_quantidade_jogos.get()
        # Se tivermos os números e a quantidade de jogos a serem gerados
        if numeros and qnt_jogos:
            # Usamos 'set' para unir duas listas e criamos uma com valores únicos, ou seja, removemos os repetidos.
            numeros_para_os_jogos = list(set(numeros[0]).union(numeros[1]))
            # Validamos quantos números temos em nossa lista
            tamanho_jogo = len(numeros_para_os_jogos)
            # Enquanto for menor que 18, adicionamos novos números
            while tamanho_jogo <= 18:
                # Criamos uma lista com números de 1 a 25
                numeros_1_25 = [x for x in range(1, 26)]
                # E usamos 'set' para remover os números existentes na nossa lista,
                # e ficar somente com os que não estão.
                jogo_numeros_adicionais = list(set(numeros_para_os_jogos).symmetric_difference(numeros_1_25))

                # Escolhe o número que será adicionado
                numero = random.choice(jogo_numeros_adicionais)
                # Adiciona na nossa lista
                numeros_para_os_jogos.append(numero)
                # Remove o número já escolhido para não ser escolhido novamente
                jogo_numeros_adicionais.remove(numero)
                # Aumenta o tamanho da nossa lista para sair do 'while'
                tamanho_jogo += 1

            # Enquanto nossa lista for maior que 20, pois queremos uma lista com 19 jogos...
            while tamanho_jogo >= 20:
                # Escolhe o número que será adicionado
                numero = random.choice(numeros_para_os_jogos)
                # Remove da nossa lista
                numeros_para_os_jogos.remove(numero)
                # Diminui o tamanho da nossa lista para sair do 'while'
                tamanho_jogo -= 1

            # Ordena os números
            numeros.sort()

            # Transforma todos em 'string' para exibição
            numeros = [str(i) for i in numeros_para_os_jogos]
            # Mostra os números
            self.numeros_gerados['text'] = f"Os jogos estão baseados nos seguintes números...\n " \
                                           f"{', '.join(numeros)}\n" \
                                           f"Um total de {len(numeros)} números foram escolhidos."
            # Adiciona os números para uma variável que será 'global'
            # self.numeros_gerados_comparar = numeros_para_os_jogos
            with open('NumerosParaJogos.json', 'w') as salvar:
                x = {'jogo': numeros_para_os_jogos}
                obj = json.dumps(x)
                salvar.write(obj)

            self.gera_os_jogos(numeros_para_os_jogos)  # Chama a função que irá gerar os jogos
        else:
            # Se não tiver nenhum número escolhido ou quantidade de jogos inexistente, mostra uma mensagem
            if not numeros:
                messagebox.showinfo("Nenhum jogo selecionado", "Favor selecionar dois jogos para geração dos números")
            if not qnt_jogos:
                messagebox.showinfo("Campo em branco", "Favor informar quantos jogos deseja fazer")

    def recebe_os_jogos_para_escolha_dos_numeros(self):
        """
        Recebe os dois jogos para a escolha da nossa lista de números:
        return: os números escolhidos
        """
        # Define quais serão os dois jogos para gerar nossos números, usamos a função 'random.choice' usando o 'id'
        # de cada 'item' da nossa árvore.
        self.t_jogos20.selection_set((random.choice(self.lista_ids_arvore), random.choice(self.lista_ids_arvore)))
        selecao = self.t_jogos20.selection()

        if selecao:
            selecionados = self.t_jogos20.selection()
            # Verifica o tamanho da seleção para verificações
            tamanho_selecao = len(selecionados)
            # Se for igual a 2
            if 1 < tamanho_selecao < 3:
                jogos = []  # Lista para guardar os jogos
                for x in selecionados:
                    # Chama a árvore e pelo 'id' encontra o valor 'value' no dicionário e escolhe o 'item' 1 da lista
                    jogos.append(self.t_jogos20.item(x).get("values")[1])

                # Transforma a 'string' na lista, em uma lista de números 'string'
                for i, x in enumerate(jogos):
                    jogos[i] = x.split(" ")
                # Tranforma todos os números em 'int.'
                jogos[0] = [int(i) for i in jogos[0]]
                jogos[1] = [int(i) for i in jogos[1]]

                # retorna os jogos
                return jogos
        # Limpa a seleção
        self.t_jogos20.selection_clear()

    def carrega_jogos20_na_arvore(self, jogos):
        """Preenche a árvore com os números a serem escolhidos"""
        # Para cada jogo em jogos
        for i, jogo in enumerate(jogos):
            self.t_jogos20.insert("", END, values=(i + 1, jogo))


def le_arquivo_20():
    """
        Faz a leitura do arquivo contendo jogos que apareceram em 20 porcentos de todos os sorteios
        ou jogos feitos aleatoriamente, mas que podem trazer algum resultado
        :return: uma lista com todos os jogos do arquivo
        """

    with open("C:\\Users\\darla\\Desktop\\Lotofacil\\LotoFacilResultados.json", "r") as jogos20:
        conteudo = []
        arquivo = json.load(jogos20)
        fim = int(list(arquivo.keys())[-1])
        for i in range(fim - 20, fim + 1):
            conteudo.append(arquivo[str(i)])

        return conteudo


def le_arquivo_resultados():
    """
    Faz uma leitura do arquivo onde se encontram todos os jogos registrados de concursos antigos
    :return: um json com o número do concurso e o jogo
    """
    with open("LotoFacilResultados.json", "r") as arquivo:
        jogos_resultados = json.load(arquivo)
        return jogos_resultados


def le_arquivo_jogos_gerados():
    """
    Faz uma leitura do arquivo gerado ao clicar em "Gerar sequência de números"
    :return: um json com todos os jogos para consultas
    """
    with open("JogosGerados.json", "r") as arquivo:
        jogos_gerados = json.load(arquivo)
        return jogos_gerados


def le_ultimo_lotofacil_arquivo():
    with open("LotoFacilResultados.json", 'r') as arquivo:
        concurso = json.load(arquivo)
        return list(concurso.keys())[-1]

def le_lista_numeros():
    with open("NumerosParaJogos.json", "r") as arquivo:
        return json.load(arquivo)

if __name__ == '__main__':
    # le_arquivo_20()
    # le_arquivo_jogos_antigos()
    loteria = Loteria()

    # loteria.cria_lista_com_numeros_do_jogo()
    loteria.mainloop()
