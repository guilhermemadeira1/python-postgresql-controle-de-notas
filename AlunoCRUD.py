import psycopg2

# classe para registrar, buscar, atualizar e deletar alunos no banco de dados
class AlunoCRUD:

	# conectar ao banco
	def obter_conexao(self):
		try:
			conexao = psycopg2.connect(
				host="localhost",
				database="escola",
			    user="postgres",
				password="12345"
			)
			print("Conexao com o banco de dados realizada com sucesso!")
			return conexao
		
		except Exception as e:
			print(f"Não foi possível se conectar ao banco de dados.\n{e}")
			
	# criar tabela alunos
	def criar_tabela(self):
		try:
			conexao = self.obter_conexao()
			cursor = conexao.cursor()
			cursor.execute("""
		      CREATE TABLE IF NOT EXISTS alunos
		      (
		           matricula SERIAL PRIMARY KEY,
		           nome VARCHAR(100) NOT NULL,
		           nota1 DECIMAL(3,2) NOT NULL,
		           nota2 DECIMAL(3,2) NOT NULL
		      );"""
		    )
			conexao.commit()
			return True
		
		except Exception as e:
			print(f"Não foi possivel criar a tabela de alunos.\nERRO: {e}")
			return False
		
		finally:
			if cursor:
				cursor.close()
			if conexao:
				conexao.close()
			
	#registrar aluno no banco de dados
	def registrar_aluno(self, matricula, nome, nota1, nota2):
		try:
			conexao = self.obter_conexao()
			cursor = conexao.cursor()
			insert = "INSERT INTO alunos(matricula,nome,nota1,nota2) VALUES (%s, %s, %s, %s);"
			cursor.execute(insert,(matricula, nome, nota1, nota2))
			conexao.commit()
			return True
		
		except Exception as e:
			print(f"Não foi possível registrar o aluno.\n{e}")
			return False
		
		finally:
			if cursor:
				cursor.close()
			if conexao:
				conexao.close()
	
	#deletar aluno do banco de dados
	def deletar_aluno(self, matricula):
		try:
			conexao = self.obter_conexao()
			cursor = conexao.cursor()
			delete = "DELETE FROM alunos WHERE matricula = %s"
			cursor.execute(delete,(matricula))
			conexao.commit()
			return True
		
		except Exception as e:
			print(f"Não foi possível deletar o aluno.\n{e}")
			return False
		
		finally:
			if cursor:
				cursor.close()
			if conexao:
				conexao.close()
			
	def buscar_aluno(self, matricula):
		pass
	def buscar_todos(self):
		pass
	def atualizar_nota1(self, matricula):
		pass
	def atualizar_nota2(self, matricula):
		pass
		
