from app import app
import flask

# ADD FRIEND
@app.route('/add_friend', methods=['POST'])
def add_friend():
    from app import db
    from models import Friend
    import json
    
    post_data = flask.request.get_json()

    first_name = post_data.get('first_name')
    last_name = post_data.get('last_name')
    
    friend = Friend()
    friend.firstname = first_name
    friend.lastname = last_name
    db.session.add(friend)
    db.session.commit()

    return flask.jsonify(ok=True)

# EDIT FRIEND
@app.route('/edit_friend', methods=['POST'])
def edit_friend():
    from app import db
    from models import Friend
    import json
    
    post_data = flask.request.get_json()

    friend_id = post_data['id']
    first_name = post_data.get('first_name')
    last_name = post_data.get('last_name')

    current_friend = Friend.query.get(friend_id)
    if first_name:
        current_friend.firstname = first_name
    if last_name:
        current_friend.lastname = last_name

    db.session.add(current_friend)
    db.session.commit()

    return flask.jsonify(ok=True)

# DELETE FRIEND
@app.route('/delete_friend/<int:friend_id>',methods=['GET'])
def delete_friend(friend_id):
    from app import db
    from models import Friend

    if friend_id:
        db.session.query(Friend).filter(Friend.id == friend_id).delete()
        db.session.commit()
        return flask.jsonify(ok=True)
    else:
        return flask.jsonify(ok=False)

# GET FRIEND DATA
@app.route("/get_friend_data/<string:friend_id>", methods=["GET"])
def get_friend_data(friend_id):
    from app import db
    from models import Friend, MovieList
    
    friend_data = db.session.query(Friend).get(friend_id)
    if friend_data:
        friend_data_dict = friend_data.to_dict()
        movie_list = db.session.query(MovieList).filter(MovieList.friendid == friend_id).first()
        movie_list_dict = movie_list.to_dict()
        return flask.jsonify(ok=True, friend_data=friend_data_dict, movies_data=movie_list_dict)
    else:
        return flask.jsonify(ok=False)


# GET ALL FRIENDS
@app.route('/get_all_friends', methods=['GET'])
def get_all_friends():
    from app import db
    from models import Friend, MovieList

    friends = [k.to_dict() for k in db.session.query(Friend).all()]

    friends_data = []

    for friend in friends:

        movie = db.session.query(MovieList).filter(MovieList.friendid == friend['id']).first()
        
        all_movies_dict = movie.to_dict() if movie else {}
        movie_d = list(all_movies_dict.keys())
        movies = []
        count = 0
        for movie_obj in movie_d:
            if 'movie' in movie_obj:
                if all_movies_dict[movie_obj]:
                    count += 1
                    movies.append({'id': movie_obj[5:], 'name': all_movies_dict[movie_obj], 'friend_id': friend['id']})

        friend['movie_count'] = count
        friend['movies'] = movies
        friend['check'] = False
        friends_data.append(friend)    

    if len(friends_data) > 0:
        return flask.jsonify(ok=True, friends=friends_data)
    else:
        return flask.jsonify(ok=False)