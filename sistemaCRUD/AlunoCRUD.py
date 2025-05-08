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
				print("Aluno registrado com suceso!")
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
				
				print("Aluno removido com suceso!")
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
			print(f"Erro ao realizar a busca: {e}")
			return None

		finally:
			if conexao:
				conexao.close()

	# buscar todos os registros de alunos
	def buscar_todos_alunos(self):
		try:
			conexao = self.obter_conexao()
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
			print(f"Erro ao realizar a busca: {e}")
			return None

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
				print("Notas atualizadas com sucesso!")
				conexao.commit()
			return True

		except psycopg2.Error as e:
			print(f"Erro ao realizar a atualização:: {e}")
			return False

		finally:
			if conexao:
				conexao.close()

	def buscar_curso(self, id_curso):
		try:
			conexao = self.obter_conexao()
			with conexao.cursor() as cursor:
				select = "SELECT nome FROM CURSOS WHERE id_curso = %s"
				cursor.execute(select,(id_curso,))
				return cursor.fetchone() # retorna o id da tupla do curso
				
		except psycopg2.Error as e:
			print(f"Erro ao buscar os cursos: {e}")
			
		finally:
			conexao.close()

	# buscar todos os cursos
	def buscar_cursos(self):
		try:
			conexao = self.obter_conexao()
			with conexao.cursor() as cursor:
				cursor.execute("SELECT * FROM CURSOS")
				return cursor.fetchall() # retorna lista de cursos
				
		except psycopg2.Error as e:
			print(f"Erro ao buscar os cursos: {e}")
			
		finally:
			conexao.close()

	# buscar id do curso pelo nome
	def buscar_id_curso(self, nome_curso):
		try:
			conexao = self.obter_conexao()
			with conexao.cursor() as cursor:
				select = "SELECT id_curso FROM CURSOS WHERE nome = %s"
				cursor.execute(select,(nome_curso,))
				return cursor.fetchone() # retorna o id da tupla do curso
				
		except psycopg2.Error as e:
			print(f"Erro ao buscar os cursos: {e}")
			
		finally:
			conexao.close()

