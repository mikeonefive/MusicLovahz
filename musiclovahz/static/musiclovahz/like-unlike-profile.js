//  Run main when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', main);

function main() {
   
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

    
    // TODO update match section dynamically here with a function (fetch call to backend matches which should return a JSON)


    // if (response.ok) {
    //     const data = await response.json();
    //     const likeContainer = button.closest(".like-container");            // look for the closest ancestor element of the button (the clicked button) that matches the CSS class .like-container.
    //     const likeCountElement = likeContainer.querySelector(".badge");     // get the badge which holds the likecount in the frontend

    //     if (likeCountElement) {
    //         likeCountElement.textContent = data.likecount;                  // Update the displayed like count in the frontend
    //     }

    //     updateLikeSymbol(button, data);

    // } else {
    //     alert('Failed to update like count.');
    // }
}
