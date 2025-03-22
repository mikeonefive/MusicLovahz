
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
        console.log(data);
        
        // check if we're currently on the matches page
        let reloadUrl;

        // reset currentPage to 1 if we're on the matches page
        if (isMatchesPage) {
            currentPage = 1;
            reloadUrl = '/show_matches/';  // use matches API
        } else {
            currentPage++;
            reloadUrl = '/find_matching_profiles/'; // use profile search
        }

        // load the next profile after a successful like/unlike action
        const profileContainer = document.querySelector('#profile-container');
        profileContainer.innerHTML = '';  // clear the existing profile

        // Fetch the next profile based on the updated currentPage
        await loadProfiles(reloadUrl, currentPage);
    }
}