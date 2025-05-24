from flask import Blueprint, jsonify, request
import atividade_model
from clients import PessoaServiceClient # Importe a classe diretamente

atividade_bp = Blueprint('atividade_bp', __name__)

# Função auxiliar para enriquecer dados
def enrich_atividade_data(atividade_dict):
    """
    Enriquece um dicionário de atividade com dados do professor e respostas com dados do aluno.
    """
    if 'professor_id' in atividade_dict:
        professor_data = PessoaServiceClient.get_professor_data(atividade_dict['professor_id'])
        if professor_data:
            # Adiciona os dados do professor diretamente na atividade
            atividade_dict['professor'] = {
                'id': professor_data.get('id'),
                'nome': professor_data.get('nome'),
                'disciplina': professor_data.get('disciplina')
            }
        else:
            atividade_dict['professor'] = None # Indica que os dados do professor não foram encontrados

    if 'respostas' in atividade_dict and atividade_dict['respostas'] is not None:
        for resposta in atividade_dict['respostas']:
            if 'id_aluno' in resposta:
                aluno_data = PessoaServiceClient.get_aluno_data(resposta['id_aluno'])
                if aluno_data:
                    # Adiciona os dados do aluno diretamente na resposta
                    resposta['aluno'] = {
                        'id': aluno_data.get('id'),
                        'nome': aluno_data.get('nome')
                        # Adicione outros campos do aluno se houver no JSON da API externa
                    }
                else:
                    resposta['aluno'] = None # Indica que os dados do aluno não foram encontrados
    return atividade_dict


@atividade_bp.route('/', methods=['GET'])
def listar_atividades():
    atividades = atividade_model.listar_atividades()
    # Enriquece cada atividade na lista
    enriched_atividades = [enrich_atividade_data(ativ) for ativ in atividades]
    return jsonify(enriched_atividades)

@atividade_bp.route('/<int:id_atividade>', methods=['GET'])
def obter_atividade(id_atividade):
    try:
        atividade = atividade_model.obter_atividade(id_atividade)
        # Enriquece a atividade antes de retornar
        enriched_atividade = enrich_atividade_data(atividade)
        return jsonify(enriched_atividade)
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404

# --- NOVOS ENDPOINTS (sem alterações significativas aqui, pois a lógica de enriquecimento está na função auxiliar) ---

@atividade_bp.route('/', methods=['POST'])
def criar_atividade():
    data = request.json
    id_disciplina = data.get('id_disciplina')
    professor_id = data.get('professor_id')
    enunciado = data.get('enunciado')

    if not all([id_disciplina, professor_id, enunciado]):
        return jsonify({'erro': 'id_disciplina, professor_id e enunciado são obrigatórios'}), 400

    # Opcional: Você pode querer validar se o professor_id existe na API externa aqui antes de criar.
    # professor_exists = PessoaServiceClient.get_professor_data(professor_id)
    # if not professor_exists:
    #     return jsonify({'erro': f'Professor com ID {professor_id} não encontrado no serviço externo.'}), 400

    nova_atividade = atividade_model.criar_atividade(id_disciplina, professor_id, enunciado)
    # Enriquece a nova atividade antes de retornar
    enriched_nova_atividade = enrich_atividade_data(nova_atividade)
    return jsonify({'mensagem': 'Atividade criada com sucesso', 'atividade': enriched_nova_atividade}), 201

@atividade_bp.route('/<int:id_atividade>/respostas', methods=['POST'])
def adicionar_resposta(id_atividade):
    data = request.json
    id_aluno = data.get('id_aluno')
    resposta_texto = data.get('resposta')

    if not all([id_aluno, resposta_texto]):
        return jsonify({'erro': 'id_aluno e resposta são obrigatórios'}), 400
    
    # Opcional: Você pode querer validar se o id_aluno existe na API externa aqui.
    # aluno_exists = PessoaServiceClient.get_aluno_data(id_aluno)
    # if not aluno_exists:
    #     return jsonify({'erro': f'Aluno com ID {id_aluno} não encontrado no serviço externo.'}), 400

    try:
        nova_resposta = atividade_model.adicionar_resposta(id_atividade, id_aluno, resposta_texto)
        # Não precisa enriquecer a resposta aqui, pois ela será enriquecida quando a atividade for listada/obtida
        return jsonify({'mensagem': 'Resposta adicionada com sucesso', 'resposta': nova_resposta}), 201
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404

@atividade_bp.route('/<int:id_atividade>/respostas/<int:id_aluno>/nota', methods=['PUT'])
def atualizar_nota_resposta(id_atividade, id_aluno):
    data = request.json
    nova_nota = data.get('nota')

    if nova_nota is None:
        return jsonify({'erro': 'O campo "nota" é obrigatório'}), 400
    
    try:
        resposta_atualizada = atividade_model.atualizar_nota_resposta(id_atividade, id_aluno, nova_nota)
        # Não precisa enriquecer a resposta aqui, pois ela será enriquecida quando a atividade for listada/obtida
        return jsonify({'mensagem': 'Nota atualizada com sucesso', 'resposta': resposta_atualizada})
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404
    except ValueError as e:
        return jsonify({'erro': str(e)}), 404

@atividade_bp.route('/<int:id_atividade>', methods=['DELETE'])
def deletar_atividade(id_atividade):
    try:
        atividade_model.deletar_atividade(id_atividade)
        return jsonify({'mensagem': 'Atividade deletada com sucesso'}), 204
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404

# --- ENDPOINT AJUSTADO (SEM VERIFICAR LER LECIONA, APENAS OBTENDO DADOS DA ATIVIDADE) ---
@atividade_bp.route('/<int:id_atividade>/professor/<int:id_professor_url>', methods=['GET'])
def obter_atividade_para_professor(id_atividade, id_professor_url):
    try:
        atividade_obj = atividade_model.obter_atividade_objeto(id_atividade)

        # Agora, a lógica é: se o professor_id_url for o professor_id da atividade,
        # você quer enriquecer e retornar a atividade.
        # Não há mais a verificação de "leciona" aqui.
        if atividade_obj.professor_id != id_professor_url:
            return jsonify({'erro': 'Professor não associado a esta atividade'}), 403 # Forbidden
        
        # Se for o professor certo, enriqueça e retorne.
        enriched_atividade = enrich_atividade_data(atividade_obj.to_dict())
        return jsonify(enriched_atividade)

    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404