# Script para criação inicial do banco de dados e tabelas

import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
import datetime
import pytz

# Carregar variáveis do arquivo .env
load_dotenv()

# Configuração do Flask
app = Flask(__name__)

# Configuração do banco de dados
DATABASE_URI = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Configuração do fuso horário para Recife
rec_timezone = pytz.timezone('America/Recife')

# Modelo da tabela MyTask
class MyTask(db.Model):
    __tablename__ = 'my_task'
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(db.String(100), nullable=False)
    complete: Mapped[int] = mapped_column(default=0)
    created: Mapped[datetime.datetime] = mapped_column(db.DateTime, default=datetime.datetime.now(tz=rec_timezone))

    def __repr__(self) -> str:
        return f"task {self.id}"

def create_database():
    """Função para criar o banco de dados e as tabelas"""
    with app.app_context():
        try:
            db.create_all()
            print("Banco de dados e tabelas criados com sucesso!")
        except Exception as e:
            print(f"Erro ao criar o banco de dados: {e}")

if __name__ == "__main__":
    print("Iniciando a criação do banco de dados...")
    create_database()
    print("Processo concluído.")
