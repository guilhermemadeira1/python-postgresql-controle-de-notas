import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from banco import Banco
from aluno import Aluno

import pandas as pd

# exibe as tuplas do banco de dados na interface
def carregar_treeview():
	banco = Banco()
	tuplas = banco.buscar_todos_alunos() # retorna os regitros do banco de dados como tuplas
	if tuplas:
		alunos = []
		for t in tuplas:
			aluno = Aluno( # cria objeto Aluno com os dados das tuplas
				matricula = t[0],
				nome = t[1],
				curso = t[2],
				nota1 = t[3],
				nota2 = t[4],
			 )
			alunos.append(aluno)
		for a in alunos:
			media = a.calcular_media()
			situacao = a.verificar_situacao()
			# insere os dados na interface
			tree_view.insert("", tk.END, values=(a.matricula,a.nome,a.curso,a.nota1,a.nota2,media,situacao))

# apaga as tuplas exibidas na tela
def limpar_treeview():
    for registro in tree_view.get_children():
        tree_view.delete(registro)

# registra os dados de entrada nome, sobrenome e curso e atualiza a tela
def registrar_entradas(entrada_nome, entrada_sobrenome, entrada_curso):
	banco = Banco() 

	if entrada_nome.get() and entrada_sobrenome.get() and entrada_curso.get():
		try:
			nome_aluno = entrada_nome.get()+" "+entrada_sobrenome.get()
			id_curso = banco.buscar_id_curso(entrada_curso.get())
			confirma = messagebox.askyesno(
				title="REGISTRO",
				message=f"Deseja matricular o aluno {nome_aluno.upper()} no\ncurso de {entrada_curso.get().upper()}?"
			)
			if confirma:
				if (banco.registrar_aluno(nome_aluno,id_curso)):
					messagebox.showinfo(title="REGISTRO",message=f"Aluno matriculado com sucesso!")
					limpar_treeview()
					carregar_treeview()
				else:
					messagebox.showerror(title="ERRO",message="Não foi possível registrar o aluno.")
			
		except Exception as e:
			print(f"Erro ao registrar aluno:{e}")
			messagebox.showerror(title="ERRO",message=f"Erro ao registrar aluno:\n{e}")
	else:
		messagebox.showerror(title="ERRO", message="Preeencha todos os campos de registro.")

# registra os dados de entrada matricula, nota1 e nota2 e atualiza a tela
def registrar_notas(matricula, nota1, nota2):
	banco = Banco()

	if matricula == "" and nota1 == "" and nota2 == "":
		messagebox.showerror("ERRO", message="Preencha ao menos um campo de nota.")
		
	elif matricula != "" and matricula.isdigit():
		matr = int(matricula)
		matriculas_cadastradas = []
		for a in banco.buscar_todos_alunos():
			matriculas_cadastradas.append(a[0])
		
		if matr in matriculas_cadastradas:
			if nota1 == "" and nota2 == "":
				messagebox.showerror("ERRO",message="Preencha ao menos um campo de nota.")

			if nota1 != "":
				try:
					n1 = float(nota1)
					if n1 >-1 and n1 <=10:
						confirma = messagebox.askyesno(
							title="ATUALIZAÇÃO",
							message=f"Deseja atualizar a NOTA1 do aluno {banco.buscar_aluno(matr)[1].upper()} para {n1}?"
						)
						if confirma:
							if banco.atualizar_nota1(matr, n1):
								messagebox.showinfo(title="ATUALIZAÇAO",message="Nota1 atualizada com sucesso!")
							else:
								messagebox.showerror(title="ERRO", message="Erro ao atualizar a nota1.")
					else:
						messagebox.showerror(title="ERRO", message="Insira uma nota entre 0.0 a 10.0")
				except ValueError:
						messagebox.showerror(title="ERRO",message="Insira um valor numérico no campo nota1.")

			if nota2 != "":
				try:
					n2 = float(nota2)
					if n2 >-1 and n2 <=10:
						confirma = messagebox.askyesno(
							title="ATUALIZAÇÃO",
							message=f"Deseja atualizar a NOTA2 do aluno {banco.buscar_aluno(matr)[1].upper()} para {n2}?"
						)
						if confirma:
							if banco.atualizar_nota2(matr, n2):
								messagebox.showinfo(title="ATUALIZAÇAO",message="Nota2 atualizada com sucesso!")
							else:
								messagebox.showerror(title="ERRO", message="Erro ao atualizar a nota2.")
					else:
						messagebox.showerror(title="ERRO", message="Insira uma nota entre 0.0 a 10.0")
				except ValueError:
						messagebox.showerror(title="ERRO", message="Insira um valor numérico no campo nota2.")
		else:
			messagebox.showerror("ERRO",message=f"A matrícula {matr} não existe.")
	else:
		messagebox.showerror("ERRO",message="Insira uma matrícula válida.")


	limpar_treeview()
	carregar_treeview()

