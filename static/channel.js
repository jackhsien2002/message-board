
let counter = 1;

const amount = 20;

document.addEventListener('DOMContentLoaded', () => {
    //if page is loaded, update the first 20 messages
    load();

    var socket =  io.connect(location.protocol + '//' + document.domain + ':' + location.port);


    socket.on('connect', () => { 
       document.querySelector('#send_message_button').onclick = () => {
            const message = document.querySelector('#message').value;
            socket.emit('send message', {'message' : message});
            return false;
        };
    });

    socket.on('broadcast message', data => {
        addPost(data);
    });

})

//if page is scrolled to the bottom, add another 20 messages 
window.onscroll = () => {
    //if page is scrolled to the bottom
    if (window.scrollY + window.innerHeight >= document.body.offsetHeight) {
        //load more messages
        load()
    }
}

function load(){
    //set start and end of the message
    const start = counter;
    const end = start + amount - 1;
    counter = start + amount;
    //building request envelope
    const request = new XMLHttpRequest();
    //specify address
    request.open("POST", "/post");
    //what to do with resopnse envelope
    request.onload = () => {
        const messages = JSON.parse(request.responseText)
        messages.forEach(addPost);
    }
    //preparing paper for envelope
    const data = new FormData();
    //making data into paper
    data.append('start', start);
    data.append('end', end);
    data.append('amount', amount);
    //send the paper with envelope
    request.send(data)
}

function addPost(data) {
    var li = document.createElement("li")
        li.style.margin = "20px";
        li.innerHTML = `${data.username}: ${data.message} ${data.times}`;
    document.querySelector("#message_board").append(li)
}