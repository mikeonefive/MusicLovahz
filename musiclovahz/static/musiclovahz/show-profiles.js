document.addEventListener('DOMContentLoaded', main);


async function main() {
  await loadProfiles(`/find_matching_profiles/`);

  // add event listener for "Show Matches" button
  document.getElementById('show-matches-btn').addEventListener('click', async (event) => {
    event.preventDefault();           // prevent default behavior for links (it would return the raw JSON in the browser cause it's a link)
    await loadProfiles(`/show_matches/`);
  });
}


async function loadProfiles(url) {
    try {
        let response = await fetch(url);
        let jsonData = await response.json();
        console.log(jsonData);
        
        // show the profile in html
        createHTMLViewForProfiles(jsonData);

        // add like and unlike button listeners
        addLikeButtonListeners();
        
      } catch (error) {
        console.log('Error: ', error);
      }
}


function createHTMLViewForProfiles(jsonData) {

  const profileContainer = document.querySelector('#profile-container');

  // IMPORTANT! clear previous profiles before adding new ones
  profileContainer.innerHTML = ''; 

  // make sure jsonData has profiles
  if (!jsonData.profiles || jsonData.profiles.length === 0) {
      profileContainer.innerHTML = "<p>No matches found.</p>";
      return;
  }

  // iterate over the profiles array and create HTML for each profile
  jsonData.profiles.forEach(profile => {
    createHTMLForSingleProfile(profile)
  });
}


function createHTMLForSingleProfile(profile) {

  const defaultProfilePicUrl = `{% static 'path/to/default/profile-pic.jpg' %}`;
  const profileContainer = document.querySelector('#profile-container');

  // create card for 'song likes'
  const songCard = createSongCard(profile);

  // create card for user profile with profile picture
  const pictureCard = createPictureCard(profile);

  // append likeButtonContainer to the profile card 
  const likeButtonContainer = createLikeButtons(profile);

  // create card for 'songs in common'
  const songsInCommonCard = createSongsInCommonCard(profile);
  
  // Append cards to the containers
  pictureCard.appendChild(likeButtonContainer);

  profileContainer.appendChild(songCard);
  profileContainer.appendChild(pictureCard);
  profileContainer.appendChild(songsInCommonCard);
}


function createLikeButtons(profile) {
  const likeButtonContainer = document.createElement('div');
  likeButtonContainer.classList.add('like-container', 'd-flex', 'justify-content-center', 'mt-0');

  const likeButton = document.createElement('button');
  likeButton.classList.add('btn', 'like-button', 'mr-5');
  likeButton.setAttribute('data-profile-id', profile.id); 

  const likeIcon = document.createElement('img');
  likeIcon.src = "/static/musiclovahz/like.png"; 
  likeIcon.classList.add('like-icon');
  likeIcon.alt = "like icon";

  likeButton.appendChild(likeIcon);

  // UNLIKE BUTTON
  const unlikeButton = document.createElement('button');
  unlikeButton.classList.add('btn', 'unlike-button');
  unlikeButton.setAttribute('data-profile-id', profile.id);

  const unlikeIcon = document.createElement('img');
  unlikeIcon.src = "/static/musiclovahz/unlike.png";
  unlikeIcon.classList.add('like-icon');
  unlikeIcon.alt = "unlike icon";

  unlikeButton.appendChild(unlikeIcon);

  // append buttons to the container
  likeButtonContainer.appendChild(likeButton);
  likeButtonContainer.appendChild(unlikeButton);
  return likeButtonContainer;
}


function createSongCard(profile) {
  const songCard = document.createElement('div');
  songCard.classList.add('col-md-4', 'col-sm-6', 'mb-4', 'mt-3');
  songCard.innerHTML = `
      <div class="card bg-dark border-0 p-3 text-center">
          <p class="text-light mb-1">${profile.username} likes</p>
          ${profile.songs.map(song => `
              <p class="text-muted small mb-0">"${song.title}" by ${song.artist}</p>
          `).join('')}
      </div>
  `;
  return songCard;
}


function createSongsInCommonCard(profile) {
  const songCard = document.createElement('div');
  songCard.classList.add('col-md-4', 'col-sm-6', 'mb-4', 'mt-4');
  songCard.innerHTML = `
      <div class="card bg-secondary bg-gradient border-0 p-3 text-center">
          <p class="text-light mb-1">You and ${profile.username} like</p>
          ${profile.songs_in_common.map(song => `
              <p class="small mb-0">"${song.title}" by ${song.artist}</p>
          `).join('')}
      </div>
  `;
  return songCard;
}


function createPictureCard(profile) {
  const pictureCard = document.createElement('div');
  pictureCard.classList.add('col-md-4', 'col-sm-6', 'mb-4', 'mt-3');
  pictureCard.innerHTML = `
      <div class="card border-0 p-3 text-center">
          ${profile.profile_picture ? 
              `<p><img class="profile-picture" src="${profile.profile_picture}" alt="${profile.username}'s profile picture"></p>` : 
              `<p><img class="profile-picture" src="${defaultProfilePicUrl} alt="Default profile picture"></p>`
          }
  `;
  return pictureCard;
}