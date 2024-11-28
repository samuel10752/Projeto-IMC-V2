from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Configuração do banco de dados
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123123",
    "database": "imc"
}

def get_db_connection():
    """Conecta ao banco de dados."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        flash(f"Erro ao conectar ao banco: {e}", "danger")
        return None

@app.route('/')
def index():
    """Página inicial que lista os pacientes."""
    conn = get_db_connection()
    pacientes = []
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM pacientes ORDER BY id ASC")
            pacientes = cursor.fetchall()
        except Error as e:
            flash(f"Erro ao buscar pacientes: {e}", "danger")
        finally:
            conn.close()
    return render_template('Lista/index.html', pacientes=pacientes)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """Adiciona um novo paciente."""
    if request.method == 'POST':
        nome = request.form['nome']
        try:
            peso = float(request.form['peso'])
            altura = float(request.form['altura'])

            if peso <= 0 or altura <= 0:
                flash("Peso e altura devem ser valores positivos.", "danger")
                return redirect(url_for('add'))

            # Cálculo do IMC
            imc = round(peso / (altura ** 2), 2)
            classificacao = (
                "Abaixo do peso" if imc < 18.5 else
                "Peso normal" if imc < 24.9 else
                "Sobrepeso" if imc < 29.9 else
                "Obesidade"
            )

            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO pacientes (nome, peso, altura, imc, classificacao)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (nome, peso, altura, imc, classificacao))
                    conn.commit()
                    flash("Paciente adicionado com sucesso!", "success")
                except Error as e:
                    flash(f"Erro ao adicionar paciente: {e}", "danger")
                finally:
                    conn.close()

        except ValueError:
            flash("Peso e altura devem ser valores numéricos.", "danger")
            return redirect(url_for('add'))

        # Redireciona para a página inicial após o sucesso
        return redirect(url_for('index'))
    
    # Renderiza a página para adicionar paciente
    return render_template('Adicionar/add.html')

@app.route('/delete/<int:id>')
def delete(id):
    """Remove um paciente."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pacientes WHERE id = %s", (id,))
            conn.commit()
            flash("Paciente excluído com sucesso!", "success")
        except Error as e:
            flash(f"Erro ao excluir paciente: {e}", "danger")
        finally:
            conn.close()
    # Redireciona para a página inicial após a exclusão
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
