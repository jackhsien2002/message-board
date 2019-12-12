document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#send message').onsubmit = () => {
        //build a new request
        const request = new XMLHttpRequest();
        const message = document.querySelector('#message').value;
        request.open('POST','/chat')
        
        request.onload = () => {
            const data = JSON.parse(request.responseText)
            const li = document.createElement('li');
            li.innerHTML = data.message
            document.querySelector('#board').append('li')
        }

        const data = new FormData();
        data.append('message', message)
        request.send(data)
    }
});