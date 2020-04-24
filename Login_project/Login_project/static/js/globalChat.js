'use strict';

var socket;
var idElementCounter = 1;
var newElementId;


//$(document).ready(function() {
//replacing JQuery by vanilla javascript
document.addEventListener("DOMContentLoaded", function() {
    //socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    socket = io.connect('http://127.0.0.1:5000/globalChat');
    socket.on('connect', function() {
        socket.emit('joined', {});
    });

    socket.on('status', function(data) {
        addElement(data.msg, data.sender, "text-align: center;","notification is-danger");
    });

    socket.on('message', function(data) {
        addChat(data.msg, data.sender);
    });

    $('#text').keypress(function(e) {
        var code = e.keyCode || e.which;
        if (code == 13) {
            var text = $('#text').val();
            $('#text').val('');
            socket.emit('text', {
                msg: text
            });
        }
    });
});


function leave_room() {
    socket.emit('left', {}, function() {
        socket.disconnect();

        // go back to the login page
        window.location.href = "{{ url_for('main.index') }}";
    });
}



function addElement(message, sender, style, classe, parentElement="parent") {
    // crée un nouvel élément div
    var newDiv = document.createElement("div");
    newDiv.id  = 'newDiv' + (++idElementCounter);
    newDiv.innerHTML = message;

    newDiv.setAttribute('class', classe);
    newDiv.setAttribute('style', style);

    // ajoute le nouvel élément créé et son contenu dans le DOM
    var currentDiv = document.getElementById(parentElement);
    currentDiv.insertBefore(newDiv, null);
    newDiv.scrollIntoView(false)

    return newDiv.id

}

function addChat(message, sender) {
    var New1;
    var New2;

    if (username !== sender) { 
        New1 = addElement("", sender, "", "columns is-multiline");
        New2 = addElement("", sender, "", "column is-two-thirds", New1);
        addElement('<i><sup>' + sender + '</i></sup></br>' + message, sender, "text-align: left;", "notification is-info", New2);
        addElement("", sender, "", "column", New1);
    }
    else{
        New1 = addElement("", sender, "", "columns is-multiline");
        addElement("", sender, "", "column", New1);
        New2 = addElement("", sender, "", "column is-two-thirds", New1);
        addElement(message, sender, "text-align: right;", "notification is-warning", New2);
    }

}