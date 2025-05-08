import tkinter as tk
from tkinter import ttk

from sistemaCRUD import Aluno, AlunoCRUD, BancoDeDados

def limpar_treeview():
    for registro in tree_view.get_children():
        tree_view.delete(registro)
    
def carregar_treeview():
    tuplas = crud.buscar_todos_alunos()
    alunos = []
    for t in tuplas:
        # o objeto aluno calcula a media e a situacao ao ser instanciado
        aluno = Aluno(t[0],t[1],t[2],t[3],t[4]) 
        alunos.append(aluno)
    for a in alunos:
        # values recebe uma tupla com os dados dos alunos
        media = a.calcular_media()
        situacao = a.verificar_situacao()
        tree_view.insert("", tk.END, values=(a.matricula,a.nome,a.curso,a.nota1,a.nota2,media,situacao))

def registrar_entradas(entrada_nome, entrada_sobrenome, entrada_curso):
    nome = entrada_nome.get()+" "+entrada_sobrenome.get()
    curso = crud.buscar_id_curso(entrada_curso.get())
    crud.registrar_aluno(nome,curso)
    limpar_treeview()
    carregar_treeview()

def registrar_notas(matricula, nota1, nota2):
    crud.atualizar_notas(matricula, nota1,nota2)
    limpar_treeview()
    carregar_treeview()

def remover_aluno(entrada_matricula):
    crud.deletar_aluno(entrada_matricula.get())
    limpar_treeview()
    carregar_treeview()

def abrir_janela():
    nova_janela = tk.Toplevel(root)
    nova_janela.title("Atualizar notas")
    nova_janela.geometry("300x200")
    tk.Label(nova_janela, text="Sistema de Notas", font="Arial", bg="lightblue").grid(row=0,column=0)
    tk.Label(nova_janela, text="Registrar Notas ").grid(row=1,column=0)

    tk.Label(nova_janela, text="Matricula: ").grid(row=2,column=0)
    entrada_matricula = tk.Entry(nova_janela)
    entrada_matricula.grid(row=2,column=1)
    
    tk.Label(nova_janela, text="Nota1: ").grid(row=3,column=0)
    entrada_nota1 = tk.Entry(nova_janela)
    entrada_nota1.grid(row=3,column=1)

    tk.Label(nova_janela, text="Nota2: ").grid(row=4,column=0)
    entrada_nota2 = tk.Entry(nova_janela)
    entrada_nota2.grid(row=4,column=1)

    botao_atualizar = tk.Button(nova_janela,text="Atualizar", command= lambda: registrar_notas(entrada_matricula.get(), entrada_nota1.get(), entrada_nota2.get()))
    botao_atualizar.grid(row=5,column=1)

if __name__ == "__main__":
    # conexao com o banco
    banco = BancoDeDados()
    banco.criar_tabelas()

    if(banco.tabela_cursos_vazia()):
        banco.inserir_cursos()
        
    crud = AlunoCRUD()

    # interface tkinter
    root = tk.Tk() 
    root.title("Janela Guilherme")
    root.geometry("900x500")

    root.config(bg="#93B8BE")

    #resize width, height = False
    #root.resizable(False,False)

    tk.Label(root, text="Sistema de Notas", font="Arial", bg="#93B8BE").grid(row=0,column=0)

    # espaço
    tk.Label(text="",bg="#93B8BE").grid(row=1,column=0)

    tk.Label(root, text="Registro de aluno ",font="Arial",bg="#93B8BE").grid(row=2,column=0)

    tk.Label(root, text="Nome: ",bg="#93B8BE").grid(row=3,column=0)
    entrada_nome = tk.Entry(root)
    entrada_nome.grid(row=3,column=1)

    tk.Label(root, text="Sobrenome: ",bg="#93B8BE").grid(row=4,column=0)
    entrada_sobrenome = tk.Entry(root)
    entrada_sobrenome.grid(row=4,column=1)

    # cursos
    tk.Label(root, text="Curso: ", bg="#93B8BE").grid(row=8, column=0)
    cursos = []
    for curso in crud.buscar_cursos():
        cursos.append(curso[1])

    combobox_curso = ttk.Combobox(root, values=cursos, width=17)
    combobox_curso.grid(row=8,column=1)

    # espaço
    tk.Label(text="", bg="#93B8BE").grid(row=9,column=0)
   
    tk.Button(text="Atualizar notas",command=abrir_janela, bg="#EADF66").grid(row=10,column=0)
    tk.Button(text="Registrar",command=lambda: registrar_entradas(entrada_nome, entrada_sobrenome, combobox_curso), bg="#66EA76").grid(row=10,column=1)

    # espaço
    tk.Label(text="", bg="#93B8BE").grid(row=11,column=0)

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
    carregar_treeview()

    # remover
    tk.Label(text="Remover aluno (insira a matrícula): ", bg="#93B8BE").grid(row=13,column=0)
    entrada_matricula = tk.Entry(root)
    entrada_matricula.grid(row=13,column=1)
    tk.Button(text="Remover", command=remover_aluno, bg="#EA6666").grid(row=13,column=2)

    root.mainloop()


