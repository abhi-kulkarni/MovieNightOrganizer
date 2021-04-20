from app import app, db
from sqlalchemy import func
import flask
import datetime
import json

# GET ALL FRIEND MOVIES
@app.route('/get_all_movies/<int:friend_id>', methods=['GET'])
def get_all_movies(friend_id):
    from models import MovieList, Friend
    from app import db

    all_movies = db.session.query(MovieList).filter(MovieList.friendid == friend_id).first()
    
    all_movies_dict = all_movies.to_dict() if all_movies else {}
    movie_d = list(all_movies_dict.keys())
    movies = []

    for movie_obj in movie_d:
        if 'movie' in movie_obj:
            if all_movies_dict[movie_obj]:
                movies.append({'id': movie_obj[5:], 'name': all_movies_dict[movie_obj],
                'friend_id': friend_id})
    
    friend = Friend.query.get(friend_id)

    if all_movies:
        return flask.jsonify(ok=True, all_movies=movies, friend=friend.to_dict())

    else:
        return flask.jsonify(ok=False, all_movies=movies, friend=friend.to_dict())

# ADD MOVIES
@app.route('/add_movie', methods=['POST'])
def add_movies():
    from app import db
    from models import MovieList, Friend

    post_data = post_data = flask.request.get_json()
    friend_id = post_data.get('id')
    movie_name = post_data.get('movie_name')
    
    if friend_id:
        movie_list = db.session.query(MovieList).filter(MovieList.friendid == friend_id).first()
        
        if not movie_list:
            movie_list = MovieList()
            movie_list.friendid = friend_id

        # for col in list(req_movies.keys()):
        #     setattr(movie_list, col, req_movies[col])
    
        all_movies_dict = movie_list.to_dict() if movie_list else {}
        movie_d = list(all_movies_dict.keys())

        empty_slots = []
        for movie_obj in movie_d:
            if 'movie' in movie_obj:
                if not all_movies_dict[movie_obj]:
                    empty_slots.append(movie_obj)
        
        if len(empty_slots) == 0:
            return flask.jsonify(ok=False, error=True, friend_id=friend_id)
        else:
            new_slot = empty_slots[0]
            setattr(movie_list, new_slot, movie_name)

            db.session.add(movie_list)
            db.session.commit()
            return flask.jsonify(ok=True, friend_id=friend_id)
    else:
        return flask.jsonify(ok=False)

#EDIT MOVIE
@app.route('/edit_movie', methods=['POST'])
def edit_movies():
    from app import db
    from models import MovieList, Friend

    post_data = flask.request.get_json()
    friend_id = post_data.get('friend_id')
    movie_id = post_data.get('movie_id')
    movie_name = post_data.get('movie_name')

    if friend_id:
        
        movie_list = db.session.query(MovieList).filter(MovieList.friendid == friend_id).first()

        col = 'movie' + movie_id
        setattr(movie_list, col, movie_name)

        db.session.add(movie_list)
        db.session.commit()

        return flask.jsonify(ok=True, friend_id=friend_id)
    else:
        return flask.jsonify(ok=False)


# DELETE MOVIE
@app.route('/delete_movie/<string:movie_id>/<string:friend_id>', methods=['GET'])
def delete_movie(movie_id, friend_id):
    from app import db
    from models import MovieList


    if friend_id:
        
        movie_list = db.session.query(MovieList).filter(MovieList.friendid == friend_id).first()
        
        col = 'movie' + movie_id
        setattr(movie_list, col, None)

        db.session.add(movie_list)
        db.session.commit()

        return flask.jsonify(ok=True, friend_id=friend_id)
    else:
        return flask.jsonify(ok=False)


# GET RANDOM MOVIE
@app.route('/get_random_movie', methods=['POST'])
def get_random_movie():
    from app import db
    from models import MovieList, Friend
    import secrets

    friend_id_list = flask.request.get_json()
    
    all_movies = []

    for friend_id in friend_id_list:
        friend = Friend.query.get(friend_id)
        movie_list = db.session.query(MovieList).filter(MovieList.friendid == friend_id).first()
        if movie_list:
            for col in ['movie1','movie2','movie3','movie4','movie5','movie6','movie7','movie8','movie9','movie10']:
                movie_obj = getattr(movie_list, col)
                if movie_obj:
                    all_movies.append(movie_obj)

    random_movie = secrets.choice(all_movies)

    return flask.jsonify(ok=True, random_movie=random_movie)