from sqlalchemy import create_engine, Column, String, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class RedactionRecord(Base):
    __tablename__ = "redaction_benchmark"

    id = Column(String, primary_key=True)
    redacted_text = Column(String)
    redacted_cases = Column(JSON)
    total_duration_seconds = Column(Float)
    created_at = Column(String)
    model = Column(String)

    def __repr__(self):
        return f"<RedactionRecord(id='{self.id}', model='{self.model}')>"


# Create database engine
engine = create_engine("sqlite:///database/redaction.db")

# Create all tables
Base.metadata.create_all(engine)

# Create session factory
Session = sessionmaker(bind=engine)
