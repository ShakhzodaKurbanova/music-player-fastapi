from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Artist(Base):
    __tablename__ = 'artists'

    artist_id = Column(Integer, primary_key=True, index=True)
    artist_name = Column(String, nullable=False, unique=True)

    songs = relationship('Song', back_populates='artists', cascade='all, delete')

class Song(Base):
    __tablename__ = 'songs'

    song_id = Column(Integer, primary_key=True, index=True)
    song_name = Column(String, nullable=False)
    artist_id = Column(Integer, ForeignKey('artists.artist_id'))

    artist = relationship('Artists', back_populates='songs')