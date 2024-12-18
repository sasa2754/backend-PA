import random
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# pip install flask flask-cors reportlab

app = Flask(__name__)
CORS(app)

databaseProduct = []
databaseUser = []
databaseCarrinho = []
databaseVendas = []
databaseOrders = []

# Adiciona o Account SID
# account_sid = 'US36cd4983aef4f122bfab72ea03128639'

# # Adiciona o Auth Token
# auth_token = 'fd4c300d578181a21c723de47fdf33d1'

# @app.route('/send-code', methods=['POST'])
# def sendCode():
#     code = random.randint(1000, 9999)
    
#     # Acessa o número de telefone corretamente
#     clientphone = request.get_json()
#     phone_number = clientphone.get('userPhone')  # Corrigido aqui
    
#     if not phone_number:
#         return jsonify({'error': 'Telefone não fornecido'}), 400
    
#     # Cria um cliente com as credenciais fornecidas
#     client = Client(account_sid, auth_token)
    
#     try:
#         message = client.messages.create(
#             body=f"Olá, o seu código de verificação é: {code}",
#             from_='+5541995050132',  # Substitua pelo seu número Twilio
#             to=phone_number
#         )  # Substitua pelo número do destinatário
        
#         print(f"Mensagem enviada com sucesso! SID: {message.sid}")
#         return jsonify({'message': 'Código enviado com sucesso!'}), 201
#     except Exception as e:
#         print(f"Erro ao enviar a mensagem: {str(e)}")
#         return jsonify({'error': 'Erro ao enviar código'}), 500



# Adicionar um produto no carrinho
@app.route('/cart', methods=['POST'])
def addCart():
    newProduct = request.get_json()
    newProduct['id'] = len(databaseCarrinho) + 1
    databaseCarrinho.append(newProduct)
    
    return jsonify('Produto adicionado no carrinho!'), 201

# Deletar um produto do carrinho
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
    newUser['isAdmin'] = False
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


# Update user
@app.route('/user/recPass', methods=['PUT'])
def updateUserPass():
    print('Ta aqui!!!!!!!!!!!!!!!!!!')
    updatedUser = request.get_json()
    print("Dados recebidos:", updatedUser)

    for user in databaseUser:
        
        if updatedUser.get('id') == user['id'] :
     
            user['password'] = updatedUser.get('newPassword', user['password'])
            
            return jsonify({"message": "atualizado com sucesso"}), 200

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

# add products default para teste

productsTeste = [
    {
        "id": 1,
        "name": "Lua de Mel",
        "price": 19,
        "amount": 10,
        "image": "luaDeMel.png"
    },
    {
        "id": 2,
        "name": "Sonho de ninho",
        "price": 29,
        "amount": 5,
        "image": "sonho.png"
    },
    {
        "id": 3,
        "name": "Donuts",
        "price": 39,
        "amount": 8,
        "image": "donuts.png"
    },
    {
        "id": 4,
        "name": "Cupcake",
        "price": 9,
        "amount": 3,
        "image": "cupcake.webp"
    },

]

# Adicionando os produtos ao banco de dados (lista)
databaseProduct.extend(productsTeste) 

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
    
    totalVendas = 0
    vendas = []
    for item in databaseCarrinho:
        venda = {
            'id': item['id'],
            'name': item['name'],
            'price': item['price'],
        }
        
        vendas.append(venda)
        totalVendas += venda['price']
        
    # Gerar o PDF
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)

    c.drawString(100, 750, "Nota Fiscal")
    c.drawString(100, 730, "Produtos comprados:")
    
    y_position = 710
    valorTotal = 0
    for venda in vendas:
        valorTotal += venda['price']
        c.drawString(100, y_position, f"Produto: {venda['name']} | Preço: {venda['price']}")
        y_position -= 20
    
    c.drawString(100, y_position - 30, f"Total da Compra: {totalVendas}")

    # Salvar o PDF no buffer
    c.save()
    pdf_buffer.seek(0)
    
    for product in databaseProduct:
        if product['id'] == item['id']:
            product['amount'] -= item['amount']
            break
        
    # Limpar o carrinho e registrar a venda
    for item in databaseCarrinho:
        databaseVendas.append(item)
        
        
    databaseCarrinho.clear()

    # Enviar o PDF como resposta
    return send_file(pdf_buffer, as_attachment=True, download_name="nota_fiscal.pdf", mimetype='application/pdf')


# Requisição pra ver a análise das vendas
@app.route('/analytics', methods=['GET'])
def getAnalytics():
    quantidade_total = 0
    vendas_por_produto = {}
    total_geral = 0
    
    quantidade_total += len(databaseVendas)
    

    # Contabilizar as vendas
    for venda in databaseVendas:
        product_id = venda['id']
        if product_id not in vendas_por_produto:
            vendas_por_produto[product_id] = {
                'name': venda['name'],
                'quantidade': 0,
                'valor_vendido': 0.0
            }
        
        vendas_por_produto[product_id]['quantidade'] += venda['amount']
        vendas_por_produto[product_id]['valor_vendido'] += venda['price']
        total_geral += venda['price']
        
        

    # Gerar o relatório de vendas
    resumo_vendas = {
        "vendas_por_produto": vendas_por_produto,
        "quantidade_produtos_vendidos": quantidade_total,
        "total_vendido": total_geral
    }

    return jsonify(resumo_vendas), 200

def create_admin_user():
    for user in databaseUser:
        if user.get('isAdmin') == True:
            return
        
    admin_user = {
        'id': len(databaseUser) + 1,
        'name': 'Admin',
        'email': 'admin@email.com',
        'password': 'admin123',
        'isAdmin': True
    }
    
    databaseUser.append(admin_user)
    print('Usuário admin criado com sucesso!')

if __name__ == '__main__':
    create_admin_user()
    app.run(debug=True)