
var count = 0;
const amount = 10;

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
    if (window.scrollY + window.innerHeight >= document.body.clientHeight) {
        //load more messages
        load()
    }
}

function load(){
    //set start and end of the message
    const start = count;
    const end = start + amount - 1;
    count += amount
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
    /* 
    var li = document.createElement("li")
    li.style.margin = "1px";
    li.innerHTML = `${data.username}: ${data.message} ${data.times}`;
    const attr = document.createAttribute("class");
    attr.value = "list-group-item"
    li.setAttributeNode(attr)
    document.querySelector("#message-board").append(li)
    */
   var attW = document.createAttribute("class");
    attW.value = "card w-50% m-2 bg-light text-dark" ;

    var attB = document.createAttribute("class");
    attB.value = "card-body" ;

    var attT = document.createAttribute("class");
    attT.value = "card-title";

    var attTXT = document.createAttribute("class");
    attTXT.value = "card-text"; 

    var divW = document.createElement('div');
    divW.setAttributeNode(attW);
    var divB = document.createElement('div');
    divB.setAttributeNode(attB);
    var h = document.createElement('h5');
    h.innerHTML = data.username
    h.setAttributeNode(attT);
    var p = document.createElement('p');

    var attTime = document.createAttribute('class');
    attTime.value = 'card-text text-right';
    var time = document.createElement('p');
    time.setAttributeNode(attTime);
    var attSmall = document.createAttribute('class');
    //attSmall.value = "text-muted";
    var small = document.createElement('small');
    small.setAttributeNode(attSmall);
    tnode = document.createTextNode(data.times);
    small.append(tnode);
    time.append(small);

    p.innerHTML = data.message
    p.setAttributeNode(attTXT);
    divW.appendChild(divB)
    divB.append(h)
    divB.append(p);
    divB.append(time);
    var m = document.querySelector('#message-board');
    if (data.is_sent === true) {
        m.insertBefore(divW, m.firstChild);
        console.log("i am in!!");
    } else {
        m.append(divW);
    }
}