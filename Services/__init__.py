import hashlib

import requests
from requests.exceptions import HTTPError
import json
from sqlalchemy.orm import sessionmaker
from Models import Movies, Genre


def get_data_from_api(request_params = None, engine = None):
    print(request_params)
    API_URI = ('http://data.tmsapi.com/v1.1/movies/showings?api_key={}&startDate={}&zip={}'
               .format(request_params.get('api_key'), request_params.get('startDate'), request_params.get('zip'))
               )
    with requests.Session() as session:
        try:
            response = get_book_details_seq(API_URI, session)
            parsed_response = extract_fields_from_response(response, engine)
            print(f"Response: {json.dumps(parsed_response, indent=2)}")
        except Exception as err:
            print(f"Exception occured: {err}")
            pass

def extract_fields_from_response(items, engine = None):
    Session = sessionmaker(bind=engine)
    session = Session()
    for item in items:
        if session.query(Movies).filter(Movies.tmsId == item.get('tmsId')).first() == None:
            movie = (Movies(tmsId = item.get('tmsId'),
                            title = item.get('title'),
                            releaseYear = str(item.get('releaseYear')),
                            description = item.get('longDescription')))

            for genre_item in item.get('genres', []):
                genre = Genre(genreId = genre_item, genreName=genre_item)
                if session.query(Genre).filter(Genre.genreName == genre_item).first() == None:
                    session.add(genre)
                    movie.genres.append(genre)
                else:
                    print(session.query(Genre).filter(Genre.genreName == genre_item).first())
#http://127.0.0.1:5000/movies?startDate=2020-11-26&zip=78701&api_key=7sta9hza6u3j5b4y6uxjn2a2

            session.add(movie)
        else:
            pass


    session.commit()

    # volume_info = item.get("volumeInfo", {})
    # title = volume_info.get("title", None)
    # subtitle = volume_info.get("subtitle", None)
    # description = volume_info.get("description", None)
    # published_date = volume_info.get("publishedDate", None)
    # return (
    #     title,
    #     subtitle,
    #     description,
    #     published_date,
    # )
    return item

def get_book_details_seq(isbn, session):
    url = isbn
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


def save_to_database():
    return 2