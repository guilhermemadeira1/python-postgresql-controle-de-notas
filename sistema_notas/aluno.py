#classe para gerenciar dados de alunos
class Aluno:
	def __init__(self, matricula: int, nome: str, curso: str, nota1: float, nota2: float):
		self.matricula = matricula
		self.nome = nome
		self.curso = curso
		self.nota1 = nota1
		self.nota2 = nota2
		self.media = self.calcular_media()
		self.situacao = self.verificar_situacao()
		
	def calcular_media(self):
		return (self.nota1+self.nota2)/2
	
	def verificar_situacao(self):
		if self.nota1 and self.nota2:
			media = self.calcular_media()
			if media >= 6:
				return "APROVADO"
			elif media >= 4:
				return "RECUPERACAO"
			else:
				return "REPROVADO"
		else:
			return ""
		

