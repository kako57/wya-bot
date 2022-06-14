from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  name = Column(String(50), nullable=False)
  discord_id = Column(String(50), nullable=False)
  sections = relationship('Sections', backref='user')
  def __repr__(self) -> str:
    return super().__repr__() + f'User(name={self.name!r}, discord_id={self.discord_id!r})'

class Section(Base):
  __tablename__ = 'sections'
  id = Column(Integer, primary_key=True)
  title = Column(String(50), nullable=False)
  start_time = Column(String(50), nullable=False)
  end_time = Column(String(50), nullable=False)
  location = Column(String(50), nullable=False)
  user_id = Column(Integer, ForeignKey('users.id'))
  def __repr__(self) -> str:
    return super().__repr__() + f'Section(title={self.title!r}, start_time={self.start_time!r}, end_time={self.end_time!r}, location={self.location!r})'
