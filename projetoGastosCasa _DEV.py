import tkinter as tk
from tkinter import ttk
from tkinter import *
import mysql.connector
import tkinter.messagebox
from tkinter import messagebox
from datetime import datetime
from tkcalendar import Calendar
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import babel.numbers

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="root",
    database= "casa_dev"
)

cursor = db.cursor()
cursor_qry_id = db.cursor()
cursor_qry_categoria = db.cursor()
cursor_qry_qPagou = db.cursor()
cursor_qry_casa = db.cursor()
cursor_qry_valor = db.cursor()
cursor_qry_desc = db.cursor()
cursor_qry_data = db.cursor()
cursorJanela4 = db.cursor()
cursor_login = db.cursor()




#=======================================================================================================================================================================================
#                                                                  LOGIN USUÁRIOS
#=======================================================================================================================================================================================
def registrar_usuario(username, password):
    try:
        registro_usuario = f"INSERT INTO usuarios (username, password) VALUES ('{username}', '{password}')"
        cursor_login.execute(registro_usuario)
        db.commit()
        return True
    except Exception as e:
        return False

def login_usuario(username, password):
    consultar_login = f"SELECT * FROM usuarios WHERE username = '{username}' AND password = '{password}'"
    cursor_login.execute(consultar_login)
    return cursor_login.fetchone() is not None

def janela_registro():
    janela_registro = tk.Toplevel()
    janela_registro.title("Registrar")

    tk.Label(janela_registro, text="Usuário").grid(row=0, column=0)
    tk.Label(janela_registro, text="Senha").grid(row=1, column=0)

    entrada_usuario = tk.Entry(janela_registro)
    entrada_senha = tk.Entry(janela_registro, show='*')

    entrada_usuario.grid(row=0, column=1)
    entrada_senha.grid(row=1, column=1)

    def registrar():
        username = entrada_usuario.get()
        password = entrada_senha.get()
        if registrar_usuario(username, password):
            messagebox.showinfo("Sucesso", "Registrado com sucesso!")
            janela_registro.destroy()
        else:
            messagebox.showerror("Erro", "Usuário já existe!")

    tk.Button(janela_registro, text="Registrar", command=registrar).grid(row=2, column=1)

def janela_login():
    janela_login = tk.Tk()
    janela_login.title("Login")

    # Definindo o tamanho da janela
    largura = 200
    altura = 160

    # Calculando a posição para centralizar a janela
    largura_tela = janela_login.winfo_screenwidth()
    altura_tela = janela_login.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)

    # Definindo a geometria da janela
    janela_login.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    tk.Label(janela_login, text="Usuário").grid(row=0, column=0, pady=10)
    tk.Label(janela_login, text="Senha").grid(row=1, column=0, pady=10)

    entrada_usuario = tk.Entry(janela_login)
    entrada_senha = tk.Entry(janela_login, show='*')

    entrada_usuario.grid(row=0, column=1)
    entrada_senha.grid(row=1, column=1)

    login_success = [False]

    def login():
        username = entrada_usuario.get()
        password = entrada_senha.get()
        if login_usuario(username, password):
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            login_success[0] = True
            janela_login.destroy()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")


    tk.Button(janela_login, text="Login", command=login).grid(row=2, column=1)
    tk.Button(janela_login, text="Registrar", command=janela_registro).grid(row=3, column=1)

    janela_login.mainloop()
    return login_success[0]


