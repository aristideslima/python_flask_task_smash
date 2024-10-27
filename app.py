# Aplicação Demonstração de Flask com Uso do SQLAlchemy usando SQLLITE
# Esse código sofrerá uma mudança para uso do MariaDB Mysql
# Portanto vamos salvar esse código aqui para uso posterior

# Imports
import logging, os, pytz, datetime
from flask import Flask, render_template, redirect, request, current_app, has_app_context
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Configuração do Logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# My App –– IMPORTANTE: instance_relative_config=True
app = Flask(__name__, instance_relative_config=True)
Scss(app)

# Criando o diretório 'instance' se ele não existir
instance_path = os.path.join(app.root_path, 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

# Criando a estrutura de TimeZone de Recife
rec_timezone = pytz.timezone('America/Recife')

# Flask-SQLAlchemy
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

def verifica_contexto():
    if has_app_context():
        print(f"Contexto do aplicativo ativo: {current_app.name}")
        # ... seu código que requer o contexto do aplicativo ...
    else:
        print("Contexto do aplicativo não ativo.")


with app.app_context():
    verifica_contexto()  # Contexto ativo dentro deste bloco

verifica_contexto()  # Contexto não ativo fora do bloco

class MyTask(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(db.String(100),nullable=False)
    complete: Mapped[int] = mapped_column(default=0)
    created: Mapped[datetime.datetime] = mapped_column(db.DateTime, default=datetime.datetime.now(tz=rec_timezone))

    def __repr__(self) -> str:
        return  f"task {self.id}"

def create_database():
    with app.app_context():
        db_path = os.path.join(app.instance_path, 'database.db')

        print(f"Diretório raiz do projeto: {app.root_path}")
        print(f"Diretório da instância: {app.instance_path}")
        print(f"Caminho completo do banco de dados: {db_path}")

        try:
            if not os.path.exists(db_path):
                db.create_all()
                print("Banco de dados criado com sucesso!")
            else:
                print("Banco de dados já existe.")
        except Exception as e:
            print(f"Erro ao criar o banco de dados: {e}")
            exit(1)  # Encerra o programa com código de erro

create_database() # Chamada Crucial para criar o banco de dados

# Routes do webpages
# Home Page
# Rota Inicial - Função de Consulta as Tasks e de Inclusão de Tasks
@app.route("/", methods=["POST","GET"])
def index():
    # Add A Task
    if request.method == "POST":
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as error:
            logging.error(f"Erro ao adicionar tarefa: {error}")
            return "Ocorreu um erro ao adicionar a tarefa.", 500 # Retorna um código de erro 500
    # See All Current Tasks
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template('index.html', tasks=tasks)

# Rota para exclusão das Tasks
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR:{e}"

# Rota para edição das Tasks
@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id:int):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR:{e}"
    else:
        return render_template('edit.html', task=task)

if __name__ == "__main__":

    if not os.path.exists(os.path.join(app.instance_path, 'database.db')):
        print("Erro crítico: O banco de dados não foi criado. Encerrando o aplicativo.")
        exit(1) # Impede a execução do app se o banco não existir.

    print(f"Executando o aplicativo a partir do diretório: {os.getcwd()}")

#    app.run(debug=True)
    app.run(debug=False,host='0.0.0.0', port=5100, threaded=True)
