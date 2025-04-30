import tkinter as tk
from tkinter import ttk

from sistemaCRUD import Aluno
from sistemaCRUD import AlunoCRUD
from sistemaCRUD import BancoDeDados

def exibirDados():
    matricula = entrada_matricula.get()
    nome = entrada_nome.get()
    nota1 = entrada_nota1.get()
    nota2 = entrada_nota2.get()

    a = Aluno(matricula,nome,nota1,nota2)
    print(f"Aluno {a.nome}\nMatricula: {a.matricula}\nNota1: {a.nota1}\nNota2: {a.nota2}")

if __name__ == "__main__":

    # conexao com o banco
    banco = BancoDeDados()
    banco.criar_tabelas()
    banco.inserir_cursos()

    crud = AlunoCRUD()

    aluno1 = Aluno(matricula=1221, nome="Joao", nota1=12.1, nota2=21.2)
    crud.matricular_aluno(matricula_aluno=aluno1.matricula,curso=1)

    # interface tkinter
    root = tk.Tk() 
    root.title("Janela Guilherme")

    #resize width, height = False
    #root.resizable(False,False)

    tk.Label(text="Registro de aluno: ").grid(row=0,column=0)

    tk.Label(root, text="Matricula: ").grid(row=1,column=0)
    entrada_matricula = tk.Entry(root)
    entrada_matricula.grid(row=1,column=1)


    tk.Label(root, text="Nome: ").grid(row=2,column=0)
    entrada_nome = tk.Entry(root)
    entrada_nome.grid(row=2,column=1)


    tk.Label(root, text="Nota1: ").grid(row=3,column=0)
    entrada_nota1 = tk.Entry(root)
    entrada_nota1.grid(row=3,column=1)

    tk.Label(root, text="Nota2: ").grid(row=4,column=0)
    entrada_nota2 = tk.Entry(root)
    entrada_nota2.grid(row=4,column=1)

    #genero 
    tk.Label(root, text="Gênero do aluno: ").grid(row=5,column=0)

    options = ("Masculino", "Feminino")
    combobox = ttk.Combobox(root,values=options,height=5).grid(row=5,column=1)


    #operacoes
    but1 = tk.Button(text="Registrar",command=crud.registrar_aluno).grid(row=8,column=0)
    but1 = tk.Button(text="Remover", command=crud.deletar_aluno).grid(row=9,column=0)

    msg = tk.Message(root, text="Esta é uma mensagem\n\nPulou linha") 
    msg.config(bg="lightblue")

    msg.grid(row=10, column=0)
    root.mainloop()


