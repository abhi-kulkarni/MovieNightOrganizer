from app import app, db
from sqlalchemy import func
import flask
import datetime
import json

# GET ALL FRIEND MOVIES

@app.route('/get_all_movies/<int:friend_id>', methods=['GET'])
def get_all_movies(friend_id):
    from models import MovieList
    from app import db

    all_movies = [k.to_dict() for k in db.session.query(MovieList).filter(MovieList.friendid == friend_id).all()]
    
    if len(all_movies) > 0:
        return flask.jsonify(ok=True, all_movies=all_movies)

    else:
        return flask.jsonify(ok=False)

# ADD MOVIES

@app.route('/add_movies', methods=['POST'])
def add_movies():
    from app import db
    from models import MovieList

    post_data = post_data = flask.request.get_json('post_data')['post_data']
    friend_id = post_data.get('id')
    
    req_movies = post_data.get('movies', {})
    
    if friend_id:
        movie_list = db.session.query(MovieList).filter(MovieList.friendid == friend_id).first()
        
        if not movie_list:
            movie_list = MovieList()
            movie_list.friendid = friend_id

        for col in list(req_movies.keys()):
            setattr(movie_list, col, req_movies[col])

        db.session.add(movie_list)
        db.session.commit()

        return flask.jsonify(ok=True)
    else:
        return flask.jsonify(ok=False)

# EDIT/DELETE MOVIES

@app.route('/modify_movies', methods=['POST'])
def modify_movies():
    from app import db
    from models import MovieList

    post_data = post_data = flask.request.get_json('post_data')['post_data']
    friend_id = post_data.get('id')

    if friend_id:
        req_movies = post_data.get('movies', {})
        
        movie_list = db.session.query(MovieList).filter(MovieList.friendid == friend_id).first()

        for col in list(req_movies.keys()):
            setattr(movie_list, col, req_movies[col])

        db.session.add(movie_list)
        db.session.commit()

        return flask.jsonify(ok=True)
    else:
        return flask.jsonify(ok=False)


# EDIT/DELETE MOVIES

@app.route('/delete_movies', methods=['DELETE'])
def delete_movies():
    from app import db
    from models import MovieList

    post_data = post_data = flask.request.get_json('post_data')['post_data']
    friend_id = post_data.get('id')

    if friend_id:
        req_movies = post_data.get('movies', [])
        
        movie_list = db.session.query(MovieList).filter(MovieList.friendid == friend_id).first()

        for col in req_movies:
            setattr(movie_list, col, None)

        db.session.add(movie_list)
        db.session.commit()

        return flask.jsonify(ok=True)
    else:
        return flask.jsonify(ok=False)


# GET RANDOM MOVIES 

@app.route('/get_random_movie', methods=['POST'])
def get_random_movie():
    from app import db
    from models import MovieList, Friend
    import secrets

    post_data = post_data = flask.request.get_json('post_data')['post_data']
    friend_id_list = post_data.get('friend_ids')
    
    all_movies = []

    for friend_id in friend_id_list:
        friend = Friend.query.get(friend_id)
        movie_list = db.session.query(MovieList).filter(MovieList.friendid == friend_id).first()
        for col in ['movie1','movie2','movie3','movie4','movie5','movie6','movie7','movie8','movie9','movie10']:
            movie_obj = getattr(movie_list, col)
            if movie_obj:
                all_movies.append(movie_obj)

    random_movie = secrets.choice(all_movies)

    return flask.jsonify(ok=True, random_movie=random_movie)