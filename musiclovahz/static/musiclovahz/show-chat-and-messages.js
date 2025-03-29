
async function showChatHistory(chatPartnerID) {
    const chatHistoryContainer = document.querySelector('#chat-history-view');

    // check if the chat history for this profile is already loaded
    if (chatHistoryContainer.dataset.currentChatPartnerID === String(chatPartnerID)) {
        return; // skip fetching if we are already displaying the correct chat history
    }

    // clear the chat history and update the dataset to the new chat partner
    chatHistoryContainer.innerHTML = "";
    chatHistoryContainer.dataset.currentChatPartnerID = chatPartnerID;
    
    // fetch call to get all the messages that were sent and received for the profile chatPartner
    try {
        let response = await fetch(`/messages/${chatPartnerID}`);
        const data = await response.json();

        // Append the chat messages
        const chatCard = createChatCardView(data);
        chatHistoryContainer.appendChild(chatCard);
    } catch (error) {
        console.error("Error fetching chat history:", error);
    }
}


function createChatCardView(data) {
    const chatCard = document.createElement('div');
    chatCard.classList.add('card', 'custom-chat-card');

    // data.messages.forEach(message => console.log(message.content));
    
    let messagesHTML = data.messages.map(msg => {
        let messageRead = "";  
        if (msg.sender === currentUser) {           // show read status only for messages sent by current user (currentUser gets passed in by Django in show_proiles.html)
            messageRead = msg.read ? "<span class='message-read'>read ✓</span>" : "";
        }

        return `
        <strong>${msg.sender}</strong> said, 
        <span class="card-text">"${msg.content}"</span> 
        <span class="message-date">${msg.datetime}</span>
        <br>
        ${messageRead}
        `;
    }).join('<br>');                                // combine all messages into one big string

    chatCard.innerHTML = `<div class="card-body">${messagesHTML}</div>`;
    return chatCard;
}


function createChatCardView(data) {
    const chatCard = document.createElement('div');
    chatCard.classList.add('card', 'custom-chat-card');

    let messagesHTML = data.messages.map(msg => {
        let messageRead = "";  
        if (msg.sender === currentUser) {
            messageRead = msg.read ? "<span class='message-read'>read ✓</span>" : "";
        }

        return `
        <strong>${msg.sender}</strong> said, 
        <span class="card-text">"${msg.content}"</span> 
        <span class="message-date">${msg.datetime}</span>
        <br>
        ${messageRead}
        `;
    }).join('<br>');  // Combine all messages into one big string

    chatCard.innerHTML = `<div class="card-body">${messagesHTML}</div>`;

    return chatCard;
}


function showComposeMessage(chatPartnerID) {
    const composeMessageContainer = document.querySelector('#send-message-view');
    composeMessageContainer.innerHTML = "";

    // create form dynamically
    const composeForm = document.createElement("form");
    composeForm.classList.add("compose-form");

    // store chatPartner as data attribute in the form
    composeForm.dataset.chatPartnerID = chatPartnerID;

    composeForm.innerHTML = `
        <textarea class="form-control mb-3" id="compose-body" placeholder="Type ya message here"></textarea>
        <input type="submit" value="Send" class="btn btn-secondary mb-3" id="send-message-button"/>
    `;

    composeMessageContainer.appendChild(composeForm);

    // attach event listener after creating the form
    sendMessage(composeForm);
}


function sendMessage(composeForm) {    
    if (!composeForm) return;

    composeForm.removeEventListener('submit', handleSubmit);
    composeForm.addEventListener('submit', handleSubmit);
}


async function handleSubmit(event) {
    event.preventDefault();         

    let content = document.querySelector('#compose-body').value;
    let chatPartnerID = event.target.dataset.chatPartnerID;             // get ID from form (every form saves the id so we don't have to pass it on in the functions)

    let csrfToken = getCSRFToken();

    // fetch call to backend sendMessage 
    try {                              
        let response = await fetch(`/messages/send/${chatPartnerID}`, {
          method: 'POST',
          headers: {                                
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken  // include CSRF token
            },
          body: JSON.stringify({
            content: content 
          })
        });
    
        // convert the response to JSON
        let result = await response.json(); 
        if (response.ok) {
            appendNewMessageToChat(result);
        }
    } catch (error) {
        console.log('Error: ', error);
    }
}


function appendNewMessageToChat(msg) {
    let messageElement = document.createElement('div');
    messageElement.innerHTML = `<strong>${msg.sender}</strong> said, 
            <class='card-text'>"${msg.content}" 
            <span class="message-date">${msg.datetime}</span>`;
    
    let chatContainer = document.querySelector('.card-body');
    chatContainer.appendChild(messageElement);

    // scroll to bottom of chat
    chatContainer.scrollTop = chatContainer.scrollHeight;

    document.querySelector('#compose-body').value = "";
}
