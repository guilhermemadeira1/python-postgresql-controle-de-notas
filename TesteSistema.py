from sistemaCRUD.AlunoCRUD import AlunoCRUD
from sistemaCRUD.Aluno import Aluno, Curso

crud = AlunoCRUD()

while True:
    print("== Sistema de controle de notas ==\n")
    print("\t> Digite 1 para registar aluno")
    print("\t> Digite 2 para listar alunos")
    print("\t> Digite 3 para atualizar notas")
    print("\t> Digite 4 para deletar aluno")
    print("\t> Digite x para encerrar o programa\n")
    escolha = int(input("Qual operação deseja realizar? "))

    match escolha:
        case 1:
            print("[REGISTRO DE ALUNO]")
            matricula = int(input("Digite a matricula: "))
            nome = input("Digite o nome: ")
            nota1 = float(input("Digite a nota 1: "))
            nota2 = float(input("Digite a nota 2: "))
        
            if(crud.registrar_aluno(matricula, nome, nota1, nota2)):
                print("Registro feito com sucesso!")
                print(f" > Matricula: {matricula}\n > Nome: {nome}\n > Nota 1: {nota1}\n > Nota 2: {nota2}")
        case 2:
            listagem = crud.buscar_todos()
            print("[LISTAGEM DE ALUNOS]")
            if listagem:
                print("MATRICULA\tNOME\tNOTA1\tNOTA2")
                for aluno in listagem:
                    print(f"{aluno[0]}\t\t{aluno[1]}\t{aluno[2]}\t{aluno[3]}")
        case 3:
            print("[ATUALIZAR NOTAS]")
            matricula = int(input("Digite a matricula do aluno que será atualizado:"))
            nota1 = float(input("Digite a nota1: "))
            nota2 = float(input("Digite a nota2: "))
            if(crud.deletar_aluno(matricula,nota1,nota2)):
                print("Atualização realizada com sucesso!")
        case 4:
            print("[REMOÇÂO DE ALUNO]")
            matricula = int(input("Digite a matricula do aluno que será removido: "))
            if(crud.deletar_aluno(matricula)):
                print("Aluno removido com sucesso!")

        case "x","X":
            break

        
