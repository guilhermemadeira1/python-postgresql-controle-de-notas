from AlunoCRUD import AlunoCRUD

crud = AlunoCRUD()

while True:
    print("== Sistema de controle de notas ==\n")
    print("\t> Digite 1 para registar aluno")
    print("\t> Digite 2 para deletar aluno")
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
            print("[REMOÇÂO DE ALUNO]")
            matricula = int(input("Digite a matricula: "))
            if(crud.deletar_aluno(matricula)):
                print("Aluno removido com sucesso!")

        case "x":
            break

        
