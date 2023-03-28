from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

class  product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    availability = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"Название: {self.name}"

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/catalog')
def catalog():
    products = product.query.all()
    return render_template('catalog.html', data = products)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method=="POST":
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']

        Product = product(name=name, description=description, price=price)

        try:
            db.session.add(Product)
            db.session.commit()
            return redirect('/catalog')
        except:
            return "Еклмн, ошибка"

    else:
        return render_template('add.html')


if __name__=='__main__':
    app.run(debug=True)