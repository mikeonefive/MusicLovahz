
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

    // check if the button has the class like-button or unlike-button
    if (button.classList.contains('like-button')) {

        // update this profile's like (fetch call to the backend)
        const response = await fetch(`/likes/${profileId}/`, {
            method: 'POST'    
        });

        const data = await response.json();
        console.log(data);


    } else if (button.classList.contains('unlike-button')) {
        const response = await fetch(`/likes/${profileId}/`, {
            method: 'DELETE'    
        });

        const data = await response.json();
        console.log(data);
    }
}
