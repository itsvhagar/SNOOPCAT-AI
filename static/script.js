var ip = '';
$(document).ready(function () {
    console.log("Hello");
    $.ajax({
    url: 'https://ipapi.co/ip',
    type: 'GET',
    contentType: 'application/json',
    async: true,
    success: function (msg) {
        ip = msg;
    },
    error: function (xhr, status, error) {
    }
});
});

$(document).on('click', '#send-button', function (e) {
    console.log("OK");
    var message = $('#message-input').val();
    console.log(message);
    $('#message-input').val("");
    // Append the message to the chat window
    $('#chat-body').append('<div class="chat-message user-message"><div class="message-content">' + message + '</div></div>');

    // Scroll to the bottom of the chat body
    $('#chat-body').scrollTop($('#chat-body')[0].scrollHeight);

    fetch('http://127.0.0.1:5000/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            ip: ip,
            message: message
        })
        })
        .then(function(response) {
            if (response.ok) {
            return response.json();
            } else {
            throw new Error('Error: ' + response.status);
            }
        })
        .then(function(response) {
            console.log(response);
            if (response.status == 'ok') {
                console.log(response.data[0]);
                // Append the message to the chat window
                $('#chat-body').append('<div class="chat-message bot-message"><img src="static/snoopcatlogo.png" alt="SnoopCat Logo"><div class="message-content">' + response.data[0] + '</div></div>');

                // Scroll to the bottom of the chat body
                $('#chat-body').scrollTop($('#chat-body')[0].scrollHeight);
            } 
        })
        .catch(function(error) {
            console.log('Error:', error);
        });
});
