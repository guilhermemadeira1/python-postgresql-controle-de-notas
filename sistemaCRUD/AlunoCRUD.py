import psycopg2

# classe para registrar, buscar, atualizar e deletar alunos no banco de dados
class AlunoCRUD:

	# retorna a conexao com o banco de dados
	def obter_conexao(self):
		try:
			conexao = psycopg2.connect(
				host="localhost",
				database="escola",
			    user="postgres",
				password="12345"
			)
			return conexao
		
		except psycopg2.Error as e:
			print(f"Não foi possível se conectar ao banco de dados: {e}")
			# None indica retorno inválido
			return None 
			
	# registrar aluno no banco de dados
	def registrar_aluno(self, nome, curso):
		try:
			conexao = self.obter_conexao()
			with conexao.cursor() as cursor:
				insert = "INSERT INTO alunos(nome, curso) VALUES (%s, %s);"
				cursor.execute(insert,(nome, curso))
				conexao.commit()
				return True

		except psycopg2.Error as e:
			print(f"Erro ao registrar o aluno: {e}")
			return False

		finally:
			conexao.close()
	
	# deletar aluno do banco de dados
	def deletar_aluno(self, matricula):
		try:
			conexao = self.obter_conexao()
			with conexao.cursor() as cursor:
				delete = "DELETE FROM alunos WHERE matricula = %s"
				cursor.execute(delete,(matricula,))
				if cursor.rowcount == 0: # se a quantidade de registros afetados no banco de dados for 0
					print("Nenhum registro foi deletado.")
					return False
				conexao.commit()
			return True
		
		except psycopg2.Error as e:
			print(f"Erro ao deletar o aluno.\n{e}")
	
		finally:
			if conexao:
				conexao.close()

	# buscar registro de aluno pela matricula
	def buscar_aluno(self, matricula):
		try:
			conexao = self.obter_conexao()
			with conexao.cursor() as cursor:
				select = """SELECT a.matricula, a.nome, c.nome, a.nota1, a.nota2 
						 	FROM alunos a JOIN curso c ON a.curso = c.id_curso
							WHERE matricula = %s;
						 """
				cursor.execute(select,(matricula,))
				resultado = cursor.fetchone()
				if resultado:
					return resultado
				else:
					return None
				
		except psycopg2.Error as e:
			print(f"Erro ao realizar a busca: {e}")
			return None

		finally:
			if conexao:
				conexao.close()

	# buscar todos os registros de alunos
	def buscar_todos(self):
		try:
			conexao = self.obter_conexao()
			with conexao.cursor() as cursor:
				select = "SELECT * FROM alunos"
				cursor.execute(select)
				resultado = cursor.fetchall()
				if resultado:
					return resultado
				else:
					return None
				
		except psycopg2.Error as e:
			print(f"Erro ao realizar a busca: {e}")
			return False

		finally:
			if conexao:
				conexao.close()

	# atualizar notas de alunos
	def atualizar_notas(self, matricula_aluno, nota1, nota2):
		try:
			conexao = self.obter_conexao()
			with conexao.cursor() as cursor:
				update = "UPDATE alunos SET nota1 = %s, nota2 = %s WHERE matricula = %s"
				cursor.execute(update, (nota1, nota2, matricula_aluno))
				
				if cursor.rowcount == 0: # se a quantidade de registros afetados no banco de dados for 0
					print("Nenhum registro foi encontrado para atualizar.")
					return False
				
				conexao.commit()
			return True

		except psycopg2.Error as e:
			print(f"Erro ao realizar a atualização:: {e}")
			return False

		finally:
			if conexao:
				conexao.close()

	def matricular_aluno(self, matricula_aluno, curso):
		try:
			conexao = self.obter_conexao()
			with conexao.cursor() as cursor:
				update = "INSERT INTO aluno_curso(matricula_aluno, id_curso) VALUES (%s,%s);"
				cursor.execute(update,(matricula_aluno,curso))
				conexao.commit()
				return True
		except psycopg2.Error as e:
			print(f"Erro ao matricular o aluno ao curso: {e}")
			return False

		finally:
			conexao.close()

if __name__ == "__main__":
	crud = AlunoCRUD()

while True:
    print("== Sistema de controle de notas ==")
    print("\t> Digite 1 para registar aluno")
    print("\t> Digite 2 para listar alunos")
    print("\t> Digite 3 para atualizar notas")
    print("\t> Digite 4 para deletar aluno")
    print("\t> Digite x para encerrar o programa\n")
    escolha = input("Qual operação deseja realizar? ")

    match escolha:
        case "1":
            print("[REGISTRO DE ALUNO]")
            matricula = int(input("Digite a matricula: "))
            nome = input("Digite o nome: ")
            nota1 = float(input("Digite a nota 1: "))
            nota2 = float(input("Digite a nota 2: "))
        
            if(crud.registrar_aluno(matricula, nome, nota1, nota2)):
                print("Registro feito com sucesso!")
                print(f" > Matricula: {matricula}\n > Nome: {nome}\n > Nota 1: {nota1}\n > Nota 2: {nota2}")
        case "2":
            listagem = crud.buscar_todos()
            print("[LISTAGEM DE ALUNOS]")
            if listagem:
                print("MATRICULA\tNOME\tNOTA1\tNOTA2")
                for aluno in listagem:
                    print(f"{aluno[0]}\t\t{aluno[1]}\t{aluno[2]}\t{aluno[3]}")
        case "3":
            print("[ATUALIZAR NOTAS]")
            matricula = int(input("Digite a matricula do aluno que será atualizado:"))
            nota1 = float(input("Digite a nota1: "))
            nota2 = float(input("Digite a nota2: "))
            if(crud.deletar_aluno(matricula,nota1,nota2)):
                print("Atualização realizada com sucesso!")
        case "4":
            print("[REMOÇÂO DE ALUNO]")
            matricula = int(input("Digite a matricula do aluno que será removido: "))
            if(crud.deletar_aluno(matricula)):
                print("Aluno removido com sucesso!")

        case "x": break
            

        