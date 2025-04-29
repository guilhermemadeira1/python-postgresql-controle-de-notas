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
			return conexao
		
		except Exception as e:
			print(f"Não foi possível se conectar ao banco de dados: {e}")
			# None indica retorno inválido
			return None 
			
	# criar tabela alunos
	def criar_tabela(self):
		try:
			conexao = self.obter_conexao()
			with conexao.cursor() as cursor:
				cursor.execute("""
		     	 	CREATE TABLE IF NOT EXISTS alunos
		     		 (
		         		matricula SERIAL PRIMARY KEY,
		          		nome VARCHAR(100) NOT NULL,
		          		nota1 DECIMAL(3,2) NOT NULL,
		        		nota2 DECIMAL(3,2) NOT NULL
		     	 	)"""
		   	 	)
				conexao.commit()
			# True indica operação realizada com sucesso
			return True
		
		except Exception as e:
			print(f"Erro ao criar a tabela de alunos: {e}")
			# False indica errp na operação
			return False
		
		finally:
			if conexao:
				conexao.close()
			
	# registrar aluno no banco de dados
	def registrar_aluno(self, matricula, nome, nota1, nota2):
		try:
			conexao = self.obter_conexao()
			with conexao.cursor() as cursor:
				insert = "INSERT INTO alunos(matricula,nome,nota1,nota2) VALUES (%s, %s, %s, %s);"
				cursor.execute(insert,(matricula, nome, nota1, nota2))
				conexao.commit()
				return True

		except Exception as e:
			print(f"Erro ao registrar o aluno: {e}")
			return False

		finally:
			if conexao:
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
		
		except Exception as e:
			print(f"Erro ao deletar o aluno.\n{e}")
	
		finally:
			if conexao:
				conexao.close()

	# buscar registro de aluno pela matricula
	def buscar_aluno(self, matricula):
		try:
			conexao = self.obter_conexao()
			with conexao.cursor() as cursor:
				select = "SELECT * FROM alunos WHERE matricula = %s"
				cursor.execute(select,(matricula,))
				resultado = cursor.fetchone()
				if resultado:
					return resultado
				else:
					return None
				
		except Exception as e:
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
				
		except Exception as e:
			print(f"Erro ao realizar a busca: {e}")
			return False

		finally:
			if conexao:
				conexao.close()

	# atualizar notas de alunos
	def atualizar_notas(self, matricula, nota1, nota2):
		try:
			conexao = self.obter_conexao()
			with conexao.cursor() as cursor:
				update = "UPDATE alunos SET nota1 = %s, nota2 = %s WHERE matricula = %s"
				cursor.execute(update, (nota1, nota2, matricula,))
				
				if cursor.rowcount == 0: # se a quantidade de registros afetados no banco de dados for 0
					print("Nenhum registro foi encontrado para atualizar.")
					return False
				
				conexao.commit()
			return True

		except Exception as e:
			print(f"Erro ao realizar a atualização:: {e}")
			return False

		finally:
			if conexao:
				conexao.close()

