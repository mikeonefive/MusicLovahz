
function addLikeButtonListeners() {
   
    // Select all elements with the class 'like-button'
    const likeButtons = document.querySelectorAll('.like-button');
    const unlikeButtons = document.querySelectorAll('.unlike-button');
    
    // Add the click event listener to each like button and show the right color (if current user has liked the profile)
    likeButtons.forEach(button => {
        button.addEventListener('click', updateLikes);
    });

    unlikeButtons.forEach(button => {
        button.addEventListener('click', updateLikes);
    })
}


async function updateLikes(event) {
    // use event.target to get the actual button that was clicked
    const button = event.currentTarget;

    // Retrieve the profile ID from the button's data attribute (the button in our html gets the data for the id from the user object, see likebuttons.html for example)
    const profileId = button.getAttribute('data-profile-id');
    let response;

    let csrfToken = getCSRFToken();

    // check if the button has the class like-button or unlike-button
    if (button.classList.contains('like-button')) {

        // console.log(`Like button clicked for ${profileId}`);

        // update this profile's like (fetch call to the backend)
        response = await fetch(`/likes/${profileId}/`, {
            method: 'POST',
            headers: {                                
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken  // include CSRF token
                }    
        });
    } else if (button.classList.contains('unlike-button')) {
        response = await fetch(`/likes/${profileId}/`, {
            method: 'DELETE',
            headers: {                                
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken  
                }   
        });

        // clear chat history when unliking
        document.querySelector('#chat-history-view').innerHTML = "";
        document.querySelector('#send-message-view').innerHTML = "";
    }

    if (response && response.ok) {  
        const data = await response.json();

        // reset currentIndex to 0 if we're on the matches page
        if (isMatchesPage) {
            currentProfileIndex = 0;
        } else {
            currentProfileIndex++;
        }

        // load the next profile after a successful like/unlike action
        displayProfile(currentProfileIndex);
    }
}