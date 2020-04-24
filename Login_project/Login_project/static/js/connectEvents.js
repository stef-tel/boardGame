'use strict';

var socketStatus;



document.addEventListener("DOMContentLoaded", function() {
    //socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    socketStatus = io.connect('http://127.0.0.1:5000/connectStatus');
    socketStatus.on('connect', function() {
        socketStatus.emit('connected', {});
    });
});


window.addEventListener('beforeunload', (event) => {
            // Cancel the event as stated by the standard.
            //event.preventDefault();
            

            socketStatus.emit('disconnected', {}, function() {
                socketStatus.disconnect();

            });

            // Chrome requires returnValue to be set.
            //event.returnValue = '';
});

  