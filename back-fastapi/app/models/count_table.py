from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class MyTable(Base):
    __tablename__ = 'my_table'

    id = Column(Integer, primary_key=True)
    count_numbe = Column(Integer)

# Configuration PostgreSQL
DATABASE_URL = "postgresql://postgres:password@localhost:5432/myapp"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_database():
    """Crée toutes les tables dans la base de données"""
    Base.metadata.create_all(bind=engine)
    print("Base de données et tables créées avec succès!")

def clear_table():
    """Vide la table my_table"""
    session = SessionLocal()
    try:
        session.query(MyTable).delete()
        session.commit()
        print("Table vidée avec succès!")
    except Exception as e:
        session.rollback()
        print(f"Erreur lors du vidage de la table: {e}")
    finally:
        session.close()

def initialize_count():
    """Crée une ligne avec count_numbe = 0"""
    session = SessionLocal()
    try:
        # Créer une nouvelle entrée avec count à 0
        new_entry = MyTable(count_numbe=0)
        session.add(new_entry)
        session.commit()
        print(f"Ligne avec count = 0 créée avec succès! ID: {new_entry.id}")
        return new_entry.id
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la création de l'entrée: {e}")
    finally:
        session.close()

def setup_database():
    """Fonction principale pour configurer la base de données complète"""
    print("=== Configuration de la base de données PostgreSQL ===")
    
    # 1. Créer la base et les tables
    create_database()
    
    # 2. Vider la table (au cas où elle contiendrait déjà des données)
    clear_table()
    
    # 3. Créer une ligne avec count = 0
    entry_id = initialize_count()
    
    print(f"=== Configuration terminée! ID de l'entrée créée: {entry_id} ===")

if __name__ == "__main__":
    setup_database()
