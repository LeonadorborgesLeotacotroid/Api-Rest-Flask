from flask import Flask,request, jsonify
from models.article import db, Article

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///articles.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/articles', methods=['GET'])
def get_articles():
    articles = Article.query.all()
    return jsonify([{
        'id': article.id,
        'title': article.title,
        'content': article.content
    } for article in articles])
    
@app.route('/create-article', methods=['POST'])
def create_article():
    data = request.get_json()
    new_article = Article(title=data['title'], content=data['content'])
    db.session.add(new_article)
    db.session.commit()
    return jsonify({
        'id': new_article.id,
        'title': new_article.title,
        'content': new_article.content,
        'message': 'Articulo creado!'
        }), 201

@app.route('/article/<int:id>', methods= ['PUT'])
def update_article(id):
    article = Article.query.get_or_404(id)
    data = request.get_json()
    article.title = data.get('title', article.title)
    article.content = data.get('content', article.content)  
    db.session.commit()
    
    return jsonify({
        'id': article.id,
        'title': article.title,
        'content': article.content,
        'message': 'Articulo actualizado!'
    })
    
@app.route('/article/<int:id>', methods=['DELETE'])
def delete_article(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    return jsonify({'message': 'Articulo eliminado!'}),200

@app.route('/article/<int:id>', methods=['GET'])
def view_article(id):
    article = Article.query.get_or_404(id)
    return  jsonify({
        'id': article.id,
        'title': article.title,
        'content': article.content
    })

if __name__ == '__main__':
    app.run(debug=True, port=8000)
    