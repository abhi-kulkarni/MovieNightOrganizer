const express = require('express');
const path = require('path');
const app = express();
const bodyParser = require('body-parser');
const request = require('request');
const api = 'http://127.0.0.1:5000';

var session = require('express-session');
var flash = require('express-flash');
app.use(session({ cookie: { maxAge: 60000 }, 
    secret: 'r4VXyGva7e',
    resave: false, 
    saveUninitialized: false
}));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.static(__dirname + '/public'));
app.use(flash());
app.use(function (req, res, next) {
  res.locals.messages = require('express-messages')(req, res);
  next();
});

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.get('/', function(req, res, next) {
    request.get(api+'/get_all_friends', function (error, response, body) {
        let friends = JSON.parse(body)['friends'];
        res.render('friends', { user: {}, friends: friends });
      }); 
});

app.get('/movies/:id', function(req, res, next) {
    let id = parseInt(req.params.id);
    request.get(api + '/get_all_movies/'+ id, function (error, response, body) {
        let body_res = JSON.parse(body);
        let movie_res = body_res['all_movies'];
        let friend_res = body_res['friend'];
        res.render('movies', { 'movie_count_err_msg': '', movie: {'friend_id': friend_res.id}, movies: movie_res, friend: friend_res });
      }); 
});

app.post('/movies/add_movie/', function(req, res) {
    let movie = req.body;
    let options = { 
        method: 'POST', 
        uri: api+'/add_movie', 
        body: movie, 
        json: true 
    }; 
    request(options, function (error, response, body) {
        let friend_id = body['friend_id'];
        if(body.ok){
            req.flash("success", "Movie Added Successfully");
        }else{
            if(body.error){
                req.flash("error", "You cannot add more than 10 movies");
            }else{
                req.flash("error_msg", "Some Error Occured");
            }
        }
       
        res.redirect('/movies/'+friend_id);
    }); 
});

app.post('/movies/edit_movie/', function(req, res) {
    let movie = req.body;
    let options = { 
        method: 'POST', 
        uri: api+'/edit_movie', 
        body: movie, 
        json: true 
    }; 
    request(options, function (error, response, body) {
        let friend_id = body['friend_id'];
        if(body.ok){
            req.flash("success", "Movie Updated Successfully");
        }else{
            req.flash("error", "Some Error Occured");
        }
        res.redirect('/movies/'+friend_id)
    });    
});

app.get('/delete_movie/:movie_id/:friend_id', function(req, res, next) {
    let movie_id = req.params.movie_id;
    let friend_id = req.params.friend_id;
    request.get(api + '/delete_movie/'+ movie_id + '/' + friend_id, function (error, response, body) {
        let body_res = JSON.parse(body);
        let friend_id = body_res['friend_id'];
        if(body_res.ok){
            req.flash("success", "Movie Deleted Successfully");
        }else{
            req.flash("error", "Some Error Occured");
        }
        res.redirect('/movies/'+friend_id)
    }); 
});

app.post('/add_friend', function(req, res) {
    let user = req.body;
    let options = { 
        method: 'POST', 
        uri: api+'/add_friend', 
        body: user, 
        json: true 
    }; 
    request(options, function (error, response, body) {
        if(body.ok){
            req.flash("success", "Friend Added Successfully");
        }else{
            req.flash("error", "Some Error occured");
        }
        res.redirect('/');
    });      
       
});

app.post('/edit_friend', function(req, res) {
    let user = req.body;
    let options = { 
        method: 'POST', 
        uri: api+'/edit_friend', 
        body: user, 
        json: true 
    }; 
        
    request(options, function (error, response, body) {
        if(body.ok){
            req.flash("success", "Friend Updated Successfully");
        }else{
            req.flash("error", "Some Error occured");
        }
        res.redirect('/');
    });      
       
});

app.get('/delete_friend/:id', function(req, res, next) {
    let id = parseInt(req.params.id);
    request.get(api + '/delete_friend/'+ id, function (error, response, body) {
        let body_res = JSON.parse(body);
        if(body_res.ok){
            req.flash("success", "Friend Deleted Successfully");
        }else{
            req.flash("error", "Some Error Occured");
        }
        res.redirect('/')
    }); 
});

app.get('/get_all_friends', function(req, res) {
    request.get(api+'/get_all_friends', function (error, response, body) {
        res.send(body);
      });      
});

app.get('/organizer', function(req, res, next) {
    request.get(api+'/get_all_friends', function (error, response, body) {
        let friends = JSON.parse(body)['friends'];
        res.render('organizer', { random_movie:false, user: {}, friends: friends });
      }); 
});

app.post('/get_random_movie', function(req, res) {
    let friend_id_list = req.body.selected_users;
    if(friend_id_list === 'selected_friends'){
        req.flash("info", "Select Atleast One Friend To Watch A Movie");
        res.redirect('/organizer');
    }else{
        friend_id_list = friend_id_list.split(',');
        let options = { 
            method: 'POST', 
            uri: api+'/get_random_movie', 
            body: friend_id_list, 
            json: true 
        }; 
        request(options, function (error, response, body) {
            let random_movie = {};
            if(body.ok){
                random_movie = body['random_movie'];
            }else{
                req.flash("error", "Some Error Occured");
            }
            res.render('organizer', { random_movie: random_movie, user: {}, friends: [] });
        });    
    }
});

module.exports = app;