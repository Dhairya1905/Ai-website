from sqlalchemy import create_engine, Column, String, DateTime, Text, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./website_generator.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Database Models
class Project(Base):
    __tablename__ = "projects"
    
    id = Column(String, primary_key=True)
    prompt = Column(Text, nullable=False)
    template = Column(String, nullable=True)
    style = Column(String, nullable=False)
    html = Column(Text, nullable=False)
    css = Column(Text, nullable=False)
    js = Column(Text, nullable=False)
    meta_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Template(Base):
    __tablename__ = "templates"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    components = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize default templates
def init_templates():
    db = SessionLocal()
    try:
        # Check if templates already exist
        if db.query(Template).count() > 0:
            return
        
        default_templates = [
            {
                "id": "portfolio",
                "name": "Portfolio",
                "description": "Perfect for artists and photographers",
                "components": ["navbar", "hero", "gallery", "about", "contact"]
            },
            {
                "id": "business",
                "name": "Business",
                "description": "Professional business website",
                "components": ["navbar", "hero", "services", "about", "testimonials", "contact"]
            },
            {
                "id": "ecommerce",
                "name": "E-commerce",
                "description": "Online store template",
                "components": ["navbar", "hero", "products", "features", "contact"]
            },
            {
                "id": "restaurant",
                "name": "Restaurant",
                "description": "Restaurant or cafe website",
                "components": ["navbar", "hero", "menu", "about", "reservations", "contact"]
            }
        ]
        
        for template_data in default_templates:
            template = Template(**template_data)
            db.add(template)
        
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    init_templates()
    print("Database initialized with default templates")
