from flask import Flask, jsonify, request
import jwt   # Importa a biblioteca JWT para criar tokens de autenticação
import datetime  # Para manipulação de data e hora

# Inicializa a aplicação Flask
app = Flask(__name__)

# chave para gerar tokens JWT
# Essa chave é usada para codificar e decodificar os tokens JWT
app.config['SECRET_KEY'] = 'sua_chave_secreta'

# Em um banco real, se usaria um banco de dados como SQLite, PostgreSQL, etc.
usuarios = {}


# Cada lembrete vai ter um ID, uma mensagem e a frequência com que o lembrete ocorre
lembretes = [
    {
        'id': 1,
        'mensagem': 'Beba água agora!',
        'frequencia_minutos': 60
    },
    {
        'id': 2,
        'mensagem': 'Hidrate-se, beba um copo de água!',
        'frequencia_minutos': 120
    }
]

# Caminho para registrar um usuário
@app.route('/registrar', methods=['POST'])
def registrar():
    # Busca os dados da requisição no formato JSON
    dados = request.get_json()
    print(dados)  # Para debugar e ver os dados recebidos
    usuario = dados.get('usuario')
    senha = dados.get('senha')
    
    # Verifica se o usuário já existe no sistema
    if usuario in usuarios:
        return jsonify({'erro': 'Usuário já existe'}), 400  # Retorna erro se o usuário já estiver registrado
    
    # Cadastra o novo usuário com a senha fornecida
    usuarios[usuario] = senha
    return jsonify({'mensagem': 'Usuário registrado com sucesso'}), 201  # Retorna mensagem de sucesso

# Caminho para login
@app.route('/login', methods=['POST'])
def login():
    # Busca os dados da requisição no formato JSON
    dados = request.get_json()
    usuario = dados.get('usuario')
    senha = dados.get('senha')
    
    # Verifica se as credenciais fornecidas estão corretas
    if usuarios.get(usuario) == senha:
        # Se o usuário e a senha estiverem corretos,  vai gera um token JWT
        token = jwt.encode(
            {'usuario': usuario, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},  # Token expira em 1 hora
            app.config['SECRET_KEY'],  # Usa a chave secreta para codificar o token
            algorithm='HS256'  # Algoritmo para codificação do JWT
        )
        return jsonify({'token': token}), 200  # Retorna o token JWT
    return jsonify({'erro': 'Usuário ou senha inválidos'}), 401  # Retorna erro se as credenciais informadas estiverem incorretas

# Caminho para consultar todos os lembretes
@app.route('/lembretes', methods=['GET'])
def obter_lembretes():
    return jsonify(lembretes)  # Retorna todos os lembretes no formato JSON

# Caminho para consultar algum lembrete específico pelo ID
@app.route('/lembretes/<int:id>', methods=['GET'])
def obter_lembrete_por_id(id):
    for lembrete in lembretes:
        if lembrete.get('id') == id:  # Verifica se o ID do lembrete corresponde
            return jsonify(lembrete)  # Retorna o lembrete encontrado
    return jsonify({'erro': 'Lembrete não encontrado'}), 404  # Retorna erro caso o lembrete não seja encontrado

# Caminho para editar/alterar um lembrete existente
@app.route('/lembretes/<int:id>', methods=['PUT'])
def editar_lembrete_por_id(id):
    # Busca os dados da requisição no formato JSON
    lembrete_alterado = request.get_json()
    for indice, lembrete in enumerate(lembretes):
        if lembrete.get('id') == id:  # Verifica se o ID do lembrete corresponde
            lembretes[indice].update(lembrete_alterado)  # Atualiza o lembrete com os novos dados fornecidos
            return jsonify(lembretes[indice])  # Retorna o lembrete com a anova atualizaçao
    return jsonify({'erro': 'Lembrete não encontrado'}), 404  # Retorna erro caso o lembrete não seja encontrado

# caminho para adicionar um novo lembrete
@app.route('/lembretes', methods=['POST'])
def incluir_novo_lembrete():
    # Busca os dados da requisição no formato JSON
    novo_lembrete = request.get_json()
    lembretes.append(novo_lembrete)  # Adiciona o novo lembrete à lista
    return jsonify(lembretes)  # Retorna a lista de lembretes com o novo lembrete incluído

# Caminho para excluir um lembrete pelo ID
@app.route('/lembretes/<int:id>', methods=['DELETE'])
def excluir_lembrete(id):
    for indice, lembrete in enumerate(lembretes):
        if lembrete.get('id') == id:  # Verifica se o ID do lembrete correspondente existe
            del lembretes[indice]  # Exclui o lembrete da lista
            return jsonify(lembretes)  # Retorna a lista de lembretes disponiveis
    return jsonify({'erro': 'Lembrete não encontrado'}), 404  # Retorna erro se o lembrete não for encontrado

# Inicia o servidor Flask na porta 5000 com depuração ativada
if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)
