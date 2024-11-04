from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import os
Base = declarative_base()

class DNARecord(Base):
    __tablename__ = 'dna_records'

    id = Column(Integer, primary_key=True)
    sequence = Column(String, unique=True, nullable=False)
    is_mutant = Column(Integer, nullable=False)

# Obtén la cadena de conexión de las variables de entorno
DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dna_records.db')  # Usa SQLite si DATABASE_URL no está definida

# Crear la base de datos
engine = create_engine('sqlite:///dna_records.db')
Base.metadata.create_all(engine)

# Crear la sesión
Session = sessionmaker(bind=engine)

