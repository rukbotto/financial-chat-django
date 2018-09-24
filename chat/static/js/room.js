'use strict';

function Room (roomId, userId, username) {
  this.refs = {
    messageContainer: '[data-ref="messages"]',
    messageTime: '[data-ref="message-time"]',
    messageForm: '[data-ref="message-form"]',
    messageInput: '[data-ref="message-input"]',
    messageSubmit: '[data-ref="message-submit"]'
  };

  this.roomId = roomId;
  this.userId = userId;
  this.username = username;

  var url = 'ws://' + window.location.host + '/ws/room/' + this.roomId + '/';
  this.socket = new WebSocket(url);
};

Room.prototype.parseISODatetime = function (datetime) {
  var regexp = /([\d]{4})-([\d]{2})-([\d]{2})T([\d]{2}):([\d]{2}):([\d]{2})\.([\d]{6})\+[\d]{2}:[\d]{2}/g;
  var match = regexp.exec(datetime);
  return new Date(
    Date.UTC(
      parseInt(match[1]),
      parseInt(match[2]) - 1,
      parseInt(match[3]),
      parseInt(match[4]),
      parseInt(match[5]),
      parseInt(match[6]),
      parseInt(match[7]) / 1000
    )
  );
};

Room.prototype.createNewMessageDOM = function (data) {
  var date = this.parseISODatetime(data['datetime']);

  var timeDOM = document.createElement('time');
  timeDOM.setAttribute('datetime', date.toISOString());
  timeDOM.textContent = date.toString();

  var metadataDOM = document.createElement('p');
  metadataDOM.textContent = 'By ' + data['user_name'] + ' on ';
  metadataDOM.appendChild(timeDOM);

  var contentDOM = document.createElement('p');
  contentDOM.textContent = data['content'];

  var newMessageDOM = document.createElement('div');
  newMessageDOM.appendChild(metadataDOM);
  newMessageDOM.appendChild(contentDOM);
  return newMessageDOM;
};

Room.prototype.onMessage = function (event) {
  var data = JSON.parse(event.data);

  var messageContainerDOM = document.querySelector(this.refs.messageContainer);
  messageContainerDOM.appendChild(this.createNewMessageDOM(data));

  var messageListDOM = messageContainerDOM.children;
  if (messageListDOM.length > 50) {
    messageContainerDOM.removeChild(messageListDOM[0]);
  }
};

Room.prototype.onClose = function (event) {
  console.error('Chat socket closed unexpectedly');
};

Room.prototype.onSubmit = function (event) {
  if (event.target.getAttribute('data-ref') == 'message-form') {
    event.preventDefault();
    var messageInputDOM = document.querySelector(this.refs.messageInput);
    this.socket.send(
      JSON.stringify({
        'content': messageInputDOM.value,
        'room_id': this.roomId,
        'user_id': this.userId
      })
    );
    messageInputDOM.value = '';
  }
};

Room.prototype.onInit = function (event) {
  var messageContainerDOM = event.target;
  var messageTimeListDOM = messageContainerDOM.querySelectorAll(this.refs.messageTime);
  for (var i = 0; i < messageTimeListDOM.length; i++) {
    var datetime = messageTimeListDOM[i].getAttribute('datetime');
    var date = this.parseISODatetime(datetime);
    messageTimeListDOM[i].textContent = date.toString();
  }
};

Room.prototype.bindEvents = function () {
  this.onMessage = this.onMessage.bind(this);
  this.socket.addEventListener('message', this.onMessage);

  this.onClose = this.onClose.bind(this);
  this.socket.addEventListener('close', this.onClose);

  this.onSubmit = this.onSubmit.bind(this);
  document.addEventListener('submit', this.onSubmit);

  this.onInit = this.onInit.bind(this);
  var messageContainerDOM = document.querySelector(this.refs.messageContainer);
  messageContainerDOM.addEventListener('init', this.onInit);
  messageContainerDOM.dispatchEvent(new Event('init'));
};
