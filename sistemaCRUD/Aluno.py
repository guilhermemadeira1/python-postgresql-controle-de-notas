#classe para gerenciar dados de alunos
class Aluno:
	def __init__(self, matricula, nome, curso, nota1, nota2):
		self.matricula = matricula
		self.nome = nome
		self.curso = curso
		self.nota1 = nota1
		self.nota2 = nota2
		
	def calcular_media(self):
		return (self.nota1+self.nota2)/2
	
	def verificar_situacao(self):
		media = self.calcular_media()

		if media >=6:
			return "APROVADO"
		elif media >=4:
			return "RECUPERACAO"
		else:
			return "REPROVADO"

