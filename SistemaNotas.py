import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

# ============== classes ==================

#classe para gerenciar dados de alunos
class Aluno:
	def __init__(self, matricula, nome, curso, nota1, nota2):
		self.matricula = matricula
		self.nome = nome
		self.curso = curso
		self.nota1 = nota1
		self.nota2 = nota2
		
	def calcular_media(self):
		return (self.nota1+self.nota2)/2
	
	def verificar_situacao(self):
		if self.nota1 and self.nota2:
			media = self.calcular_media()
			if media >=6:
				return "APROVADO"
			elif media >=4:
				return "RECUPERACAO"
			else:
				return "REPROVADO"
		else:
			return ""

# =============== funções ==================

# retorna conexao com o banco de dados
def obter_conexao():
	try:
		conexao = psycopg2.connect(
			host="localhost",
			database="escola",
			user="postgres",
			password="12345",
		)
		return conexao
		
	except psycopg2.Error as e:
		print(f"Erro ao conectar ao banco de dados: {e}")
		# None indica retorno inválido
		return None
		
# cria as tabelas alunos e cursos 
def criar_tabelas():
	try:
		conexao = obter_conexao()
		if conexao:
			with conexao.cursor() as cursor:
				cursor.execute("""
				CREATE TABLE IF NOT EXISTS cursos(
				   	id_curso SERIAL PRIMARY KEY,
				   	nome VARCHAR(100) NOT NULL,
					carga_horaria int NOT NULL
				);
		     	CREATE TABLE IF NOT EXISTS alunos
		     	(
		         	matricula SERIAL PRIMARY KEY,
		          	nome VARCHAR(100) NOT NULL,
				   	curso INT NOT NULL,
		          	nota1 DECIMAL(2,1) DEFAULT 0.0 NOT NULL,
		        	nota2 DECIMAL(2,1) DEFAULT 0.0 NOT NULL,
				   	FOREIGN KEY(curso) REFERENCES cursos(id_curso)
		     	);
				"""
		   	 	)
			conexao.commit()
			# True indica operação realizada com sucesso
			return True
			
	except psycopg2.Error as e:
		print(f"Erro ao criar as tabelas: {e}")
		# False indica erro na operação
		return False
		
	finally:
		conexao.close()

# registra cursos no banco de dados
def inserir_cursos():
	try:
		conexao = obter_conexao()
		with conexao.cursor() as cursor:
			insert = "INSERT INTO cursos(nome, carga_horaria) VALUES(%s,%s);"
			cursos = [
				("Matemática",80),
				("História",60),
				("Língua portuguesa",80),
				("Química",70),
		 	    ("Física",70),
				("Biologia",80),
				("Informática",80)
            ]
			cursor.executemany(insert,cursos)
			conexao.commit()
					
	except psycopg2.Error as e:
		print(f"Erro ao gerar os registros na tabela cursos: {e}")
			
	finally:
		if conexao:
			conexao.close()
			
# verifica se a tabela cursos esta vazia 
def tabela_cursos_vazia():
	try:
		conexao = obter_conexao()
		with conexao.cursor() as cursor:
			cursor.execute("SELECT * FROM CURSOS")
			resultado = cursor.fetchone()
			if(resultado is None):
					return True
			else:
				return False
				
	except psycopg2.Error as e:
		print(f"Erro ao verificar tabela cursos: {e}")
			
	finally:
		if conexao:
			conexao.close()
	
# registra aluno no banco de dados
def registrar_aluno(nome, curso):
	try:
		conexao = obter_conexao()
		with conexao.cursor() as cursor:
			insert = "INSERT INTO alunos(nome, curso) VALUES (%s, %s);"
			cursor.execute(insert,(nome, curso))
			conexao.commit()
			print("Aluno registrado com suceso!")
			return True

	except psycopg2.Error as e:
		print(f"Erro ao registrar o aluno: {e}")
		return False

	finally:
		conexao.close()
	
# deleta aluno do banco de dados
def deletar_aluno(matricula):
	try:
		conexao = obter_conexao()
		with conexao.cursor() as cursor:
			delete = "DELETE FROM alunos WHERE matricula = %s"
			cursor.execute(delete,(matricula,))
			if cursor.rowcount == 0: # se a quantidade de registros afetados no banco de dados for 0
				print("Nenhum registro foi deletado.")
				return False
				
			print("Aluno removido com suceso!")
			conexao.commit()
		return True
		
	except psycopg2.Error as e:
		print(f"Erro ao deletar o aluno.\n{e}")
	
	finally:
		if conexao:
			conexao.close()

