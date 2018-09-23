'use strict';

function Room (id) {
  this.refs = {
    messageContainer: '[data-ref="room-messages"]',
    messageForm: '[data-ref="message-form"]',
    messageInput: '[data-ref="message-input"]',
    messageSubmit: '[data-ref="message-submit"]'
  };

  var url = 'ws://' + window.location.host + '/ws/room/' + id + '/';
  this.socket = new WebSocket(url);
};

Room.prototype.onMessage = function (event) {
  var data = JSON.parse(event.data);
  var content = data['content'];

  var newMessage = document.createElement('p');
  newMessage.textContent = content;

  var messagesContainer = document.querySelector(this.refs.messageContainer);
  messagesContainer.appendChild(newMessage);

  var messages = messagesContainer.children;
  if (messages.length > 50) {
    messageContainer.removeChild(messages[0]);
  }
};

Room.prototype.onClose = function (event) {
  console.error('Chat socket closed unexpectedly');
};

Room.prototype.onSubmit = function (event) {
  if (event.target.getAttribute('data-ref') == 'message-form') {
    event.preventDefault();
    var messageInput = document.querySelector(this.refs.messageInput);
    this.socket.send(JSON.stringify({ 'content': messageInput.value }));
    messageInput.value = '';
  }
};

Room.prototype.bindEvents = function () {
  this.onMessage = this.onMessage.bind(this);
  this.socket.addEventListener('message', this.onMessage);

  this.onClose = this.onClose.bind(this);
  this.socket.addEventListener('close', this.onClose);

  this.onSubmit = this.onSubmit.bind(this);
  document.addEventListener('submit', this.onSubmit);
};
