import psycopg2
import random
from datetime import datetime

# classe para gerenciar conexao e as tabelas no banco de dados
class Banco:
	def obter_conexao(self):
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
	def criar_tabelas(self):
		try:
			conexao = self.obter_conexao()
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
						nota1 DECIMAL(3,1) DEFAULT 0.0 NOT NULL,
						nota2 DECIMAL(3,1) DEFAULT 0.0 NOT NULL,
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

	# insere cursos no banco de dados
	def inserir_cursos(self):
		try:
			conexao = self.obter_conexao()
			with conexao.cursor() as cursor:
				insert = "INSERT INTO cursos(nome, carga_horaria) VALUES(%s,%s);"
				cursos = [
					("Matemática",80),
					("História",60),
					("Português",80),
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

	# insere alunos no banco de dados
	def inserir_alunos(self):
		try:
			conexao = self.obter_conexao()
			with conexao.cursor() as cursor:
				insert = "INSERT INTO alunos(matricula,nome,curso,nota1,nota2) VALUES (%s,%s,%s,%s,%s)"
				alunos = [
					("João Pedro", 1, 8, 7.5),
					("Maria Eduarda", 2, 5.5, 9),
					("Gabriel da Silva", 7, 2, 10),
					("Felipe das Neves", 4, 7.5, 6),
					("Juliana Fernanda", 7, 10, 9.5),
					("Miguel Pereira", 3, 10, 9.5),
					("Manuela Souza", 2, 7, 8),
					("Altair Nogueira", 6, 10, 10),
				]
				alunos_com_matricula = []
				for nome, curso, nota1, nota2 in alunos:
					ano = datetime.now().strftime("%Y")
					numeros_aleatorios = [str(random.randint(0,9)) for _ in range(5)]
					matricula = int(ano+"".join(numeros_aleatorios))
					alunos_com_matricula.append((matricula, nome, curso, nota1, nota2))
						
				cursor.executemany(insert,alunos_com_matricula)
				conexao.commit()

		except psycopg2.Error as e:
			print(f"Erro ao inserir alunos: {e}")
		
		finally:
			if conexao:
				conexao.close()
				
	# verifica se a tabela cursos esta vazia 
	def tabela_cursos_vazia(self):
		try:
			conexao = self.obter_conexao()
			with conexao.cursor() as cursor:
				cursor.execute("SELECT * FROM cursos")
				resultado = cursor.fetchone()
				if resultado is None:
					return True
				else:
					return False
				
		except psycopg2.Error as e:
			print(f"Erro ao verificar tabela cursos:\n{e}")
				
		finally:
			if conexao:
				conexao.close()

	# verifica se a tabela alunos esta vazia
	def tabela_alunos_vazia(self):
		try:
			conexao = self.obter_conexao()
			with conexao.cursor() as cursor:
				cursor.execute("SELECT * FROM alunos")
				resultado = cursor.fetchone()
				if resultado is None:
					return True
				else:
					return False
				
		except psycopg2.Error as e:
			print(f"Erro ao verificar a tabela alunos:\n{e}")

		finally:
			if conexao:
				conexao.close()

	# registra aluno no banco de dados
	def registrar_aluno(self, nome, curso):
		try:
			conexao = self.obter_conexao()
			with conexao.cursor() as cursor:
				insert = "INSERT INTO alunos(matricula, nome, curso) VALUES (%s, %s, %s)"
				ano = datetime.now().strftime("%Y")
				numeros_aleatorios = []
				for _ in range(5):
					numeros_aleatorios.append(str(random.randint(0,9)))

				matricula = int(ano+"".join(numeros_aleatorios))
				cursor.execute(insert,(matricula, nome, curso))
				conexao.commit()
				print("Aluno registrado com sucesso!")
				return True

		except psycopg2.Error as e:
			print(f"Erro ao registrar o aluno: {e}")
			return False

		finally:
			if conexao:
				conexao.close()
		
	# deleta aluno do banco de dados
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

	# busca registro de aluno pela matricula
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
			print(f"Erro ao buscar o aluno: {e}")
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
			print(f"Erro ao buscar todos os alunos: {e}")
			return None

		finally:
			if conexao:
				conexao.close()

	# atualiza a nota1 do aluno
	def atualizar_nota1(self, matricula_aluno, nota1):
		try:
			conexao = self.obter_conexao()
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
	def atualizar_nota2(self, matricula_aluno, nota2):
		try:
			conexao = self.obter_conexao()
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
			if conexao:
				conexao.close()

	# buscar todos os cursos
	def buscar_todos_cursos(self):
		try:
			conexao = self.obter_conexao()
			with conexao.cursor() as cursor:
				cursor.execute("SELECT * FROM CURSOS")
				return cursor.fetchall() # retorna lista de cursos
					
		except psycopg2.Error as e:
			print(f"Erro ao buscar os cursos: {e}")
				
		finally:
			if conexao:
				conexao.close()

	# busca o id do curso pelo nome
	def buscar_id_curso(self, nome_curso):
		conexao = None
		try:
			conexao = self.obter_conexao()
			with conexao.cursor() as cursor:
				select = "SELECT id_curso FROM CURSOS WHERE nome = %s"
				cursor.execute(select,(nome_curso,))
				return cursor.fetchone() # retorna o id da tupla do curso
					
		except psycopg2.Error as e:
			print(f"Erro ao buscar os cursos: {e}")
				
		finally:
			if conexao:
				conexao.close()
		