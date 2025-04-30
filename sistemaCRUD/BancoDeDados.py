import psycopg2

# classe para gerenciar conexao e as tabelas no banco de dados
class BancoDeDados:
	
	# retorna conexao com o banco de dados
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

	# cria as tabelas: alunos, cursos e aluno_curso
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
		          		nota1 DECIMAL(3,2) DEFAULT 0.0 NOT NULL,
		        		nota2 DECIMAL(3,2) DEFAULT 0.0 NOT NULL,
				   		FOREIGN KEY(curso) REFERENCES cursos(id_curso)
		     	 	);
				    CREATE TABLE IF NOT EXISTS aluno_curso(
				   		matricula_aluno INT,
				        id_curso INT, 
				   		PRIMARY KEY(matricula_aluno,id_curso),
				   		FOREIGN KEY(matricula_aluno) REFERENCES alunos(matricula),
				   		FOREIGN KEY(id_curso) REFERENCES cursos(id_curso)
				   	);
				   """
		   	 	)
				conexao.commit()
				# True indica operação realizada com sucesso
				return True
			
		except psycopg2.Error as e:
			print(f"Erro ao criar a tabela de alunos: {e}")
			# False indica erro na operação
			return False
		
		finally:
			conexao.close()

    # classe para gerar os cursos no banco de dados
	def inserir_cursos(self):
		try:
			conexao = self.obter_conexao()
			if conexao:
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