#=======================================================================================================================================================================================
#                                                                  Janela 1 - DEFINIÇÃO DAS FUNÇÕES
#=======================================================================================================================================================================================
def iniciar_programa_principal():
    janela = tk.Tk()
    janela.title("Nossa casa")
    notebook = ttk.Notebook(janela, width= 680, height=510)
    notebook.pack(expand=True, fill='both')

    altura = 530
    largura = 680

    # Calculando a posição para centralizar a janela
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)

    # Definindo a geometria da janela
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
    # global janela


    def salvar():
        diaMesAno = label1_calendario.get_date()
        dataCompra_formatada = datetime.strptime(diaMesAno, "%m/%d/%y").strftime("%y/%m/%d")
        descricao = nome_label2.get()
        valor = nome_label3.get()
        if "," in valor:
            valor = valor.replace(",", ".")
        compraCasa_MYSQL = compraCasa.get()
        if compraCasa_MYSQL == 'Sim':
            compraCasa_MYSQL = 1
        else:
            compraCasa_MYSQL = 0
        quemPagou_MYSQL = quemComprou.get()
        Categoria = categoria.get()
        
        if descricao == "" or valor == "":
            tkinter.messagebox.showinfo('Erro','Dados insuficientes. Por favor preencher todos os campos')

        # Inseri os dados no banco.
        inserir_dados = f'''INSERT INTO gastos (diaMesAno, descricao, valor, compraCasa, quemPagou, Categoria) 
        VALUES (
        "{dataCompra_formatada}", "{descricao}", {valor}, "{compraCasa_MYSQL}", "{quemPagou_MYSQL}", "{Categoria}"
        )'''

        try:
            cursor.execute(inserir_dados)
            db.commit()
            tkinter.messagebox.showinfo('Compra','Compra cadastrada com sucesso.')
        except Exception as e:
            tkinter.messagebox.showinfo('Erro MySQL',f'Ocorreu um erro no MySQL: {e}')

    def Limpar():
        nome_label2.delete(0, END)
        nome_label3.delete(0, END)


    #=======================================================================================================================================================================================
    #                                                                  Janela 1 - CORPO O PROGRAMA
    #=======================================================================================================================================================================================
    Janela1 = ttk.Frame(notebook)

    label = ttk.Label(Janela1, font=('Arial', '18', 'bold'), background='orange', foreground='Black', text="Insira os dados da compra")
    label.place(x=200, y=0)

    labelBranco = ttk.Label(Janela1, text='')
    labelBranco.grid(row=0)
    labelBranco2 = ttk.Label(Janela1, text='')
    labelBranco2.grid(row=1)


    # Programa começa aqui. Primeiro Label referente à data da compra.
    label1 = ttk.Label(Janela1, text = "Data: ", font=('Arial', '14', 'bold'))
    label1.grid(row=2, column= 0, pady = 10, padx = 5,)
    label1_calendario = Calendar(Janela1, selecmode='day', year=2024, month=1, day=1)
    label1_calendario.grid(row=2, column=1, padx=0)

    # Segundo label referente à descrição
    label2 = ttk.Label(Janela1, text = "Descrição: ", font=('Arial', '14', 'bold'))
    label2.grid(row=3, column= 0, pady = 10, padx = 5,)
    nome_label2= tk.Entry(Janela1, width= 50, bg='#f76300', fg='white', font=('Arial', '12'))
    nome_label2.grid(row= 3, column=1, padx= 0)

    # Terceiro label referente ao valor do gasto
    label3 = ttk.Label(Janela1, text = "Valor: ", font=('Arial', '14', 'bold'))
    label3.grid(row=4, column= 0, pady = 10, padx = 5,)
    nome_label3= tk.Entry(Janela1, width= 50, bg='#f76300', fg='white', font=('Arial', '12'))
    nome_label3.grid(row= 4, column=1, padx= 0)


    # Quarto label responde se é uma compra da casa ou não. Levar uma caixa de 'Sim' ou Não', mas na inserção, inserir como 1 ou 0
    fCompraCasa =[
        'Sim',
        'Não'
    ]

    compraCasa = StringVar()
    compraCasa.set(fCompraCasa[0])

    label4 = ttk.Label(Janela1, text = "Compra da casa? ", font=('Arial', '14', 'bold'))
    label4.grid(row=5, column= 0, pady = 10, padx = 5,)
    nome_label4 = OptionMenu(Janela1, compraCasa, *fCompraCasa)
    nome_label4.grid(row= 5, column=1, padx= 0)


    # Quinta label deve apresentar uma caixa igual ao quarto label, com os valores: 'Alexandre', 'Camila', 'Extras'.
    fQuemComprou =[
        'Alexandre',
        'Camila',
        'Extras'
    ]

    quemComprou = StringVar()
    quemComprou.set(fQuemComprou[0])

    label5 = ttk.Label(Janela1, text = "Quem pagou? ", font=('Arial', '14', 'bold'))
    label5.grid(row=6, column= 0, pady = 10, padx = 5,)
    nome_label5= OptionMenu(Janela1, quemComprou, *fQuemComprou)
    nome_label5.grid(row= 6, column=1, padx= 0)

    # Sexto label deve apresentar uma caixa igual ao quarto label, com os valores: 'Mercado'...
    fCategoria =[
        'Mercado',
        'Conta',
        'Aluguel',
        'Decoração',
        'Saúde',
        'Mimos',
        'Outros - Casa',
        'Saida para comer',
        'Amigos',
        'Presentes'    
    ]

    categoria = StringVar()
    categoria.set(fCategoria[0])

    label6 = ttk.Label(Janela1, text = "Categoria: ", font=('Arial', '14', 'bold'))
    label6.grid(row=7, column= 0, pady = 10, padx = 5,)
    nome_label6= OptionMenu(Janela1, categoria, *fCategoria)
    nome_label6.grid(row= 7, column=1, padx= 0)


    #=======================================================================================================================================================================================
    #                                                                  Janela 1 - Botões de salvar e Limpar
    #=======================================================================================================================================================================================
    botaoSalvar = tk.Button(Janela1, text="Salvar", command=salvar, font=('Arial', '14', 'bold'))
    botaoSalvar.place(x='530', y='460')

    botaoLimpar = tk.Button(Janela1, text="Limpar", command=Limpar, font=('Arial', '14', 'bold'))
    botaoLimpar.place(x='100', y='460')


    #=======================================================================================================================================================================================
    #                                                                                JANELA 2
    #=======================================================================================================================================================================================

    # Janela 2 - Ganhos
    # Definição das funções
    def salvar_Janela2():
        diaMesAno_Janela2 = label1_calendario_Janela2.get_date()
        dataCompra_formatada_Janela2 = datetime.strptime(diaMesAno_Janela2, "%m/%d/%y").strftime("%y/%m/%d")
        descricao_Janela2 = nome_label2_Janela2.get()
        responsavel_Janela2 = quemGanhou.get()
        valor_Janela2 = nome_label4_Janela2.get()
        if "," in valor_Janela2:
            valor_Janela2 = valor_Janela2.replace(",", ".")
        
        if descricao_Janela2 == "" or valor_Janela2 == "":
            tkinter.messagebox.showinfo('Erro','Dados insuficientes. Por favor preencher todos os campos')

        # Inserir os dados no banco.
        inserir_dados_Janela2 = f'''INSERT INTO ganhos (diaMesAno, descricao, responsavel, valor) 
        VALUES (
        "{dataCompra_formatada_Janela2}", "{descricao_Janela2}", "{responsavel_Janela2}", {valor_Janela2}
        )'''

        try:
            cursor.execute(inserir_dados_Janela2)
            db.commit()
            tkinter.messagebox.showinfo('Ganho','Ganho cadastrado com sucesso.')
        except Exception as e:
            tkinter.messagebox.showinfo('Erro MySQL',f'Ocorreu um erro no MySQL: {e}')




    def Limpar_Janela2():
        nome_label2_Janela2.delete(0, END)
        nome_label4_Janela2.delete(0, END)




    #=======================================================================================================================================================================================
    #                                                                          JANELA 2 - Corpo do programa
    #=======================================================================================================================================================================================

    Janela2 = ttk.Frame(notebook)

    label = ttk.Label(Janela2, font=('Arial', '18', 'bold'), background='green', foreground='Black', text="Insira os ganhos de capital")
    label.place(x=200, y=0)

    labelBranco = ttk.Label(Janela2, text='')
    labelBranco.grid(row=0)
    labelBranco2 = ttk.Label(Janela2, text='')
    labelBranco2.grid(row=1)

    #------------------------------------------------------------------------------

    # Programa começa aqui. Primeiro Label referente à data que recebeu.
    label1_Janela2 = ttk.Label(Janela2, text = "Data: ", font=('Arial', '14', 'bold'))
    label1_Janela2.grid(row=2, column= 0, pady = 10, padx = 5,)
    label1_calendario_Janela2 = Calendar(Janela2, selecmode='day', year=2024, month=1, day=1)
    label1_calendario_Janela2.grid(row=2, column=1, padx=0)

    # Segundo label referente à descrição
    label2_Janela2 = ttk.Label(Janela2, text = "Descrição: ", font=('Arial', '14', 'bold'))
    label2_Janela2.grid(row=3, column= 0, pady = 10, padx = 5,)
    nome_label2_Janela2= tk.Entry(Janela2, width= 50, bg='#f76300', fg='white', font=('Arial', '12'))
    nome_label2_Janela2.grid(row= 3, column=1, padx= 0)

    # Terceiro label referente ao valor do gasto

    fQuemGanhou =[
        'Alexandre',
        'Camila',
        'Extras'
    ]

    quemGanhou = StringVar()
    quemGanhou.set(fQuemGanhou[0])

    label3_Janela2 = ttk.Label(Janela2, text = "Responsavel: ", font=('Arial', '14', 'bold'))
    label3_Janela2.grid(row=4, column= 0, pady = 10, padx = 5,)
    nome_label3_Janela2= OptionMenu(Janela2, quemGanhou, *fQuemGanhou)
    nome_label3_Janela2.grid(row= 4, column=1, padx= 0)

    # Quarto label referente ao valor do gasto
    label4_Janela2 = ttk.Label(Janela2, text = "Valor: ", font=('Arial', '14', 'bold'))
    label4_Janela2.grid(row=5, column= 0, pady = 10, padx = 5,)
    nome_label4_Janela2= tk.Entry(Janela2, width= 50, bg='#f76300', fg='white', font=('Arial', '12'))
    nome_label4_Janela2.grid(row= 5, column=1, padx= 0)


    #=======================================================================================================================================================================================
    #                                                                  Janela 2 - Botões de salvar e Limpar
    #=======================================================================================================================================================================================

    botaoSalvar = tk.Button(Janela2, text="Salvar", command=salvar_Janela2, font=('Arial', '14', 'bold'))
    botaoSalvar.place(x='530', y='460')

    botaoLimpar = tk.Button(Janela2, text="Limpar", command=Limpar_Janela2, font=('Arial', '14', 'bold'))
    botaoLimpar.place(x='100', y='460')


    #=======================================================================================================================================================================================
    #                                                                                  Janela 3
    #=======================================================================================================================================================================================
    #Inicio Janela 3
    Janela3 = ttk.Frame(notebook)

    label = ttk.Label(Janela3, font=('Arial', '18', 'bold'), background='green', foreground='Black', text="Gerar relatório em PDF")
    label.place(x=200, y=0)

    labelBranco = ttk.Label(Janela3, text='')
    labelBranco.grid(row=0)
    labelBranco2 = ttk.Label(Janela3, text='')
    labelBranco2.grid(row=1)



    #=======================================================================================================================================================================================
    #                                                                       Janela 3 - DEFINIÇÃO DAS FUNÇÕES
    #=======================================================================================================================================================================================
    def gerarPDF():
        
        diaMesAnoInicial = label1_calendario_Janela3.get_date()
        diaMesAnoFinal = label2_calendario_Janela3.get_date()
        dataCompra_formatada_Inicial = datetime.strptime(diaMesAnoInicial, "%m/%d/%y").strftime("%y/%m/%d")
        dataCompra_formatada_Final = datetime.strptime(diaMesAnoFinal, "%m/%d/%y").strftime("%y/%m/%d")
        filtroPagou = filtroQuemPagou.get()
        filtroCasa = filtroCompraCasa.get()
        filtroValor1 = filtroValor.get()
        filtroValor2 = nome_label5_1_Janela3.get()
        filtroCategoriaSelecionada = opcoesCategoria.curselection()
        valores_selecionados = [opcoesCategoria.get(index) for index in filtroCategoriaSelecionada]
        qry = f"SELECT descricao as 'Descrição do gasto', valor as 'Valor', case compraCasa when 1 then 'Sim' when 0 then 'Não' end as  'Compra da Casa', quemPagou as 'Quem Pagou',  Categoria FROM gastos where Categoria in ("
        i = 0
        while i < len(valores_selecionados):
            qry += f"'{valores_selecionados[i]}'"
            i += 1
            if i == len(valores_selecionados):
                continue
            else:
                qry += ', '
        qry += ") AND "

        if diaMesAnoFinal != diaMesAnoInicial:
            qry = qry + f"diaMesAno BETWEEN '{dataCompra_formatada_Inicial}' and '{dataCompra_formatada_Final}' AND"
        if filtroPagou != 'Tudo':
            qry = qry + f" quemPagou = '{filtroPagou}' AND"
        if filtroPagou == 'Tudo':
            qry = qry
        if filtroCasa == 'Somente Casa':
            qry = qry + f' compraCasa = 1 AND'
        if filtroCasa == 'Somente Sua':
            qry = qry + f' compraCasa = 0 AND'
        if filtroCasa == 'Tudo':
            qry = qry
        if filtroValor2:
            qry = qry + f' valor {filtroValor1} {filtroValor2} AND'

        qry_completa_1 = qry.split()
        qry_completa_1.pop()
        qry_completa = ' '.join(qry_completa_1)
        

        try:
            cursor.execute(qry_completa)
            resultados = cursor.fetchall()
            pdf_filename = "C:/Users/alexa/Desktop/Documento.pdf"
            c = canvas.Canvas(pdf_filename, pagesize=letter)
            y_position = 720
            c.drawAlignedString(100, 750, "Descrição")
            c.drawRightString(490, 750, "Valor")
            lista = []
            tracos = '-'
            for resultado in resultados:
                coluna_nome = resultado[0]
                coluna_gasto = str(resultado[1])
                lista.append(resultado[1])
                if y_position < 50:
                    c.showPage()
                    y_position = 720
                    c.drawAlignedString(100, 750, "Descrição")
                    c.drawRightString(490, 750, "Valor")
                c.drawString (80, y_position, f'{coluna_nome:-<70}')
                c.drawString (340, y_position, f'{tracos:-<30}')
                c.drawString (460, y_position, coluna_gasto)
                y_position -= 20
            contador = 0
            for numero in lista:
                contador += numero
            contador_total = str(round(contador, 2))
            y_position -= 10
            if y_position < 50:
                c.showPage()
                y_position = 720
            c.drawRightString(500, y_position, contador_total)
            c.drawRightString(70, y_position, 'Total')
            c.save()
            tkinter.messagebox.showinfo('Gerar PDF', 'PDF gerado com sucesso.')
        except Exception as e:
            tkinter.messagebox.showinfo('Erro MySQL',f'Ocorreu um erro no MySQL: {e}')

    #=======================================================================================================================================================================================
    #                                                                       Janela 3 - CORPO DO PROGRAMA
    #=======================================================================================================================================================================================
    #Label 1 e Label 2 referente a data de início e data final.
    label1_Janela3 = ttk.Label(Janela3, text = "Data Inicial: ", font=('Arial', '14', 'bold'))
    label1_Janela3.place(x='150', y= '45')
    label1_calendario_Janela3 = Calendar(Janela3, selecmode='day', year=2024, month=1, day=1)
    label1_calendario_Janela3.place(x='80', y= '70')

    label2_Janela3 = ttk.Label(Janela3, text = "Data Final: ", font=('Arial', '14', 'bold'))
    label2_Janela3.place(x='430', y= '45')
    label2_calendario_Janela3 = Calendar(Janela3, selecmode='day', year=2024, month=1, day=1)
    label2_calendario_Janela3.place(x= '350', y='70')


    # Terceiro label referente ao filtro de quem quer ver os gastos.
    fFiltroQuemPagou =[
        'Alexandre',
        'Camila',
        'Tudo'
    ]

    filtroQuemPagou = StringVar()
    filtroQuemPagou.set(fFiltroQuemPagou[0])

    label3_Janela3 = ttk.Label(Janela3, text = "Gastos de: ", font=('Arial', '14', 'bold'))
    label3_Janela3.place(x='0', y='270')
    nome_label3_Janela3 = OptionMenu(Janela3, filtroQuemPagou, *fFiltroQuemPagou)
    nome_label3_Janela3.place(x='110', y='270')

    # Quarto label referente ao filtro de gastos referente a você, casa ou tudo.
    fFiltroCompraCasa =[
        'Somente Casa',
        'Somente Sua',
        'Tudo'
    ]

    filtroCompraCasa = StringVar()
    filtroCompraCasa.set(fFiltroCompraCasa[0])

    label4_Janela3 = ttk.Label(Janela3, text = "Gastos relacionados a: ", font=('Arial', '14', 'bold'))
    label4_Janela3.place(x='0', y='310')
    nome_label4_Janela3 = OptionMenu(Janela3, filtroCompraCasa, *fFiltroCompraCasa)
    nome_label4_Janela3.place(x='225', y='310')

    # Quinto label referente ao filtro de valor
    fFiltroValor =[
        'Maior que',
        'Menor que',
        'Maior ou igual a',
        'Menor ou igual a'
    ]

    filtroValor = StringVar()
    filtroValor.set(fFiltroValor[0])

    label5_Janela3 = ttk.Label(Janela3, text = "Valor: ", font=('Arial', '14', 'bold'))
    label5_Janela3.place(x='0', y='350')
    nome_label5_Janela3 = OptionMenu(Janela3, filtroValor, *fFiltroValor)
    nome_label5_Janela3.place(x='70', y='350')
    nome_label5_1_Janela3 = tk.Entry(Janela3, width= 15, bg='gray', fg='white', font=('Arial', '12'))
    nome_label5_1_Janela3.place(x= '170', y='355')

    #Sexto label referente à categoria.
    label6_Janela3 = ttk.Label(Janela3, text = "Categoria: ", font=('Arial', '14', 'bold'))
    label6_Janela3.place(x='0', y='390')
    opcoesCategoria = tk.Listbox(Janela3, selectmode= tk.MULTIPLE, height=3)
    barra_rolagem = ttk.Scrollbar(Janela3, orient='vertical', command=opcoesCategoria.yview)
    opcoesCategoria.config(yscrollcommand=barra_rolagem.set)
    for opcao in fCategoria:
        opcoesCategoria.insert(tk.END, opcao)
    barra_rolagem.place(x='210', y='390')
    opcoesCategoria.place(x='105', y='390')


    #=======================================================================================================================================================================================
    #                                                                       Janela 3 - DEFINIÇÃO OS BOSTÕES
    #=======================================================================================================================================================================================
    # Botões de salvar e Limpar
    botaoGerarPDF = tk.Button(Janela3, text="Gerar PDF", command=gerarPDF, font=('Arial', '14', 'bold'))
    botaoGerarPDF.place(x='510', y='460')



    #=======================================================================================================================================================================================
    #                                                                                   Janela 4
    #=======================================================================================================================================================================================

    #Inicio Janela 4
    Janela4 = ttk.Frame(notebook)

    label = ttk.Label(Janela4, font=('Arial', '18', 'bold'), background='green', foreground='Black', text="Alterar dados cadastrados no sistema")
    label.place(x=130, y=0)

    labelBranco = ttk.Label(Janela4, text='')
    labelBranco.grid(row=0)
    labelBranco2 = ttk.Label(Janela4, text='')
    labelBranco2.grid(row=1)





    #=======================================================================================================================================================================================
    #                                                                       Janela 4 - DEFINIÇÃO DAS FUNÇÕES
    #=======================================================================================================================================================================================
    def on_select(event):
        selected_item = tree.focus()
        item_text = tree.item(selected_item, 'values')
        item_textId = item_text[0]
        return item_textId
        # salvar_Janela4(item_textId)
        # return item_textId2

    def on_coluna_selecionada(*args):
        coluna_selecionada = filtroColuna.get()
        if coluna_selecionada == "Valor" or coluna_selecionada == "Descrição":
            nome_label2_Entry_Janela4.config(state="normal")
            nome_label2_Casa_Janela4.place_forget()
            nome_label2_Option_Janela4.place_forget()
            nome_label2_Calendar_Janela4.place_forget()
            nome_label2_QComprou_Janela4.place_forget()
            nome_label2_Entry_Janela4.place(x= '75', y='320')
        elif coluna_selecionada == "Categoria":
            nome_label2_Entry_Janela4.place_forget()
            nome_label2_Calendar_Janela4.place_forget()
            nome_label2_QComprou_Janela4.place_forget()
            nome_label2_Casa_Janela4.place_forget()
            nome_label2_Option_Janela4.place(x= '75', y='310')
            nome_label2_Option_Janela4.config(state="normal")
        elif coluna_selecionada == "Data":
            nome_label2_Casa_Janela4.place_forget()
            nome_label2_Calendar_Janela4.place(x='75', y= '310')
            nome_label2_Calendar_Janela4.config(state='normal')
        elif coluna_selecionada == "CompraCasa":
            nome_label2_Entry_Janela4.place_forget()
            nome_label2_Calendar_Janela4.place_forget()
            nome_label2_Option_Janela4.place_forget()
            nome_label2_QComprou_Janela4.place_forget()
            nome_label2_Casa_Janela4.place(x= '75', y='310')
            nome_label2_Casa_Janela4.config(state="normal")
        else:
            nome_label2_Entry_Janela4.place_forget()
            nome_label2_Calendar_Janela4.place_forget()
            nome_label2_Option_Janela4.place_forget()
            nome_label2_QComprou_Janela4.place(x= '75', y='310')
            nome_label2_QComprou_Janela4.config(state="normal")

    def salvar_Janela4():
        linha_selecionada_resultado = on_select(None)
        filtroColuna_Janela4 = filtroColuna.get()
        try:
            if filtroColuna_Janela4 == "Descrição":
                valor_Janela4 = nome_label2_Entry_Janela4.get()
                qrySalvarJanela4 = f"UPDATE GASTOS SET descricao = '{valor_Janela4}' WHERE idGastos = {linha_selecionada_resultado}"
                cursorJanela4.execute(qrySalvarJanela4)
                db.commit()
                tkinter.messagebox.showinfo('Update',f'{filtroColuna_Janela4} atualizado com sucesso.')
            elif filtroColuna_Janela4 == "Valor":
                valor_Janela4 = nome_label2_Entry_Janela4.get()
                if "," in valor_Janela4:
                    valor_Janela4 = valor_Janela4.replace(",", ".")
                qrySalvarJanela4 = f'UPDATE GASTOS SET valor = {valor_Janela4} WHERE idGastos = {linha_selecionada_resultado}'
                cursorJanela4.execute(qrySalvarJanela4)
                db.commit()
                tkinter.messagebox.showinfo('Update',f'{filtroColuna_Janela4} atualizado com sucesso.') 
            elif filtroColuna_Janela4 == 'Data':            
                valor_Janela4 = nome_label2_Calendar_Janela4.get_date()
                dataCompra_formatada_Janela4 = datetime.strptime(valor_Janela4, "%m/%d/%y").strftime("%y/%m/%d")
                qrySalvarJanela4 = f"UPDATE GASTOS SET diaMesAno = '{dataCompra_formatada_Janela4}' WHERE idGastos = {linha_selecionada_resultado}"
                cursorJanela4.execute(qrySalvarJanela4)
                db.commit()
                tkinter.messagebox.showinfo('Update',f'{filtroColuna_Janela4} atualizado com sucesso.')
            elif filtroColuna_Janela4 == 'CompraCasa':
                valor_Janela4 = compraCasa_Janela4.get()
                if valor_Janela4 == "Sim":
                    valor_Janela4 = 1
                else:
                    valor_Janela4 = 0
                qrySalvarJanela4 = f'UPDATE GASTOS SET compraCasa = {valor_Janela4} WHERE idGastos = {linha_selecionada_resultado}'
                cursorJanela4.execute(qrySalvarJanela4)
                db.commit()
                tkinter.messagebox.showinfo('Update',f'{filtroColuna_Janela4} atualizado com sucesso.')
            elif filtroColuna_Janela4 == 'QuemPagou':
                valor_Janela4 = quemComprou_Janela4.get()
                qrySalvarJanela4 = f"UPDATE GASTOS SET quemPagou = '{valor_Janela4}' WHERE idGastos = {linha_selecionada_resultado}"
                cursorJanela4.execute(qrySalvarJanela4)
                db.commit()
                tkinter.messagebox.showinfo('Update',f'{filtroColuna_Janela4} atualizado com sucesso.')
            elif filtroColuna_Janela4 == 'Categoria':
                valor_Janela4 = categoria_Janela4.get()
                qrySalvarJanela4 = f"UPDATE GASTOS SET Categoria = '{valor_Janela4}' WHERE idGastos = {linha_selecionada_resultado}"
                cursorJanela4.execute(qrySalvarJanela4)
                db.commit()
                tkinter.messagebox.showinfo('Update',f'{filtroColuna_Janela4} atualizado com sucesso.')
        except Exception as e:
            tkinter.messagebox.showinfo('Erro MySQL',f'Ocorreu um erro no MySQL: {e}')

    # TODO # SERIA LEGAL COLOCAR UM BOTÂO DE "REBUILD" PARA CARREGAR OS DADOS SEM QUE TENHA QUE FECHAR O PROGRAMA.
    def recarregar_dados():
        # Limpar a Treeview
        for item in tree.get_children():
            tree.delete(item)
        
        # Carregar os dados novamente do banco de dados
        cursor_qry_id.execute(qry_id)
        resultados_qry_id = cursor_qry_id.fetchall()
        fFiltroId = [id[0] for id in resultados_qry_id]

        cursor_qry_data.execute(qry_data)
        resultados_qry_data = cursor_qry_data.fetchall()
        fFiltrodata = [data[0] for data in resultados_qry_data]

        cursor_qry_desc.execute(qry_desc)
        resultados_qry_desc = cursor_qry_desc.fetchall()
        fFiltrodesc = [descricao[0] for descricao in resultados_qry_desc]

        cursor_qry_valor.execute(qry_valor)
        resultados_qry_valor = cursor_qry_valor.fetchall()
        fFiltrovalor_qry = [valor[0] for valor in resultados_qry_valor]

        cursor_qry_casa.execute(qry_casa)
        resultados_qry_casa = cursor_qry_casa.fetchall()
        fFiltrocasa = [casa[0] for casa in resultados_qry_casa]

        cursor_qry_qPagou.execute(qry_qPagou)
        resultados_qry_qPagou = cursor_qry_qPagou.fetchall()
        fFiltroqPagou = [qPagou[0] for qPagou in resultados_qry_qPagou]

        cursor_qry_categoria.execute(qry_categoria)
        resultados_qry_categoria = cursor_qry_categoria.fetchall()
        fFiltroCategoria = [categoria[0] for categoria in resultados_qry_categoria]

        # Inserir os novos dados na Treeview
        for i in range(len(fFiltroId)):
            tree.insert("", tk.END, text=i, values=(fFiltroId[i], fFiltrodata[i], fFiltrodesc[i], fFiltrovalor_qry[i], fFiltrocasa[i], fFiltroqPagou[i], fFiltroCategoria[i]))


    #=======================================================================================================================================================================================
    #                                                                        Janela 4 - CORPO DO PROGRAMA
    #=======================================================================================================================================================================================
    # Início da tabela
    tree = ttk.Treeview(Janela4,columns=("ID","Data", "Descrição", "Valor", "CompraCasa", "QuemPagou", "Categoria"), height = 10)

    # Definir os cabeçalhos das colunas
    tree.heading("#0", text="nRegistro")
    tree.heading("#1", text="idGastos")
    tree.heading("#2", text="Data")
    tree.heading("#3", text="Descrição")
    tree.heading("#4", text="Valor")
    tree.heading("#5", text="CompraCasa")
    tree.heading("#6", text="QuemPagou")
    tree.heading("#7", text="Categoria")

    qry_id = "select idGastos from gastos"
    cursor_qry_id.execute(qry_id)
    resultados_qry_id = cursor_qry_id.fetchall()
    fFiltroId = []
    for id in resultados_qry_id:
        fFiltroId.append(id)

    qry_data = "select date_format(diaMesAno, '%d/%m/%Y')  as Data from gastos"
    cursor_qry_data.execute(qry_data)
    resultados_qry_data = cursor_qry_data.fetchall()
    fFiltrodata = []
    for data in resultados_qry_data:
        fFiltrodata.append(data)

    qry_desc = "select descricao from gastos"
    cursor_qry_desc.execute(qry_desc)
    resultados_qry_desc = cursor_qry_desc.fetchall()
    fFiltrodesc = []
    for descricao in resultados_qry_desc:
        fFiltrodesc.append(descricao)

    qry_valor = "select valor from gastos"
    cursor_qry_valor.execute(qry_valor)
    resultados_qry_valor = cursor_qry_valor.fetchall()
    fFiltrovalor_qry = []
    for valor in resultados_qry_valor:
        fFiltrovalor_qry.append(valor)

    qry_casa = "select case compraCasa when 1 then 'Sim' when 0 then 'Não' end from gastos"
    cursor_qry_casa.execute(qry_casa)
    resultados_qry_casa = cursor_qry_casa.fetchall()
    fFiltrocasa = []
    for casa in resultados_qry_casa:
        fFiltrocasa.append(casa)

    qry_qPagou = "select quemPagou from gastos"
    cursor_qry_qPagou.execute(qry_qPagou)
    resultados_qry_qPagou = cursor_qry_qPagou.fetchall()
    fFiltroqPagou = []
    for qPagou in resultados_qry_qPagou:
        fFiltroqPagou.append(qPagou)

    qry_categoria = "select Categoria from gastos"
    cursor_qry_categoria.execute(qry_categoria)
    resultados_qry_categoria = cursor_qry_categoria.fetchall()
    fFiltroCategoria = []
    for categoria_Janela4 in resultados_qry_categoria:
        fFiltroCategoria.append(categoria_Janela4)

    for i in range(len(fFiltroId)):
        tree.insert("", tk.END, text=[i], values=(fFiltroId[i] ,fFiltrodata[i], fFiltrodesc[i], fFiltrovalor_qry[i], fFiltrocasa[i], fFiltroqPagou[i], fFiltroCategoria[i]))

    # Posicionar e redimensionar a Treeview usando place()
    tree.place(x=10, y=50, width= 660)

    # Label 2 - Coluna-----------------
    fFiltroColuna =[
        'Data',
        'Descrição',
        'Valor',
        'CompraCasa',
        'QuemPagou',
        'Categoria'
    ]

    filtroColuna = StringVar()
    filtroColuna.set(fFiltroColuna[0])

    # ---- DEFINIÇÂO PARA ATUALIZAÇÂO ATUOMÁTICA
    filtroColuna = tk.StringVar()
    filtroColuna.set(fFiltroColuna[0])
    filtroColuna.trace("w", on_coluna_selecionada)

    label2_Janela4 = ttk.Label(Janela4, text = "Coluna: ", font=('Arial', '14', 'bold'))
    label2_Janela4.place(x='9', y='280')
    nome_label2_Janela4 = OptionMenu(Janela4, filtroColuna, *fFiltroColuna)
    nome_label2_Janela4.place(x='90', y='280')

    # Label 3 ------------------------
    label3_Janela4 = ttk.Label(Janela4, text = "Valor: ", font=('Arial', '14', 'bold'))
    label3_Janela4.place(x='9', y='315')

    # Entry para o valor
    nome_label2_Entry_Janela4 = tk.Entry(Janela4, width=15, bg='gray', fg='white', font=('Arial', '12'))

    # OptionMenu para a categoria
    fCategoria_Janela4 =[
    'Mercado',
    'Conta',
    'Aluguel',
    'Decoração',
    'Saúde',
    'Mimos',
    'Outros - Casa',
    'Saida para comer',
    'Amigos',
    'Presentes'    
    ]
    categoria_Janela4 = StringVar()
    categoria_Janela4.set(fCategoria_Janela4[0])
    nome_label2_Option_Janela4 = OptionMenu(Janela4, categoria_Janela4, *fCategoria_Janela4)
    nome_label2_Option_Janela4.place(x= '75', y='310')
    nome_label2_Option_Janela4.config(state="normal")

    # OptionMenu para a CompraCasa
    fCompraCasa_Janela4 =[
        'Sim',
        'Não'
    ]

    compraCasa_Janela4 = StringVar()
    compraCasa_Janela4.set(fCompraCasa_Janela4[0])
    nome_label2_Casa_Janela4 = OptionMenu(Janela4, compraCasa_Janela4, *fCompraCasa_Janela4)
    nome_label2_Casa_Janela4.place(x= '75', y='310')
    nome_label2_Casa_Janela4.config(state="normal")

    # OptionMenu para QuemComprou
    fQuemComprou_Janela4 =[
        'Alexandre',
        'Camila'
    ]

    quemComprou_Janela4 = StringVar()
    quemComprou_Janela4.set(fQuemComprou_Janela4[0])
    nome_label2_QComprou_Janela4 = OptionMenu(Janela4, quemComprou_Janela4, *fQuemComprou_Janela4)
    nome_label2_QComprou_Janela4.place(x= '75', y='310')
    nome_label2_QComprou_Janela4.config(state="normal")

    # Calendario para Data
    nome_label2_Calendar_Janela4 = Calendar(Janela4, selecmode='day', year=2024, month=1, day=1)
    nome_label2_Calendar_Janela4.place(x='75', y= '310')
    nome_label2_Calendar_Janela4.config(state='normal')

    tree.bind('<<TreeviewSelect>>', on_select)

    #=======================================================================================================================================================================================
    #                                                                        Janela 4 - DEFINIÇÃO DOS BOTÕES
    #=======================================================================================================================================================================================
    botão_salvar_Janela4 = tk.Button(Janela4, text="SALVAR", command=salvar_Janela4, font=('Arial', '14', 'bold'))
    botão_salvar_Janela4.place(x='540', y='370')

    botão_atualizar_Janela4 = tk.Button(Janela4, text="ATUALIZAR", command=recarregar_dados, font=('Arial', '14', 'bold'))
    botão_atualizar_Janela4.place(x='525', y='415')


    #=======================================================================================================================================================================================
    #                                                                               FIM DO PROGRAMA
    #=======================================================================================================================================================================================
    Janela1.pack(fill= tk.BOTH, expand=True)
    Janela2.pack(fill= tk.BOTH, expand=True)
    Janela3.pack(fill= tk.BOTH, expand=True)
    Janela4.pack(fill= tk.BOTH, expand=True)
    notebook.add(Janela1, text = "Gastos")
    notebook.add(Janela2, text = "Ganhos")
    notebook.add(Janela3, text = "Gerador de PDF")
    notebook.add(Janela4, text = 'Alterar Cadastros')
    notebook.pack()
    janela.mainloop()



# janela_login()
while True:
    if janela_login():
        iniciar_programa_principal()
        break
    else:    
        fechar_programa = messagebox.askquestion('Fechar programa', 'Você realmente deseja fechar o programa?')
        if fechar_programa == 'yes':
            break
        else:
            continue