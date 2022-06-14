from sqlalchemy import create_engine
from models import Base
from dotenv import load_dotenv
import os

load_dotenv()
db_path = f'sqlite:///{os.getenv('DB_PATH')}'

def update_schema():
  engine = create_engine(db_path, echo=True)
  Base.metadata.create_all(engine)

if __name__ == "__main__":
  update_schema()