# busca registro de aluno pela matricula
def buscar_aluno(matricula):
	try:
		conexao = obter_conexao()
		with conexao.cursor() as cursor:
			select = """SELECT a.matricula, a.nome, c.nome, a.nota1, a.nota2 
						 	FROM alunos a JOIN cursos c ON a.curso = c.id_curso
							WHERE matricula = %s;
						 """
			cursor.execute(select,(matricula,))
			resultado = cursor.fetchone()
			if resultado:
				return resultado
			else:
				return None
				
	except psycopg2.Error as e:
		print(f"Erro ao buscar o aluno: {e}")
		return None

	finally:
		if conexao:
			conexao.close()

# buscar todos os registros de alunos
def buscar_todos_alunos():
	try:
		conexao = obter_conexao()
		with conexao.cursor() as cursor:
			select = """SELECT a.matricula, a.nome, c.nome, a.nota1, a.nota2 
					 	FROM alunos a JOIN cursos c ON a.curso = c.id_curso
					"""
			cursor.execute(select)
			resultado = cursor.fetchall()
			if resultado:
					return resultado
			else:
				return None
				
	except psycopg2.Error as e:
		print(f"Erro ao buscar todos os alunos: {e}")
		return None

	finally:
		if conexao:
			conexao.close()

# atualiza a nota1 do aluno
def atualizar_nota1(matricula_aluno, nota1):
	try:
		conexao = obter_conexao()
		nota = float(nota1)
		with conexao.cursor() as cursor:
			update = "UPDATE alunos SET nota1 = %s WHERE matricula = %s"
			cursor.execute(update, (nota1, matricula_aluno))
			conexao.commit()
			print("Nota1 atualizada com sucesso!")
			return True
		
	except psycopg2.Error as e:
		print(f"Erro ao atualizar nota1: {e}")
		return False

	finally:
		if conexao:
			conexao.close()

# atualiza a nota2 do aluno
def atualizar_nota2(matricula_aluno, nota2):
	try:
		conexao = obter_conexao()
		with conexao.cursor() as cursor:
			update = "UPDATE alunos SET nota2 = %s WHERE matricula = %s"
			cursor.execute(update, (nota2, matricula_aluno))
			conexao.commit()
			print("Nota2 atualizada com sucesso!")
			return True
	except psycopg2.Error as e:
		print(f"Erro ao atualizar nota2: {e}")
		return False
	
	finally:
		if conexao:
			conexao.close()

# busca um registro de curso pelo id
def buscar_curso(id_curso):
	try:
		conexao = obter_conexao()
		with conexao.cursor() as cursor:
			select = "SELECT nome FROM CURSOS WHERE id_curso = %s"
			cursor.execute(select,(id_curso,))
			return cursor.fetchone() # retorna o id da tupla do curso
				
	except psycopg2.Error as e:
		print(f"Erro ao buscar os cursos: {e}")
			
	finally:
		if conexao:
			conexao.close()

# buscar todos os cursos
def buscar_cursos():
	try:
		conexao = obter_conexao()
		with conexao.cursor() as cursor:
			cursor.execute("SELECT * FROM CURSOS")
			return cursor.fetchall() # retorna lista de cursos
				
	except psycopg2.Error as e:
		print(f"Erro ao buscar os cursos: {e}")
			
	finally:
		conexao.close()

# busca o id do curso pelo nome
def buscar_id_curso(nome_curso):
	try:
		conexao = obter_conexao()
		with conexao.cursor() as cursor:
			select = "SELECT id_curso FROM CURSOS WHERE nome = %s"
			cursor.execute(select,(nome_curso,))
			return cursor.fetchone() # retorna o id da tupla do curso
				
	except psycopg2.Error as e:
		print(f"Erro ao buscar os cursos: {e}")
			
	finally:
		if conexao:
			conexao.close()
		
