
async function showChatHistory(chatPartnerID) {
    const chatHistoryContainer = document.querySelector('#chat-history-view');
    chatHistoryContainer.innerHTML = "";
    
    // fetch call to get all the messages that were sent and received for the profile chatPartner
    let response = await fetch(`/messages/${chatPartnerID}`);
    const data = await response.json();

    const chatCard = createChatCardView(data);
    chatHistoryContainer.appendChild(chatCard);
}


function createChatCardView(data) {

    const chatCard = document.createElement('div');
    chatCard.classList.add('card', 'custom-chat-card');

    // data.messages.forEach(message => console.log(message.content));

    chatCard.innerHTML = `
    <div class="card-body">
        ${data.messages.map(msg => `
            <strong>${msg.sender}</strong> said, 
            <class='card-text'>"${msg.content}" 
            <span class="message-date">${msg.datetime}</span>`)
            .join('<br>')}
    </div>`;

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
