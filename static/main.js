function updateUserMessage(question) {
  // Create a new div element to hold the user message
  var userDiv = document.createElement('div');
  userDiv.className = 'chat-container';
  var userMessage = document.createElement('p');
  userMessage.className = 'user-message';
  userMessage.innerText = question;
  userDiv.appendChild(userMessage);

  // Append the user message to the chat container
  var chatContainer = document.getElementById('chat-container');
  chatContainer.appendChild(userDiv);
}

function updateBotMessage(answer) {
  // Create a new div element to hold the bot message
  var botDiv = document.createElement('div');
  botDiv.className = 'chat-container';
  var botMessage = document.createElement('p');
  botMessage.className = 'bot-message';
  botMessage.innerText = answer;
  botDiv.appendChild(botMessage);

  // Append the bot message to the chat container
  var chatContainer = document.getElementById('chat-container');
  chatContainer.appendChild(botDiv);
}

$(document).ready(function() {
  $('#upload-form').on('submit', function(e) {
      e.preventDefault();
      var formData = new FormData(this);
      $.ajax({
          type: 'POST',
          url: '/upload',
          data: formData,
          contentType: false,
          processData: false,
          success: function(response) {
              if (response.success) {
                  M.toast({html: 'Files uploaded successfully'});
              } else {
                  M.toast({html: 'Error uploading files'});
              }
          },
          error: function() {
              M.toast({html: 'Error uploading files'});
          }
      });
  });

  $('#ask-btn').on('click', function() {
      var question = $('#question').val();
      if (!question) {
          M.toast({html: 'Please enter a question'});
          return;
      }
      updateUserMessage(question);
      $('#loading-spinner').css('display', 'inline-block');
      $.post('/ask', { question: question }, function(data) {
          updateBotMessage(data.answer);
          $('#loading-spinner').css('display', 'none');
      }).fail(function() {
          updateBotMessage('Error getting answer');
          $('#loading-spinner').css('display', 'none');
      });
  });
});
