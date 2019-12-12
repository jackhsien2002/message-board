let counter = 1;

const amount = 20;

document.addEventListener('DOMContentLoaded', () => {
    let channel_id;
    if(localStorage.getItem('channel_id')) {
        channel_id = localStorage.getItem('channel_id');
        load(channel_id);
    }

    let channelArray = document.querySelectorAll('.channel');

    channelArray.forEach(function(ele) {
        ele.onclick = function () {
            const channel_id = ele.id
            localStorage.setItem('channel_id', channel_id);
            load(channel_id);
        };
    });

    window.onscroll = function() {
        if(window.innerHeight + window.scrollY >= document.body.offsetHeight) {
            load(channel_id);
        }
    };

});

function load(channel_id) {
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
    data.append('channel_id', channel_id)
    //send the paper with envelope
    request.send(data);
}

function addPost(data) {
    var li = document.createElement("li")
    li.style.margin = "20px";
    li.innerHTML = `${data.username}: ${data.message} ${data.times}`;
        document.querySelector("#message_board").append(li)
}