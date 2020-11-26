from sqlalchemy import Integer, String, Column, ForeignKey, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

SQLALCHEMY_DATABASE_URI_2 = 'sqlite:///andela.db'

engine = create_engine(SQLALCHEMY_DATABASE_URI_2, echo=True)


class Movies(Base):
    __tablename__ = 'movies'

    tmsId = Column(String(16), primary_key=True)
    title = Column(String(50))
    releaseYear = Column(String(50))
    description = Column(String(1000))
    genres = relationship('Genre', secondary= lambda: Movie_Genres.__table__)
    theatres = relationship('Theatre', secondary= lambda: Movie_Theatres.__table__)


class Genre(Base):
    __tablename__ = 'genre'

    genreId = Column(String(64), primary_key= True)
    genreName = Column(String(50), unique= True)

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
    genreId = Column(String(64), ForeignKey('genre.genreId'), primary_key=True)


Base.metadata.create_all(engine)
