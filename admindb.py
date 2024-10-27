import os
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# URI do banco de dados definida no arquivo .env
DATABASE_URI = os.getenv("DATABASE_URI")

# Definir larguras fixas para cada coluna (ajuste conforme necessário)
COLUMN_WIDTHS = {
    "id": 5,
    "content": 50,
    "complete": 10,
    "created": 20
}

def connect_to_database():
    """
    Conecta ao banco de dados usando SQLAlchemy e retorna a sessão e a engine.
    """
    try:
        engine = create_engine(DATABASE_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        print(f"Conectado ao banco de dados: {DATABASE_URI}")
        return session, engine
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None, None

def list_tables(engine):
    """
    Lista todas as tabelas no banco de dados usando SQLAlchemy.
    """
    try:
        metadata = MetaData()
        metadata.reflect(bind=engine)  # Reflete as tabelas do banco de dados
        tables = metadata.tables.keys()
        print("Tabelas no banco de dados:")
        for table in tables:
            print(f"- {table}")
        return tables
    except Exception as e:
        print(f"Erro ao listar tabelas: {e}")
        return []

def display_table_content(engine, table_name):
    """
    Exibe o conteúdo de uma tabela específica usando SQLAlchemy.
    """
    try:
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=engine)
        with engine.connect() as connection:
            result = connection.execute(table.select()).fetchall()
            print(f"\nConteúdo da tabela '{table_name}':")
            
            if result:
                # Exibe cabeçalhos com larguras fixas
                col_names = table.columns.keys()
                header = " | ".join(f"{col_name:<{COLUMN_WIDTHS.get(col_name, 15)}}" for col_name in col_names)
                print(header)
                print("-" * len(header))

                # Exibe cada linha com alinhamento à esquerda e largura fixa
                for row in result:
                    row_str = " | ".join(f"{str(cell):<{COLUMN_WIDTHS.get(col_name, 15)}}" for cell, col_name in zip(row, col_names))
                    print(row_str)
            else:
                print(f"A tabela '{table_name}' está vazia.")
    except Exception as e:
        print(f"Erro ao exibir conteúdo da tabela '{table_name}': {e}")

def main():
    """
    Função principal para conectar ao banco, listar tabelas e exibir conteúdo.
    """
    session, engine = connect_to_database()
    if engine:
        try:
            tables = list_tables(engine)
            if tables:
                for table in tables:
                    display_table_content(engine, table)
            else:
                print("Nenhuma tabela encontrada no banco de dados.")
        finally:
            session.close()
            print("\nConexão com o banco de dados encerrada.")

if __name__ == "__main__":
    main()
