# Aplicação Flask com SQLAlchemy para uso com um banco de dados já existente
# Essa versão da APP não cria Banco de de Dados

import logging
import os
import pytz
import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, request, current_app, has_app_context
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column

# Carregar variáveis do arquivo .env
load_dotenv()

# Configuração do Logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuração do Flask
app = Flask(__name__, instance_relative_config=True)
Scss(app)

# Configuração do fuso horário para Recife
rec_timezone = pytz.timezone('America/Recife')

# Configuração do URI do banco de dados
DATABASE_URI = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Modelo da tabela MyTask para gerenciamento de tarefas
class MyTask(db.Model):
    __tablename__ = 'my_task'
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(db.String(100), nullable=False)
    complete: Mapped[int] = mapped_column(default=0)
    created: Mapped[datetime.datetime] = mapped_column(db.DateTime, default=lambda: datetime.datetime.now(tz=rec_timezone))

    def __repr__(self) -> str:
        return f"task {self.id}"

# Rotas do aplicativo

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as error:
            logging.error(f"Erro ao adicionar tarefa: {error}")
            return "Ocorreu um erro ao adicionar a tarefa.", 500
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template('index.html', tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id: int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR:{e}"

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id: int):
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
    print(f"Executando o aplicativo a partir do diretório: {os.getcwd()}")
    app.run(debug=False, host='0.0.0.0', port=5100, threaded=True)