# remove aluno e atualiza a tela
def remover_aluno_entrada(matricula):
	banco = Banco()

	if matricula:
		if matricula.isdigit():
			matr = int(matricula)
			matriculas_cadastradas = []
			for a in banco.buscar_todos_alunos():
				matriculas_cadastradas.append(a[0])

			if matr in matriculas_cadastradas:
				nome_aluno = banco.buscar_aluno(matricula)[1].upper()
				nome_curso = banco.buscar_aluno(matricula)[2].upper()
				confirma = messagebox.askyesno(
						title="REMOÇÃO DE ALUNO", 
						message=f'Deseja remover o aluno {nome_aluno}\ndo curso de "{nome_curso}" ?'
				)
				if confirma:
					try:
						banco.deletar_aluno(matr)
						limpar_treeview()
						carregar_treeview()
							
					except Exception as e:
						print(e)
						messagebox.showerror(title="ERRO", message=e)
			else:
				messagebox.showerror(title="ERRO",message="Matrícula não encontrada.")
		else:
			messagebox.showerror(title="ERRO", message='Insira um valor numérico na entrada "REMOVER ALUNO"')
	else:
		messagebox.showerror(title="ERRO",message='Insira uma matrícula na entrada "REMOVER ALUNO"' )

# persistir dados em um arquivo
def salvar_dados():
	banco = Banco()

	confirma = messagebox.askyesno(
		title="SALVAR",
		message="Deseja salvar os registros de alunos?"
	)
	if confirma:
		lista_alunos = banco.buscar_todos_alunos()
		formatos = [
			("arquivo de texto",".txt"),
			("arquivo csv",".csv")
		]
		colunas = ["MATRICULA","NOME","CURSO","NOTA1","NOTA2","MEDIA","SITUACAO"]

		novo_arquivo = filedialog.asksaveasfile(defaultextension=".txt",filetypes=formatos)

		if novo_arquivo.name.endswith(".txt"): # o atributo novo_arquivo.name informa o caminho do arquivo

			with open(novo_arquivo.name,"a") as arquivo:
				campos = "\t".join(colunas)+"\n"
				arquivo.write(campos)
				for matricula, nome, curso, nota1, nota2 in lista_alunos:
					aluno = Aluno(
						matricula = matricula,
						nome = nome,
						curso = curso,
						nota1 = nota1,
						nota2 = nota2,
					)
					dados = vars(aluno).values()
					linha = "\t".join(map(str,dados))+"\n"
					arquivo.write(linha)
					print(linha,end="")

				messagebox.showinfo(title="SALVAR",message="Dados salvos com sucesso!\n")	
				print("dados salvos com sucesso!")

		if novo_arquivo.name.endswith(".csv"):
			dados = []
			for matricula, nome, curso, nota1, nota2 in lista_alunos:
				aluno = Aluno(
					matricula = matricula,
					nome = nome,
					curso = curso,
					nota1 = nota1,
					nota2 = nota2,
				)
				dados.append(vars(aluno).values())
				
			dataframe_alunos = pd.DataFrame(data=dados,columns=colunas)
			dataframe_alunos.to_csv(novo_arquivo.name,index=False)

			messagebox.showinfo(title="SALVAR",message="Dados salvos com sucesso!\n")	
			print("dados salvos com sucesso!")

# abre nova janela para inserir as notas
def abrir_janela():
	nova_janela = tk.Toplevel(root)
	nova_janela.title("Atualizar notas")
	nova_janela.geometry("330x230")
	nova_janela.config(bg=cores["azul"])
	nova_janela.resizable(False, False)
	
	tk.Label(nova_janela, text="Atualizar notas", font="Arial", bg=cores["azul"]).grid(row=0,column=0)
	# espaçamento
	tk.Label(nova_janela, text="", bg=cores["azul"]).grid(row=1,column=0)
	
	tk.Label(nova_janela, text="Matricula: ", bg=cores["azul"]).grid(row=2,column=0)
	entrada_matricula = tk.Entry(nova_janela)
	entrada_matricula.grid(row=2,column=1)
    
	tk.Label(nova_janela, text="Nota1: ", bg=cores["azul"]).grid(row=3,column=0)
	entrada_nota1 = tk.Entry(nova_janela)
	entrada_nota1.grid(row=3,column=1)
	
	tk.Label(nova_janela, text="Nota2: ", bg=cores["azul"]).grid(row=4,column=0)
	entrada_nota2 = tk.Entry(nova_janela)
	entrada_nota2.grid(row=4,column=1)
	# espaçamento
	tk.Label(nova_janela, text="", bg=cores["azul"]).grid(row=5,column=0)
	tk.Label(nova_janela, text="", bg=cores["azul"]).grid(row=6,column=0)
	tk.Label(nova_janela, text="", bg=cores["azul"]).grid(row=7,column=0)

	# mensagem
	tk.Message(
		nova_janela, 
		text="Para aprovação, a média do aluno deve ser seperior ou igual a 6.",
		width=200
	).grid(row=8, column=1)

	botao_atualizar = tk.Button(
		nova_janela, 
		text = "atualizar",
		bg = cores["amarelo"],
		command= lambda: registrar_notas(
			entrada_matricula.get(),
			entrada_nota1.get(),
			entrada_nota2.get()
		)
	)
	botao_atualizar.grid(row=6,column=1)

