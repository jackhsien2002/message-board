document.addEventListener('DOMContentLoaded', () => {

    var socket =  io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => { 
       document.querySelector('#send_message_button').onclick = () => {
            const message = document.querySelector('#message').value;
            socket.emit('send message', {'message' : message});
            return false;
        };
    });

    socket.on('broadcast message', data => {
        const li = document.createElement('li');
        li.innerHTML = `${data.username}: ${data.message}`;
        document.querySelector('#message_board').append(li);
    });

});