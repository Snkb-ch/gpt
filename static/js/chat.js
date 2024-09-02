// document.addEventListener('DOMContentLoaded', function() {
//   const chatMessages = document.getElementById('chat-messages');
//   const userInput = document.getElementById('user-input');
//   const sendButton = document.getElementById('send-button');

//   sendButton.addEventListener('click', sendMessage);
//   userInput.addEventListener('keypress', function(e) {
//     if (e.key === 'Enter' && !e.shiftKey) {
//       e.preventDefault();
//       sendMessage();
//     }
//   });

//   function scrollToBottom() {
//     window.scrollTo(0, document.body.scrollHeight);
//   }

//   async function sendMessage() {
//     const message = userInput.value.trim();
//     if (message) {
//       addMessage('user', message);
//       userInput.value = '';
//       scrollToBottom();
      
//       try {
//         console.log('Sending message:', message);
//         const response = await fetch('/chat-gpt', {
//           method: 'POST',
//           headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': getCookie('csrftoken')
//           },
//           body: JSON.stringify({message: message})
//         });

//         console.log('Response status:', response.status);
//         if (!response.ok) {
//           throw new Error(`HTTP error! status: ${response.status}`);
//         }

//         const reader = response.body.getReader();
//         const decoder = new TextDecoder();
//         let aiMessage = '';
//         let messageElement = null;

//         while (true) {
//           const { value, done } = await reader.read();
//           if (done) break;
          
//           const chunk = decoder.decode(value);
//           console.log('Received chunk:', chunk);
//           const lines = chunk.split('\n');
          
//           for (const line of lines) {
//             if (line.startsWith('data: ')) {
//               const data = line.slice(6);
//               if (data === '[DONE]') {
//                 if (messageElement) {
//                   messageElement.dataset.complete = 'true';
//                 }
//                 break;
//               } else {
//                 aiMessage += data;
//                 if (!messageElement) {
//                   messageElement = addMessage('ai', aiMessage);
//                 } else {
//                   messageElement.innerHTML = aiMessage;
//                 }
//                 scrollToBottom();
//               }
//             }
//           }
//         }
//       } catch (error) {
//         console.error('Error:', error);
//         addMessage('ai', 'Sorry, an error occurred while processing your request.');
//         scrollToBottom();
//       }
//     }
//   }

//   function addMessage(sender, message) {
//     const messageContainer = document.createElement('div');
//     messageContainer.classList.add('message-container');

//     const messageElement = document.createElement('div');
//     messageElement.classList.add('message', `${sender}-message`);
//     messageElement.innerHTML = message;
//     messageElement.dataset.complete = 'false';

//     messageContainer.appendChild(messageElement);
//     chatMessages.appendChild(messageContainer);

//     return messageElement;
//   }

//   function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//       const cookies = document.cookie.split(';');
//       for (let i = 0; i < cookies.length; i++) {
//         const cookie = cookies[i].trim();
//         if (cookie.substring(0, name.length + 1) === (name + '=')) {
//           cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//           break;
//         }
//       }
//     }
//     return cookieValue;
//   }
// });