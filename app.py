from flask import Flask,request,render_template,redirect,url_for
import sqlite3

app = Flask(__name__)

def init_database():
    conn = sqlite3.connect("kardex.db")

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS personas(
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            fecha_nac DATE NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

init_database()

# Listado de registros
@app.route('/')
def index():
    conn = sqlite3.connect("kardex.db")
    # Permite manejar registros en forma de diccionario
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personas")
    personas = cursor.fetchall()

    return render_template('index.html',personas=personas)

# Nuevo registro nuevo
@app.route("/create")
def create():
    return render_template('create.html')

# Guardar registro nuevo
@app.route("/save",methods=['POST'])
def save():
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    fecha_nac = request.form['fecha_nac']

    conn = sqlite3.connect("kardex.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO personas (nombre,telefono,fecha_nac)
        VALUES (?,?,?)
        """,
        (nombre,telefono,fecha_nac))
    conn.commit()
    conn.close()
    return redirect("/")

# Editar registro
@app.route("/edit/<int:id>")
def persona_edit(id):
    conn = sqlite3.connect("kardex.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personas WHERE id = ?", (id,))
    persona = cursor.fetchone()
    conn.close()
    return render_template("edit.html",persona = persona)

# Guardar actualización de registro
@app.route("/update",methods=['POST'])
def personas_update():
    id = request.form['id']
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    fecha_nac = request.form['fecha_nac']

    conn = sqlite3.connect("kardex.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE personas SET nombre=?,telefono=?,fecha_nac=? WHERE id=?
        """,(nombre,telefono,fecha_nac,id))
    conn.commit()
    conn.close()
    return redirect("/")

# Eliminar registro
@app.route("/delete/<int:id>")
def personas_delete(id):
    conn = sqlite3.connect("kardex.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM personas WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True,port=5001)
