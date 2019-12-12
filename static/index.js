document.addEventListener('DOMContentLoaded', () => {


    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => { 
       document.querySelector('#send message button').onclick = () => {
            const message = document.querySelector('#message').value;
            socket.emit('send message', {'message' : message})
        };
    });

    socket.on('broadcast message', data => {
        const li = document.createElement('li');
        li.innerHTML = `visitor message: ${data.message}`;
        document.querySelector('#board').append(li);
    });
    
});