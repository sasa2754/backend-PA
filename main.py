from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

databaseProduct = []
databaseUser = []
databaseCarrinho = []
databaseVendas = []

@app.route('/cart', methods=['POST'])
def addCart():
    newProduct = request.get_json()
    newProduct['id'] = len(databaseCarrinho) + 1
    databaseCarrinho.append(newProduct)
    
    return jsonify('Produto adicionado no carrinho!'), 201

@app.route('/cart/<int:id>', methods=['DELETE'])
def deleteCart(id):
    global databaseCarrinho
    databaseCarrinho = [product for product in databaseCarrinho if product['id'] != id]
    
    return jsonify('Produto deletado do carrinho', 204)
    
# Pegar todos os usuários
@app.route('/cart', methods=['GET'])
def getAllCarts():
    return jsonify(databaseCarrinho), 200

# Adicionar um novo usuário
@app.route('/user', methods=['POST'])
def addUser():
    newUser = request.get_json()
    newUser['id'] = len(databaseUser) + 1
    databaseUser.append(newUser)
    
    return jsonify('Usuário cadastrado com sucesso!'), 201

# Login
@app.route('/login', methods=['POST'])
def login():
    login_data = request.get_json()

    email = login_data.get('email')
    password = login_data.get('password')

    if not email or not password:
        return jsonify({"message": "Email e senha são obrigatórios!"}), 400

    for user in databaseUser:
        if user['email'] == email:
            print(user)
            if user['password'] == password:
                return jsonify({"message": "Login bem-sucedido!", "user": user}), 200
            else:
                return jsonify({"message": "Senha incorreta!"}), 401

    return jsonify({"message": "Usuário não encontrado!"}), 404

# Pegar todos os usuários
@app.route('/user', methods=['GET'])
def getAllUsers():
    return jsonify(databaseUser), 200

# Update user
@app.route('/user/<int:id>', methods=['PUT'])
def updateUser(id):
    updatedUser = request.get_json()
    print("Dados recebidos:", updatedUser)

    for user in databaseUser:
        if user['id'] == id:
            print('entrou no if')
            if updatedUser.get('name') != '' and updatedUser.get('name') != None :
                user['name'] = updatedUser.get('name', user['name'])
                if updatedUser.get('email') != '' and updatedUser.get('email') != None :
                    user['email'] = updatedUser.get('email', user['email'])
                    if updatedUser.get('password') != '' and updatedUser.get('password') != None and updatedUser.get('newPassword') != '' and updatedUser.get('newPassword') != None :
                        if user['password'] == updatedUser.get('password'):
                            user['password'] = updatedUser.get('newPassword', user['password'])
                            return jsonify(user), 200
                        return jsonify({"message": "Senha incorreta"}), 400

    return jsonify({"message": "Usuário não encontrado"}), 404

# Delete User
@app.route('/user/<int:id>', methods=['DELETE'])
def deleteUser(id):
    global databaseUser
    databaseUser = [user for user in databaseUser if user['id'] != id]
    
    return jsonify('Usuário deletado', 204)

# Pegar todos os produtos
@app.route('/product', methods=['GET'])
def getAllProducts():
    return jsonify(databaseProduct), 200


# Pegar um produto por nome
@app.route('/products/<name>', methods=['GET'])
def getProductByName(name):
    products = [product for product in databaseUser if name.lower() in product["name"].lower()]
    
    if products:
        return jsonify(products), 200
    else:
        return jsonify({"message": "Produto não encontrado"}), 404
    

# Adicionar um novo produto
@app.route('/product', methods=['POST'])
def addProduct():
    newProduct = request.get_json()
    newProduct['id'] = len(databaseProduct) + 1
    databaseProduct.append(newProduct)
    
    return jsonify('Produto adicionado com sucesso!'), 201


# Atualizar um produto
@app.route('/product/<int:id>', methods=['PUT'])
def updateProduct(id):
    updatedProduct = request.get_json()
    
    for product in databaseProduct:
        if product['id'] == id:
            product['name'] = updatedProduct.get('name', product['name'])
            product['price'] = updatedProduct.get('price', product['price'])
            product['amount'] = updatedProduct.get('amount', product['amount'])
            return jsonify(product), 200
        
    return jsonify({"message": "Produto não encontrado"}), 404


# Deletar um produto
@app.route('/product/<int:id>', methods=['DELETE'])
def deleteProduct(id):
    global databaseProduct
    databaseProduct = [product for product in databaseProduct if product['id'] != id]
    
    return jsonify('Produto deletado', 204)

@app.route('/sell', methods=['POST'])
def sellProducts():
    global databaseCarrinho, databaseVendas
    
    if not databaseCarrinho:
        return jsonify({"message": "Carrinho vazio"}), 400
    
    for item in databaseCarrinho:
        venda = {
            'id': item['id'],
            'name': item['name'],
            'price': item['price'],
            'amount': item['amount'],
        }
        
        databaseVendas.append(venda)
        
        for product in databaseProduct:
            if product['id'] == item['id']:
                product['amount'] -= item['amount']
                
    databaseCarrinho.clear()
    
    return jsonify({"Message": "Produtos vendidos com sucesso!"}), 200

# Requisição pra ver a análise das vendas
@app.route('/analytics', methods=['GET'])
def getAnalytics():
    vendas_por_produto = {}
    total_geral = 0
    quantidade_total = 0

    # Contabilizar as vendas
    for venda in databaseVendas:
        product_id = venda['product_id']
        if product_id not in vendas_por_produto:
            vendas_por_produto[product_id] = {
                'name': venda['name'],
                'quantidade': 0,
                'valor_vendido': 0.0
            }
        
        vendas_por_produto[product_id]['quantidade'] += venda['amount']
        vendas_por_produto[product_id]['valor_vendido'] += venda['price'] * venda['amount']
        total_geral += venda['price'] * venda['amount']
        quantidade_total += venda['amount']

    # Gerar o relatório de vendas
    resumo_vendas = {
        "vendas_por_produto": vendas_por_produto,
        "quantidade_total_vendida": quantidade_total,
        "total_vendido": total_geral
    }

    return jsonify(resumo_vendas), 200

if __name__ == '__main__':
    app.run(debug=True)