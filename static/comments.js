/*var d = document, s = d.createElement('link');
s.href = 'http://' + commentHost + '/static/materialize/css/materialize.css';
s.rel = "stylesheet";
(d.head || d.body).appendChild(s);

var d = document, s = d.createElement('script');
s.src = 'http://' + commentHost + '/static/materialize/js/materialize.js';
(d.head || d.body).appendChild(s);*/

inital_portion = '<div class="container"><div class="row"><div class="col-12"><div class="card lg-12 sm-12 md-12"><div class="card-body" style="padding-bottom: 10px"><div class="row"><div class="col lg-12 sm-12 md-12 form-group"><input class="form-control" id="chat-message-username" type="text" placeholder="Name"></div></div><div class="row"><div class="col sm-12 lg-12 md-12 form-group"><textarea class="form-control" id="chat-message-input" type="text" class="materialize-textarea" rows="5" placeholder="Test Message"></textarea></div></div><div class="row text-right"><div class="col-12 col-sm-12 col-lg-12 col-md-12"><a class="btn btn-primary" id="chat-message-submit" type="button" value="Send">Add Comment</a></div></div></div></div></div></div><div class="row" style="margin-top:10px;"><div class="col sm-12 md-12 lg-12"><div id="chat-log" class="col-sm-12 col-md-12 col-lg-12"></div></div></div></div>'

function stringToHslColor(str, s, l) {
    var hash = 0;
    for (var i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }

    var h = hash % 360;
    return 'hsl(' + h + ', ' + s + '%, ' + l + '%)';
}

document.querySelector('#comment_thread').innerHTML = inital_portion;
const chatSocket = new WebSocket(
    'ws://'
    + commentHost
    + ':8001/ws/comments/'
    + roomName
    + '/'
);

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    if (data.command == 'add') {
        var color = stringToHslColor(data.user_id, 50, 60);

        svg = "<div style='width:50px;margin:20%;'><svg version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 20 20\"  class=\"avatar color-{{ color_ix }}\" ><circle cx=\"50%\" cy=\"50%\" fill=\"" + color + "\" r='12' ></circle><text text-anchor='middle' x=\"50%\" y=\"70%\" style=\"color:white\" font-size=\"15px\">" + data.username[0] + "</text></svg></div>";

        if (userID == data.user_id) {
            btn = "<a class='deletemsg btn btn-danger' onclick='deleteMsg(\"" + data.id + "\");'>Delete</a>"
//            btn = '<div class="card-action" style="margin-top: 0">' + btn + '</div>';
        } else {
            btn = "";
        }
        card = '<div class="row" id="comment_' + data.id + '" style="margin-top:10px;" ><div class="card col-sm-12 col-md-12 col-lg-12"><div class="row no-gutters" ><div class="card-image col col-sm col-md-2 col-lg-2" >' + svg + '</div><div class=" col-8 col-sm-8 col-md-8 col-lg-8"><div class="card-body" ><b style="font-size: larger">' + data.username + '</b><p>' + data.message + '</p>' + btn + '</div></div></div></div></div>';
        document.querySelector('#chat-log').innerHTML = card + document.querySelector('#chat-log').innerHTML;

    } else if (data.command == 'delete') {
        el = document.querySelector('#comment_' + data.id);
        el.remove();
    } else if (data.command == 'delete_error') {
        alert('You cannot remove this !')
    }else if (data.command == 'register') {
                console.log('Your user ID: '+data.id);
                userID = data.id;
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
