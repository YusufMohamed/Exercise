from sqlalchemy import Integer, String, Column, ForeignKey, create_engine, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

movie_genres_table = Table('movie_genres', Base.metadata,
                           Column('movieId', String(16), ForeignKey('movies.tmsId'), primary_key=True),
                           Column('genreId', Integer, ForeignKey('genre.genreId'), primary_key=True)
                           )

movie_theatres_table = Table('movie_theatres', Base.metadata,
                             Column('movieId', String(16), ForeignKey('movies.tmsId'), primary_key=True),
                             Column('theatreId', Integer, ForeignKey('theatre.theatreId'), primary_key=True)
                             )

movie_channels_table = Table('movie_channels', Base.metadata,
                             Column('movieId', String(16), ForeignKey('movies.tmsId'), primary_key=True),
                             Column('channelId', Integer, ForeignKey('channel.channelId'), primary_key=True)
                             )


class Movies(Base):
    __tablename__ = 'movies'

    tmsId = Column(String(16), primary_key=True)
    title = Column(String(50))
    releaseYear = Column(String(50))
    description = Column(String(1000))
    genres = relationship('Genre', secondary=movie_genres_table, backref='Movies')
    theatres = relationship('Theatre', secondary=movie_theatres_table, backref='Movies')
    channels = relationship('Channel', secondary=movie_channels_table, backref='Movies')


class Genre(Base):
    __tablename__ = 'genre'

    genreId = Column(Integer, primary_key=True, autoincrement=True)
    genreName = Column(String(50), unique=True)
    movies = relationship('Movies', secondary=movie_genres_table, backref='Genre')

class Channel(Base):
    __tablename__ = 'channel'

    channelId = Column(Integer, primary_key=True, autoincrement=True)
    channelName = Column(String(50))
    movies = relationship('Movies', secondary=movie_channels_table, backref='Channel')

class Theatre(Base):
    __tablename__ = 'theatre'

    theatreId = Column(Integer, primary_key= True)
    theatreName = Column(String(50))
    movies = relationship('Movies', secondary=movie_theatres_table, backref='Theatre')
