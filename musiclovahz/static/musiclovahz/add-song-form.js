
document.addEventListener('DOMContentLoaded', main);

function main() {
    const addSongButton = document.getElementById('add-song-btn');
    addSongButton.addEventListener('click', addNewSongForm);
}

function addNewSongForm() {
    const songInputContainer = document.getElementById('song-input-container');
    const newSongInput = document.createElement('div');
    
    newSongInput.classList.add('form-group', 'w-25', 'song-input');
    newSongInput.innerHTML = `<input class="form-control mb-1" type="text" name="title" placeholder="Song title">
                    <input class="form-control" type="text" name="artist" placeholder="Artist">`; 

    songInputContainer.appendChild(newSongInput);
}