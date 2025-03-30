let currentAudioPlayer = null; // Keep track of the currently playing audio player
let currentAudioURL = ''; 
let audioCache = new Map();


function createAudioPlayer(title, artist) {

    const audioPlayerContainer = document.createElement('span');

    const audioPlayer = document.createElement('audio');
    audioPlayer.id = `audioPlayer-${title}`;                // make sure each audio player has a unique ID
    audioPlayer.preload = 'auto';
    audioPlayerContainer.appendChild(audioPlayer);

    const playButton = document.createElement('button');
    playButton.classList.add('audio-button');
    playButton.style.color = "white";
    playButton.textContent = '▶';
    playButton.addEventListener('click', () => {
        fetchAndPlay(title, artist, audioPlayer);

    });
    audioPlayerContainer.appendChild(playButton);

    const stopButton = document.createElement('button');
    stopButton.classList.add('audio-button');
    stopButton.style.color = "white";
    stopButton.textContent = '⏹';
    stopButton.addEventListener('click', () => {
        audioPlayer.pause();

    });
    audioPlayerContainer.appendChild(stopButton);
    
    return audioPlayerContainer;
}


async function fetchAndPlay(title, artist, audioPlayer) {
    // stop the currently playing song if there's one
    if (currentAudioPlayer && currentAudioPlayer !== audioPlayer)
        currentAudioPlayer.pause();
    
    currentAudioPlayer = audioPlayer;

    let query = `${artist} ${title}`;
    const encodedQuery = encodeURIComponent(query); 

    // check if the song url is already in our cache
    if (audioCache.has(encodedQuery)) {
        audioPlayer.src = audioCache.get(encodedQuery);
        currentAudioURL = audioPlayer.src;

        audioPlayer.oncanplaythrough = () => playSong(audioPlayer);

        return; // exit function, song is in cache
    }

    const response = await fetch(`/get_audio_url?query=${encodedQuery}`);

    if (!response.ok) {
        console.error('Failed to fetch audio URL');
        return;
    }

    const data = await response.json();

    if (data.audio_url && currentAudioURL !== data.audio_url) {
        audioPlayer.src = data.audio_url;  // Set the audio source to the fetched URL
        currentAudioURL = data.audio_url;

        audioCache.set(encodedQuery, data.audio_url);

        // Wait for the audio to be ready to play
        audioPlayer.oncanplaythrough = () => playSong(audioPlayer);

    } else {
        console.error('Audio URL not found in the response');
    }
}


function playSong(audioPlayer) {
    audioPlayer.loop = true;
    audioPlayer.play()
                .catch(error => {
                console.error("Error playing the audio:", error);
                });
}