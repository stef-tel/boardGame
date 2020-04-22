'use strict';

//var socket = io.connect('http://' + document.domain + ':' + location.port);
var socket = io.connect('http://127.0.0.1:5000');

// verify our websocket connection is established
socket.on('connect', function() {
    console.log('Websocket connected!');
});

//added for room logic ==> base of games !

// message handler for the 'join_room' channel
socket.on('join_room', function(msg) {
    console.log(msg);
});

// createGame onclick - emit a message on the 'create' channel to 
// create a new game with default parameters
function createGame() {
    console.log('Creating game...');
    socket.emit('create', {size: 'normal', teams: 2, dictionary: 'Simple'});
}