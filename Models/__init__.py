from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship
Base = declarative_base()

PWD='joest3r.95'
USR='ymkhalifa'
SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@localhost:3306/andela'.format(USR, PWD)

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo = True)



class Movies(Base):
    __tablename__ = 'movies'

    tmsId = Column(Integer, primary_key=True)
    title = Column(String(50))
    releaseYear = Column(String(50))
    description = Column(String(1000))
    genres = relationship('Genre', secondary= 'Movie_Genres')
    theatres = relationship('Theatre', secondary= 'Movie_Theatres')


class Genre(Base):
    __tablename__ = 'genre'

    genreId = Column(Integer, primary_key= True, autoincrement= True)
    genreName = Column(String(50))

class Channel(Base):
    __tablename__ = 'channel'

    channelId = Column(Integer, primary_key=True)
    channelName = Column(String(50))

class Theatre(Base):
    __tablename__ = 'theatre'

    theatreId = Column(Integer, primary_key= True)
    theatreName = Column(String(50))

class Movie_Theatres(Base):
    __tablename__ = 'movie_theatres'

    movieId = Column(Integer, ForeignKey('movies.tmsId'), primary_key=True)
    theatreId = Column(Integer, ForeignKey('theatre.theatreId'), primary_key=True)

class Movie_Genres(Base):
    __tablename__ = 'movie_Genres'

    movieId = Column(Integer, ForeignKey('movies.tmsId'), primary_key=True)
    genreId = Column(Integer, ForeignKey('genre.genreId'), primary_key=True)


Base.metadata.create_all(engine)
