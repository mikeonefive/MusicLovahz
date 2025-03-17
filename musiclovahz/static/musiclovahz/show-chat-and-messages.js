
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

    data.messages.forEach(message => console.log(message.content));

    chatCard.innerHTML = `
    <div class="card-body">
        ${data.messages.map(msg => `
            <strong>${msg.sender}</strong> said, 
            <class='card-text'>"${msg.content}" 
            <span class="message-date">${msg.datetime}</span>`).join('')}
    </div>
    `;

    return chatCard;
}