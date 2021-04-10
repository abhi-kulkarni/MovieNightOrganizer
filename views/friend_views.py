from app import app
import flask

# ADD FRIEND
@app.route('/add_friend', methods=['POST'])
def add_friend():
    from app import db
    from models import Friend
    import json
    
    post_data = flask.request.get_json('post_data')['post_data']

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
    
    post_data = flask.request.get_json('post_data')['post_data']

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

@app.route('/delete_friend/<int:friend_id>',methods=['DELETE'])
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
    from models import Friend

    friends = [k.to_dict() for k in db.session.query(Friend).all()]
    if len(friends) > 0:
        return flask.jsonify(ok=True, friends=friends)
    else:
        return flask.jsonify(ok=False)