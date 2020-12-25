/*var d = document, s = d.createElement('link');
s.href = 'http://' + commentHost + '/static/materialize/css/materialize.css';
s.rel = "stylesheet";
(d.head || d.body).appendChild(s);

var d = document, s = d.createElement('script');
s.src = 'http://' + commentHost + '/static/materialize/js/materialize.js';
(d.head || d.body).appendChild(s);*/

// inital_portion = `<div class="container"><div class="row"><div class="col-12 col-sm-12 col-md-12 col-lg-12"><div class="card col lg-12 sm-12 md-12"><div class="card-body" style="padding-bottom: 10px"><div class="row"><div class="col lg-12 sm-12 md-12 form-group" id="comment_errors"></div></div><div class="row"><div class="col lg-12 sm-12 md-12 form-group"><input class="form-control" id="chat-message-username" type="text" placeholder="Name"></div></div><div class="row"><div class="col sm-12 lg-12 md-12 form-group"><textarea class="form-control" id="chat-message-input" type="text" class="materialize-textarea" rows="5" placeholder="Message"></textarea></div></div><div class="row text-right"><div class="col-12 col-sm-12 col-lg-12 col-md-12"><a class="btn btn-primary" id="chat-message-submit" type="button" value="Send">Add Comment</a></div></div></div></div><div class="row" style="margin-top:10px;"><div class="col sm-12 md-12 lg-12"><div id="pinned-chat-log" class="col-sm-12 col-md-12 col-lg-12"></div></div></div><div class="row" style="margin-top:10px;"><div class="col sm-12 md-12 lg-12"><div id="chat-log" class="col-sm-12 col-md-12 col-lg-12"></div></div></div><div class="row" style="margin:10px;"><div class="col-12 col-sm-12 col-md-12 col-lg-12"><button class="btn btn-primary form-control" onclick="load_comments();">Load More Comments</button></div></div></div>`;

inital_portion = `
<!-- COMMENT SECTION STARTS HERE -->
<!-- Comment Errors -->
<div id="comment_errors"></div>
<!-- User Name Input -->
<input id="chat-message-username" type="text" placeholder="Name" />
<!-- User Comment Input -->
<textarea id="chat-message-input" type="text" class="materialize-textarea" rows="5" placeholder="Message"></textarea>
<!-- Add Comment Button -->
<input id="chat-message-submit" type="button" value="Add Comment">

<!-- Pinned Comments Section -->
<div id="pinned-chat-log">
</div>
<!-- Normal Comments Section -->
<div id="chat-log">
</div>
<button onclick="load_comments();">
    Load More Comments
</button>
<!-- COMMENT SECTION ENDS HERE -->
`;

function stringToHslColor(str, s, l) {
    var hash = 0;
    for (var i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }

    var h = hash % 360;
    return 'hsl(' + h + ', ' + s + '%, ' + l + '%)';
}

document.querySelector('#comment_thread').innerHTML = inital_portion;

if (typeof contactName !== 'undefined') {
document.querySelector('#chat-message-username').value = contactName;

}

const chatSocket = new WebSocket(
    'wss://'
    + commentHost
    + ':8001/ws/comments/'
    + roomName
    + '/'
);

var startIndex = 0;
var stopIndex = 10;
load_comments = function() {
//   alert("Hello !");
   chatSocket.send(JSON.stringify({
        'command': 'get_messages',
        'start': startIndex ,
	'stop' : stopIndex,
    }));
    startIndex = stopIndex;
    stopIndex += 10;
}

	load_pinned_comments = function() {
       document.querySelector('#pinned-chat-log').innerHTML = "";
	
	   chatSocket.send(JSON.stringify({
		    'command': 'get_pinned_messages',
		}));

	}
chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    el = document.querySelector("#comment_errors");
    el.innerHTML = "";
    
    console.log(data);
    if (data.command == 'add' || data.command == 'get_message' || data.command=='get_pinned_message') {
        var color = stringToHslColor(data.user_id + "---" + data.username, 50, 60);

        // svg = "<div style='width:50px;margin:20%;'><svg version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 20 20\"  class=\"avatar color-{{ color_ix }}\" ><circle cx=\"50%\" cy=\"50%\" fill=\"" + color + "\" r='12' ></circle><text text-anchor='middle' x=\"50%\" y=\"70%\" style=\"color:white\" font-size=\"15px\">" + data.username[0] + "</text></svg></div>";

        if (userID == data.user_id) {
            // btn = "<a class='delete' onclick='deleteMsg(\"" + data.id + "\");'>Delete</a>"
            btn = `<button class="delete" onclick="deleteMsg("${data.id}")"></button>`
//            btn = '<div class="card-action" style="margin-top: 0">' + btn + '</div>';
        } else {
            btn = "";
        }

 	extra = "";    
	extra2 = "";
	if (data.command == 'get_pinned_message') {
		extra = "border-primary";
		extra2 = "pinned_";
	}

        // card = '<div class="row" id="'+extra2+'comment_' + data.id + '" style="margin-top:10px;" ><div class="card '+extra+' col-sm-12 col-md-12 col-lg-12"><div class="row no-gutters" ><div class="card-image col-2 col-sm-2 col-md-1 col-lg-1" >' + svg + '</div><div class=" col-8 col-sm-8 col-md-8 col-lg-8"><div class="card-body"><b style="font-size: larger">' + data.username + '</b><p>' + data.message + '</p>' + btn + '</div></div></div></div></div>';

        card = `
        <div class="chatbox__comment">
            <div class="chatbox__comment-icon" style="background-color: ${color};">
                <p>${data.username[0]}</p>
            </div>
            <div class="chatbox__comment-text">
                <p class="username">${data.username}</p>
                <p class="message">${data.message}</p>
                ${btn}
            </div>
        </div>
        `;
	if (data.command == 'add' && data.approved){
        document.querySelector('#chat-log').innerHTML = card + document.querySelector('#chat-log').innerHTML;
	} else if (data.command == 'get_message') {
        document.querySelector('#chat-log').innerHTML = document.querySelector('#chat-log').innerHTML + card;
	} else if (data.command == 'get_pinned_message') {
		document.querySelector('#pinned-chat-log').innerHTML = document.querySelector('#pinned-chat-log').innerHTML + card;
	}

    } else if (data.command == 'delete') {
        el = document.querySelector('#comment_' + data.id);
        el.remove();
    } else if (data.command == 'delete_error') {
        alert('You cannot remove this !')
    }else if (data.command == 'register') {
                console.log('Your user ID: '+data.id);
                userID = data.id;
		load_comments();
		load_pinned_comments();
    }else if (data.command == 'clear_pins') {
        document.querySelector('#pinned-chat-log').innerHTML = "";
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
    el = document.querySelector("#comment_errors");
    el.innerHTML = "<div class='alert alert-danger'>Connection to comments server closed unexpectedly, Please refresh.</div>";
    
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
    const msg = document.querySelector('#chat-message-input').value;
    if ((userName.length > 0) && (msg.length > 0)) {
        chatSocket.send(JSON.stringify({
            'command': 'add',
            'username': userName,
            'message': message
        }));
        messageInputDom.value = '';
    } else {
        alert("Name and Message cannot be empty !!");
    }
}
