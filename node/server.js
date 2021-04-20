const app = require('./app');
const port = 5001;

app.listen(port, function() {
    console.log('Express server listening on port ' + port);
});