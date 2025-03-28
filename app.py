import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv

#Cargar las variables de entorno
load_dotenv()

#Crear instancia
app = Flask(__name__)

#Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Desactivar el seguimiento de modificaciones de objetos

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

#Modelo de la base de datos
class Planta(db.Model):
    __tablename__= 'plantas'
    id_planta = db.Column(db.Integer, primary_key=True)
    nombre_cientifico = db.Column(db.String)
    nombre_comun = db.Column(db.String)
    descripcion = db.Column(db.String)
    stock = db.Column(db.Integer)

    def to_dict(self):
        return{
            'id_planta': self.id_planta,
            'nombre_cientifico': self.nombre_cientifico,
            'nombre_comun': self.nombre_comun,
            'descripcion': self.descripcion,
            'stock': self.stock
        }

#Crear tablas si no existen
with app.app_context():
    db.create_all()

#Ruta raiz
@app.route('/', methods=['GET'])
def index():
    #Trae todas las plantas
    plantas = Planta.query.all()
    return render_template('index.html', plantas = plantas)

#CREAR
@app.route('/new', methods=['GET','POST'])
def create_planta():
    if request.method == 'POST':
        id_planta = request.form['id_planta']
        nombre_cientifico = request.form['nombre_cientifico']
        nombre_comun = request.form['nombre_comun']
        descripcion = request.form['descripcion']
        stock = request.form['stock']
        db.session.add(Planta(id_planta=id_planta, nombre_cientifico=nombre_cientifico, nombre_comun=nombre_comun, descripcion=descripcion, stock=stock))
        db.session.commit()
        return redirect(url_for('index'))
    #Aqui sigue si es GET
    return render_template('create_planta.html')

#ELIMINAR
@app.route('/delete/<int:id_planta>')
def delete_planta(id_planta):
    planta = Planta.query.get(id_planta)
    if planta:
        db.session.delete(planta)
        db.session.commit()
    return redirect(url_for('index'))

#ACTUALIZAR
@app.route('/update/<int:id_planta>', methods=['GET','POST'])
def update_planta(id_planta):
    planta = Planta.query.get(id_planta)
    if request.method == 'POST':
        #No se modifica: id_planta
        planta.nombre_cientifico = request.form['nombre_cientifico']
        planta.nombre_comun = request.form['nombre_comun']
        planta.descripcion = request.form['descripcion']
        planta.stock = request.form['stock']
        db.session.commit()
        return redirect(url_for('index'))
    #Aqui sigue si es GET
    return render_template('update_planta.html', planta=planta)


if __name__ == '__main__':
    app.run(debug=True)

#source bin/activate
#pip install -r requirements.txt
#flask run --port=5010