# exibe as tuplas do banco de dados na interface
def carregar_treeview():
	tuplas = buscar_todos_alunos() # retorna os regitros do banco de dados como tuplas
	if tuplas:
		alunos = []
		for t in tuplas:
			aluno = Aluno(t[0],t[1],t[2],t[3],t[4]) # cria objeto Aluno com os dados das tuplas
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
	if entrada_nome.get() and entrada_sobrenome.get() and entrada_curso.get():
		try:
			nome_aluno = entrada_nome.get()+" "+entrada_sobrenome.get()
			id_curso = buscar_id_curso(entrada_curso.get())
			confirma = messagebox.askyesno(
				title="REGISTRO",
				message=f"Deseja matricular o aluno {nome_aluno.upper()} no\ncurso de {entrada_curso.get().upper()}?"
			)
			if confirma:
				if (registrar_aluno(nome_aluno,id_curso)):
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

	if matricula == "" and nota1 == "" and nota2 == "":
		messagebox.showerror("ERRO", message="Preencha ao menos um campo de nota.")
		
	elif matricula != "" and matricula.isdigit():
		matr = int(matricula)
		matriculas_cadastradas = []
		for a in buscar_todos_alunos():
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
							message=f"Deseja atualizar a NOTA1 do aluno {buscar_aluno(matr)[1].upper()} para {n1}?"
						)
						if confirma:
							if atualizar_nota1(matr, n1):
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
							message=f"Deseja atualizar a NOTA2 do aluno {buscar_aluno(matr)[1].upper()} para {n2}?"
						)
						if confirma:
							if atualizar_nota2(matr, n2):
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
	if matricula:
		if matricula.isdigit():
			matr = int(matricula)
			matriculas_cadastradas = []
			for a in buscar_todos_alunos():
				matriculas_cadastradas.append(a[0])

			if matr in matriculas_cadastradas:
				nome_aluno = buscar_aluno(matricula)[1].upper()
				nome_curso = buscar_aluno(matricula)[2].upper()
				confirma = messagebox.askyesno(
						title="REMOÇÃO DE ALUNO", 
						message=f'Deseja remover o aluno {nome_aluno}\ndo curso de "{nome_curso}" ?'
				)
				if confirma:
					try:
						deletar_aluno(matr)
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

def salvar_dados():
	alunos = buscar_todos_alunos()
	confirma = messagebox.askyesno(
		title="SALVAR",
		message="Deseja salvar os registros de alunos?"
	)
	if confirma:
		with open("dados_alunos.txt","w") as arquivo:
			for a in alunos:
				colunas = "MATRICULA\tNOME\tCURSO\t"
				linha = "\t".join(map(str,a))+"\n"
				arquivo.write(linha)

			messagebox.showinfo(title="SALVAR",message="Dados salvos com sucesso!")	
			print("dados salvos!")

# abre nova janela para inserir as notas
def abrir_janela():
	nova_janela = tk.Toplevel(root)
	nova_janela.title("Atualizar notas")
	nova_janela.geometry("300x200")
	nova_janela.config(bg=cores["azul"]) 
	
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

# =============== interface ===================
if __name__ == "__main__":
	try:
		#cria as tabelas
		criar_tabelas()

		# insere os cursos na tabela cursos se estiver vazia
		if(tabela_cursos_vazia()):
			inserir_cursos()

	except Exception as e:
			messagebox.showerror(title="ERRO", message=f"Erro de conxeão com o banco de dados\n{e}")
	
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
	root.geometry("900x500")
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
	for curso in buscar_cursos():
		cursos.append(curso[1])

	combobox_curso = ttk.Combobox(root, values=cursos, width=17)
	combobox_curso.grid(row=8,column=1)

    # espaço
	tk.Label(root,text="", bg=cores["azul"]).grid(row=9,column=0)
   
	tk.Button(root, text="Atualizar notas",command=abrir_janela, bg="#EADF66").grid(row=10,column=0)
	tk.Button(root,text="Registrar",command=lambda: registrar_entradas(entrada_nome, entrada_sobrenome, combobox_curso), bg=cores["verde"]).grid(row=10,column=1)
    # espaçamento
	tk.Label(root,text="", bg=cores["azul"]).grid(row=11,column=0)

    # exibição dos registros de alunos com média e situação escolar
	colunas = ("MATRICULA","NOME","CURSO","NOTA1","NOTA2","MEDIA","SITUAÇAO")
	tree_view = ttk.Treeview(root,columns=colunas, show="headings")

	for col in colunas:
		tree_view.heading(col, text=col)

	tree_view.column("MATRICULA", width=90)
	tree_view.column("NOME", width=90)
	tree_view.column("CURSO", width=100)
	tree_view.column("NOTA1", width=70)
	tree_view.column("NOTA2", width=70)
	tree_view.column("MEDIA", width=70)
	tree_view.column("SITUAÇAO", width=90)

	tree_view.grid(row=12,column=1)
	tk.Button(root,text="salvar",command=salvar_dados, bg=cores["verde"]).grid(row=13,column=3)
	carregar_treeview()

    # remover aluno
	tk.Label(text="Remover aluno (insira a matrícula): ", bg=cores["azul"]).grid(row=13,column=0)
	entrada_matricula = tk.Entry(root)
	entrada_matricula.grid(row=13,column=1)
	tk.Button(text="Remover", command=lambda: remover_aluno_entrada(entrada_matricula.get()), bg=cores["vermelho"]).grid(row=13,column=2)

	root.mainloop()


