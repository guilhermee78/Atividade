# atividade_model.py
from sql import db

class AtividadeNotFound(Exception):
    pass

class Atividade(db.Model):
    __tablename__ = 'atividades'
    id_atividade = db.Column(db.Integer, primary_key=True)
    id_disciplina = db.Column(db.Integer, nullable=False)
    professor_id = db.Column(db.Integer, nullable=False) # <--- Adicionado
    enunciado = db.Column(db.String(500), nullable=False)
    
    respostas = db.relationship('Resposta', backref='atividade', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Atividade {self.id_atividade} - {self.enunciado[:30]}>"

    def to_dict(self):
        return {
            'id_atividade': self.id_atividade,
            'id_disciplina': self.id_disciplina,
            'professor_id': self.professor_id, # <--- Adicionado
            'enunciado': self.enunciado,
            'respostas': [resposta.to_dict() for resposta in self.respostas]
        }

class Resposta(db.Model):
    __tablename__ = 'respostas'
    id_resposta = db.Column(db.Integer, primary_key=True)
    id_aluno = db.Column(db.Integer, nullable=False)
    resposta = db.Column(db.String(500), nullable=False)
    nota = db.Column(db.Integer, nullable=True)

    atividade_id = db.Column(db.Integer, db.ForeignKey('atividades.id_atividade'), nullable=False)

    def __repr__(self):
        return f"<Resposta {self.id_resposta} - Aluno {self.id_aluno}>"

    def to_dict(self):
        return {
            'id_aluno': self.id_aluno,
            'resposta': self.resposta,
            'nota': self.nota
        }

# Funções de acesso ao banco de dados (AGORA USANDO SQLAlchemy)
def listar_atividades():
    return [ativ.to_dict() for ativ in Atividade.query.all()]

def obter_atividade(id_atividade):
    atividade = Atividade.query.get(id_atividade)
    if atividade is None:
        raise AtividadeNotFound
    return atividade.to_dict()

def criar_atividade(id_disciplina, professor_id, enunciado): # <--- professor_id adicionado
    nova_atividade = Atividade(id_disciplina=id_disciplina, professor_id=professor_id, enunciado=enunciado) # <--- professor_id adicionado
    db.session.add(nova_atividade)
    db.session.commit()
    return nova_atividade.to_dict()

def adicionar_resposta(id_atividade, id_aluno, resposta_texto):
    atividade = Atividade.query.get(id_atividade)
    if atividade is None:
        raise AtividadeNotFound

    nova_resposta = Resposta(id_aluno=id_aluno, resposta=resposta_texto, atividade=atividade)
    db.session.add(nova_resposta)
    db.session.commit()
    return nova_resposta.to_dict()

def atualizar_nota_resposta(id_atividade, id_aluno, nova_nota):
    resposta = Resposta.query.filter_by(atividade_id=id_atividade, id_aluno=id_aluno).first()
    if resposta is None:
        raise ValueError(f"Resposta do aluno {id_aluno} para atividade {id_atividade} não encontrada.")
    
    resposta.nota = nova_nota
    db.session.commit()
    return resposta.to_dict()

def deletar_atividade(id_atividade):
    atividade = Atividade.query.get(id_atividade)
    if atividade is None:
        raise AtividadeNotFound
    db.session.delete(atividade)
    db.session.commit()
    return True

def obter_atividade_objeto(id_atividade):
    atividade = Atividade.query.get(id_atividade)
    if atividade is None:
        raise AtividadeNotFound
    return atividade