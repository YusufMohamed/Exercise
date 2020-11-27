import requests
from requests.exceptions import HTTPError
import json
from sqlalchemy.orm import sessionmaker
from Models import Movies, Genre, Theatre, Channel
import pandas as pd


def get_data_from_api(request_params=None, engine=None):
    API_FLAG = None
    API_URI = None
    if request_params.get('lineupId', None) != None and request_params.get('zip', None) == None:
        API_URI = ('http://data.tmsapi.com/v1.1/movies/airings?lineupId={}&startDateTime={}&api_key={}'
                   .format(request_params.get('lineupId'), request_params.get('startDateTime'),
                           request_params.get('api_key'))
                   )
        API_FLAG = 1
    elif request_params.get('lineupId', None) == None and request_params.get('zip', None) != None:
        API_URI = ('http://data.tmsapi.com/v1.1/movies/showings?api_key={}&startDate={}&zip={}'
                   .format(request_params.get('api_key'), request_params.get('startDate'), request_params.get('zip'))
                   )
        API_FLAG = 2
    else:
        pass
    with requests.Session() as session:
        try:
            response = get_movie_info(API_URI, session)
            parsed_response = extract_fields_from_response(response, engine, API_FLAG)
            print(f"Response: {json.dumps(parsed_response, indent=2)}")
            return parsed_response
        except Exception as err:
            print(f"Exception occured: {err}")
            return parsed_response


def extract_fields_from_response(items, engine=None, api_flag=None):
    Session = sessionmaker(bind=engine)
    session = Session()
    response = {"Status": 200}
    if api_flag == 2:
        for item in items:
            if session.query(Movies).filter(Movies.tmsId == item.get('tmsId')).first() == None:
                movie = (Movies(tmsId=item.get('tmsId'),
                                title=item.get('title'),
                                releaseYear=str(item.get('releaseYear')),
                                description=item.get('longDescription')))
                session.add(movie)

                for genre_item in item.get('genres', []):
                    genre = Genre(genreName=genre_item)
                    if session.query(Genre).filter(Genre.genreName == genre_item).first() == None:
                        session.add(genre)
                        genre.movies.append(movie)

                    else:
                        genre = session.query(Genre).filter(Genre.genreName == genre_item).first()
                        genre.movies.append(movie)

                for showtime_item in item.get('showtimes', []):
                    theatre = Theatre(theatreId=int(showtime_item.get('theatre').get('id')),
                                      theatreName=showtime_item.get('theatre').get('name'))
                    if session.query(Theatre).filter(Theatre.theatreId == theatre.theatreId).first() == None:
                        session.add(theatre)
                        theatre.movies.append(movie)

                    else:
                        theatre = session.query(Theatre).filter(Theatre.theatreId == theatre.theatreId).first()
                        theatre.movies.append(movie)
            else:
                pass
    else:
        for item in items:
            if session.query(Movies).filter(Movies.tmsId == item.get('program').get('tmsId')).first() == None:
                movie = (Movies(tmsId=item.get('program').get('tmsId'),
                                title=item.get('program').get('title'),
                                releaseYear=str(item.get('program').get('releaseYear')),
                                description=item.get('program').get('longDescription')))
                session.add(movie)

                for genre_item in item.get('program').get('genres', []):
                    genre = Genre(genreName=genre_item)
                    if session.query(Genre).filter(Genre.genreName == genre_item).first() == None:
                        session.add(genre)
                        genre.movies.append(movie)

                    else:
                        genre = session.query(Genre).filter(Genre.genreName == genre_item).first()
                        genre.movies.append(movie)

                for channel_item in item.get('channels', []):
                    channel = Channel(channelName=channel_item)
                    if session.query(Channel).filter(Channel.channelName == channel.channelName).first() == None:
                        session.add(channel)
                        channel.movies.append(movie)

                    else:
                        channel = session.query(Channel).filter(Channel.channelName == channel.channelName).first()
                        channel.movies.append(movie)
            else:
                pass
    try:
        session.commit()
    except:
        session.rollback()
        response['Status'] = 404
    finally:
        session.close()
    return response


def get_movie_info(api_endpoint, session):
    url = api_endpoint
    response = None
    try:
        response = session.get(url)
        response.raise_for_status()
        print(f"Response status ({url}): {response.status_code}")
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error ocurred: {err}")
    response_json = response.json()
    items = response_json
    return items


def top_five_genres(engine=None):
    movie_genres = pd.read_sql_table(table_name='movie_genres', con=engine)
    genres = pd.read_sql_table(table_name='genre', con=engine)
    movies = pd.read_sql_table(table_name='movies', con=engine)
    top_5_genres = (movie_genres
                    .groupby('genreId')['genreId']
                    .count().reset_index(name="count")
                    .sort_values(by=['count'], ascending=False)
                    .nlargest(5, ['count'])
                    )
    data_set = (pd
                .merge(movie_genres, top_5_genres, on='genreId')
                .merge(genres, on='genreId')
                .merge(movies[['tmsId', 'title', 'description']],
                       right_on='tmsId',
                       left_on='movieId')
                )

    result = data_set[['genreName', 'title', 'description']].to_json(orient="records")
    parsed = json.loads(result)

    groupedByGenre = {}
    for json_record in parsed:
        genre = json_record.get('genreName')
        if groupedByGenre.get(genre, None) == None:
            groupedByGenre[genre] = []
        groupedByGenre[genre].append(json_record)

    return groupedByGenre