# selecionar uma linha da tree view
def selecionar_linha(evento):
	# obtem a linha selecionada
	linha = tree_view.selection()
	if linha:
		# obtem o valor da matricula da linha selecionada
		dados = tree_view.item(linha)["values"]
		matricula = dados[0]
		# atualiza o campo remover aluno com a matricula
		entrada_matricula.delete(0, tk.END) # delete(posição inicial da str, posicao final da str)
		entrada_matricula.insert(0, matricula) # insert(posição inicial da str, valor acrescentado)

# =============== interface ===================
if __name__ == "__main__":

	# instancia objeto com as operações do banco
	banco = Banco()
	try:
		#cria as tabelas do banco se não existirem
		banco.criar_tabelas()

		# insere os registros na tabela cursos se estiver vazia
		if banco.tabela_cursos_vazia() == True:
			banco.inserir_cursos()

		# insere registros na tabela alunos estiver vazia
		if banco.tabela_alunos_vazia() == True:
			banco.inserir_alunos()

	except Exception as e:
			messagebox.showerror(title="ERRO", message=f"Erro\n{e}")
	
	# cores de fundo
	cores = {
		"azul":"#93B8BE", 
		"amarelo":"#EADF66",
		"vermelho":"#EA6666",
		"verde":"#66EA76"
	}

	# janela principal
	root = tk.Tk() 
	root.title("Sistema de controle de notas escolares")
	root.geometry("970x520")
	root.config(bg=cores["azul"])
	
    # titulo
	tk.Label(root, text="Controle de notas", font="Arial", bg=cores["azul"]).grid(row=0,column=0)
	
	# espaçamento
	tk.Label(text="",bg=cores["azul"]).grid(row=1,column=0)
	tk.Label(root, text="Registro de aluno ",font="Arial",bg=cores["azul"]).grid(row=2,column=0)

    # campo inserir nome
	tk.Label(root, text="Nome: ",bg=cores["azul"]).grid(row=3,column=0)
	entrada_nome = tk.Entry(root)
	entrada_nome.grid(row=3,column=1)

    # campo inserir sobrenome
	tk.Label(root, text="Sobrenome: ",bg=cores["azul"]).grid(row=4,column=0)
	entrada_sobrenome = tk.Entry(root)
	entrada_sobrenome.grid(row=4,column=1)

    # campo inserir curso
	tk.Label(root, text="Curso: ", bg=cores["azul"]).grid(row=8, column=0)
	cursos = []
	for curso in banco.buscar_todos_cursos():
		cursos.append(curso[1])

	combobox_curso = ttk.Combobox(root, values=cursos, width=17)
	combobox_curso.grid(row=8,column=1)

    # espaço
	tk.Label(root,text="", bg=cores["azul"]).grid(row=9,column=0)

	# botão registrar aluno
	tk.Button(root,text="Registrar",command=lambda: registrar_entradas(entrada_nome, entrada_sobrenome, combobox_curso), bg=cores["verde"]).grid(row=10,column=1)

    # espaçamento
	tk.Label(root,text="", bg=cores["azul"]).grid(row=11,column=0)

	# botão atualizar notas
	tk.Button(root, text="Atualizar notas",command=abrir_janela, bg="#EADF66").grid(row=11,column=0)

    # exibição dos registros de alunos com média e situação escolar
	colunas = ("MATRICULA","NOME","CURSO","NOTA1","NOTA2","MEDIA","SITUAÇAO")
	tree_view = ttk.Treeview(root,columns=colunas, show="headings")

	for col in colunas:
		tree_view.heading(col, text=col)

	tree_view.column("MATRICULA", width=90)
	tree_view.column("NOME", width=120)
	tree_view.column("CURSO", width=100)
	tree_view.column("NOTA1", width=70)
	tree_view.column("NOTA2", width=70)
	tree_view.column("MEDIA", width=70)
	tree_view.column("SITUAÇAO", width=90)

	tree_view.grid(row=12,column=1)
	carregar_treeview()

	# ativa uma ação na treeview quando uma linha for selecionada com o botao esquerdo do mouse
	tree_view.bind(sequence="<ButtonRelease-1>", func= selecionar_linha)

    # remover aluno
	tk.Label(text="Remover aluno (insira a matrícula): ", bg=cores["azul"]).grid(row=14,column=0)
	entrada_matricula = tk.Entry(root)
	entrada_matricula.grid(row=14,column=1)
	tk.Button(text="Remover", command=lambda: remover_aluno_entrada(entrada_matricula.get()), bg=cores["vermelho"]).grid(row=15,column=1)

	# salvar dados
	tk.Label(root,text="Salvar dados: ", bg=cores["azul"]).grid(row=14,column=2)
	tk.Button(root,text="salvar",command=salvar_dados, bg=cores["verde"]).grid(row=14,column=3)

	root.mainloop()
