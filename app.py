import peewee
from flask import Flask, jsonify, request

banco = peewee.SqliteDatabase('bancoContato.db')

class BancoContato(peewee.Model):
    titulo = peewee.CharField()
    conteudo = peewee.TextField()

    def to_dict(self):
        return {'id':self.id, 'nome': self.nome, 'canal': self.canal, 'valor': self.valor,  'obs': self.obs}

    class Meta:
        database = banco

try:
    banco.create_table(BancoContato)
except Exception as e:
    pass


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

# GET /contatos/
@app.route('/contatos')
def postagens():
    return jsonify([contato.to_dict() for contato in BancoContato.select()])


# GET /contatos/1
@app.route('/contatos/<int:idContato>')
def postagem(idContato):
    try:
        contato = BancoContato.get(id=idContato)
        return jsonify(contato.to_dict())
    except BancoContato.DoesNotExist:
        return jsonify({'status': 404, 'mensagem': 'Contato não encontrado'})


# POST /contatos/
@app.route('/contatos', methods=['POST'])
def nova_postagem():
    dados = request.json
    contato = BancoContato(nome=dados['nome'], canal=dados['canal'], valor=dados['valor'], obs=dados['obs'])
    contato.save()

    return jsonify({'status': 200, 'mensagem': 'Contato salvo com sucesso!'})


# PUT/PATCH /contatos/1
@app.route('/contatos/<int:idContato>', methods=['PUT', 'PATCH'])
def editar_postagem(idContato):
    dados = request.json

    try:
        contato = BancoContato.get(id=idContato)
    except BancoContato.DoesNotExist as e:
        return jsonify({'status': 404, 'mensagem': 'Contato não encontrado'})

    contato.nome = dados['nome']
    contato.canal = dados['canal']
    contato.valor = dados['valor']
    contato.obs = dados['obs']
    contato.save()

    return jsonify({'status': 200, 'mensagem': 'Contato salvo com sucesso'})


# DELETE /contatos/1
@app.route('/contatos/<int:idContato>', methods=['DELETE'])
def apagar_postagem(idContato):
    try:
        contato = BancoContato.get(id=idContato)
        contato.delete_instance()

        return jsonify({'status': 200, 'mensagem': 'Contato excluído com sucesso'})

    except BancoContato.DoesNotExist:
        return jsonify({'status': 404, 'mensagem': 'Contato não encontrado'})


if __name__ == '__main__':
    app.run()
