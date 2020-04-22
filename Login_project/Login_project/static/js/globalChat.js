'use strict';

var socket;
    $(document).ready(function(){
        //socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
        socket = io.connect('http://127.0.0.1:5000/globalChat');
        socket.on('connect', function() {
        socket.emit('joined', {});
    });

    socket.on('status', function(data) {
              //$('#chat').val($('#chat').val() + '<' + data.msg + '>\n');
              //$('#chat').scrollTop($('#chat')[0].scrollHeight);
              addChat(data.msg,data.sender,'join');
    });

    socket.on('message', function(data) {
        //$('#chat').val($('#chat').val() + data.msg + '\n');
        //$('#chat').scrollTop($('#chat')[0].scrollHeight);
        //var messagecontent = JSON.parse(data)
        addChat(data.msg,data.sender,'message');
    });

    $('#text').keypress(function(e) {
            var code = e.keyCode || e.which;
            if (code == 13) {
                var text = $('#text').val();
                $('#text').val('');
                socket.emit('text', {msg: text});
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

    function addChat (message, sender, type) {
        // crée un nouvel élément div
        var newDiv = document.createElement("div");
    
        var align;
        var color;
    
        if (type == 'message'){
            if (username == sender){
            align = "text-align: right;"
            color = "notification is-info"
            // et lui donne un peu de contenu
            newDiv.innerHTML = message;

            } else {
            align = "text-align: left;"
            color = "notification is-warning"
            newDiv.innerHTML = '<i><sup>' + sender + '</i></sup></br>' + message;
            }
        }else{
            align = "text-align: center;"
            color = "notification is-danger" 
            newDiv.innerHTML = message;
        }

        newDiv.setAttribute('class', color);
        newDiv.setAttribute('style', align);
    
        // ajoute le nouvel élément créé et son contenu dans le DOM
        var currentDiv = document.getElementById('parent');
        currentDiv.insertBefore(newDiv, null);
        currentDiv.scrollIntoView(false)

    }