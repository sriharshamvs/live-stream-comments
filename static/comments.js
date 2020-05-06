
var d = document, s = d.createElement('link');
s.href = 'http://'+commentHost+'/static/materialize/css/materialize.css';
s.rel = "stylesheet";
(d.head || d.body).appendChild(s);

var d = document, s = d.createElement('script');
s.src = 'http://'+commentHost+'/static/materialize/js/materialize.js';
(d.head || d.body).appendChild(s);

inital_portion = '<div class="container"><div class="row"><div class="col s12 m12"><div id="chat-log" style=""></div></div></div><div class="row"><div class="col s12 m12"><div class="card"><div class="card-content" style="padding-bottom: 10px"><div class="row"><div class="col s12 m12"><input id="chat-message-username" type="text" placeholder="Name"></div></div><div class="row"><div class="col s12 m12"><textarea id="chat-message-input" type="text" class="materialize-textarea" rows="200" placeholder="Test Message"></textarea></div></div></div><div class="card-action" style="padding-top:0"><a id="chat-message-submit" type="button" value="Send">Add Comment</a></div></div></div></div></div>'

document.querySelector('#comment_thread').innerHTML = inital_portion;
const chatSocket = new WebSocket(
    'ws://'
    + commentHost
    + '/ws/comments/'
    + roomName
    + '/'
);

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    if (data.command == 'add') {
        svg = "<div style='width:50px;margin:20%;'><svg version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 20 20\"  class=\"avatar color-{{ color_ix }}\" >\n" +
            "  <circle cx=\"50%\" cy=\"50%\" fill=\"red\" r='12' ></circle>\n" +
            "  <text text-anchor='middle' x=\"50%\" y=\"70%\" style=\"color:white\" font-size=\"15px\">" + data.username[0] + "</text>\n" +
            "</svg></div>"
        btn = "<a class='deletemsg ' onclick='deleteMsg(\"" + data.id + "\");'>Delete</a>"
        card = '<div class="row" id="comment_' + data.id + '"><div class="col s12 m12"><div class="card horizontal"><div class="card-image">' + svg + '</div><div class="card-stacked"><div class="card-content" style="padding-top: 10px; padding-bottom: 10px"><b style="font-size: larger">' + data.username + '</b><p>' + data.message + '</p></div><div class="card-action" style="margin-top: 0">' + btn + '</div></div></div></div></div>'

        //document.querySelector('#chat-log').innerHTML += ("<div style=\"border: 1px solid black;padding:5px;margin:5px\" id='comment_" + data.id + "'>" +  svg + "<div style='display: inline-block;margin-left: 5px'>" + data.username + '<br>' + data.message + '<br>' + btn + '</div>');
        document.querySelector('#chat-log').innerHTML += card
    } else if (data.command == 'delete') {
        el = document.querySelector('#comment_' + data.id);
        el.remove();
    } else if (data.command == 'delete_error') {
        alert('You cannot remove this !')
    }
};

function deleteMsg(id) {
    el = document.querySelector('#comment_' + id).innerHTML;
    chatSocket.send(JSON.stringify({
        'command': 'delete',
        'id': id,
    }));
}

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
/* document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
}; */

document.querySelector('#chat-message-submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    const userName = document.querySelector('#chat-message-username').value;
    if (userName) {
        chatSocket.send(JSON.stringify({
            'command': 'add',
            'username': userName,
            'message': message
        }));
        messageInputDom.value = '';
    } else {
        alert("Name cannot be empty !!");
    }
}