let counter = 1;

const amount = 20;

document.addEventListener('DOMContentLoaded', load);

window.onscroll = () => {
    if(window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        load();
    }
};

function load() {
    const start = counter;
    const end = counter + amount - 1;
    counter = counter + amount;
    for (var i = start; i <= end; i++) {

        add_post(i.toString());
    }
}

function add_post(content) {
    var ele = document.createElement('div');
    ele.className = "";
    ele.innerHTML = content;
    ele.style.margin = "50px";

    document.querySelector("#post").append(ele);
}