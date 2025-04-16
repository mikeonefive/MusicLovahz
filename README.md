MusicLovahz - A Music-Based Matchmaking Platform

Overview

MusicLovahz is a web application that connects users based on their shared taste in music. Users can build a profile by adding their favorite songs, and the platform suggests potential matches based on these selections. Unlike traditional social networks, MusicLovahz leverages users' song preferences to facilitate meaningful connections, making it a unique and engaging experience for music aficionados.

Distinctiveness and Complexity

Uniqueness of the Project

MusicLovahz is a distinctive project because it introduces a novel way of connecting users—through shared music preferences. Unlike conventional social networks or dating apps that rely on profile descriptions, swiping mechanisms, or generic interest categories, this platform prioritizes users' actual song selections. As of now, I am not aware of a similar application that operates with this specific matchmaking logic.

Complexity of Implementation

Implementing this project was challenging, especially in structuring the database and handling model queries within Django. The complexity arises from:

Database Relationships: Managing user relationships required careful planning. Initially, I considered using a single matches field, but this proved inefficient due to unidirectional like relationships. Instead, I introduced a separate likes field to track one-way interests, while matches store mutual connections.

Django Model Queries: The logic for retrieving users with similar song interests was intricate, requiring multi-table queries and optimization for performance.

Pagination and Frontend Integration: To ensure a smooth user experience, I implemented pagination when displaying potential matches, allowing users to browse one profile at a time.

AJAX-Based Like System: The like functionality involves asynchronous JavaScript interactions with Django views to provide real-time feedback on user actions.

Messages: Matched users can send and receive messages through a simple chat interface. Messages are stored with sender, recipient, timestamp, and a read status for better interaction tracking. Messages between users are retrieved in chronological order, and any unread messages are automatically marked as read when viewed by the recipient. Message sending is handled via asynchronous POST requests, allowing real-time communication without reloading the page. While it doesn’t use sockets, the integration was still challenging to implement due to user authentication, error handling, and dynamic updates.

Custom Audio Player: Songs can be previewed directly in the browser using dynamically fetched audio streams via yt_dlp. Users hear real samples without downloading files or opening external tabs. A lightweight, JavaScript-based player lets users play or stop previews. Each button triggers asynchronous fetching of the best-quality audio URL, with caching to minimize repeated requests.

Project Files and Their Contents

Backend Files

admin.py: The Django admin interface was customized for better usability. Songs and users are displayed with key attributes like title, artist, and email for quick access. Filter_horizontal widgets were added to allow easy management of many-to-many fields like songs, likes, and matches directly from the admin panel. Message objects are shown using their serialized representation, making it easier to inspect chat content and troubleshoot during development.

models.py: Defines the User model with songs, likes, and matches relationships, as well as the Song and Message model. The default Django user model was extended to support complex social features. Custom many-to-many relationships handle likes, unlikes, and mutual matches, while profile_picture adds optional user personalization. Songs are stored with title and artist info for user preferences. Messages are timestamped, support read tracking, and are serialized for easy integration with AJAX-based chat.

forms.py: Contains UserProfileForm for updating profiles and CustomUserCreationForm for user registration.

views.py: Handles user authentication, profile editing, matchmaking logic, likes/matches updates, sending/receiving messages, and fetching the URLs for audio playback. The views in this file handle user authentication, profile management, and matchmaking. The login, registration, and profile edit functionality allow users to interact with their accounts, while AJAX-based endpoints enable liking, unliking, and messaging other users. Additionally, an audio player is integrated with yt_dlp to stream audio previews from YouTube, adding another interactive element to the experience.

urls.py: Maps frontend requests to appropriate Django views.

utils.py: This file contains helper functions that streamline the matchmaking logic (mutual likes, songs users have in common) and improve code organization. It helps optimize database queries and keeps the main views more readable.


Frontend Files

templates/musiclovahz/

audio_player_test.html: Easy implementation for an audio player in a test file.

layout.html: Basic layout for the project.

login.html: User authentication page.

register.html: Registration form with profile picture upload.

edit_profile.html: Form to update user information and add songs.

show_profiles.html: Displays potential matches along with shared songs.

like-unlike-profile.js: Handles AJAX-based like/unlike interactions for real-time UI updates.

add-song-form.js: Adds new song fields dynamically.

audio-player.js: Audio player functionality for fetching the URLs and playing the songs in the profile cards.

csrf-handler.js: Gets the CSRF token.

pagination.js: Dynamically displays/handles pagination controls for the matches page.

render-profiles.js: Gets the relevant profiles from the backend and creates the frontend HTML views for profiles.

show-chat-and-messages.js: Fetches the relevant messages from the backend and renders the frontend view for the app's chat functionality.

styles.css: Custom style sheet.

Used Libraries

yt_dlp (fetching urls and songs from youtube) 

How to Run the Application

Set Up the Virtual Environment

python -m venv venv
source venv/bin/activate 

Install Dependencies

pip install -r requirements.txt

Apply Migrations

python manage.py migrate

Run the Development Server

python manage.py runserver

Access the Application
Open a web browser and navigate to http://127.0.0.1:8000/.

Additional Notes

MusicLovahz is currently a foundational project with room for enhancement. Features like refining the like functionality, improving match accuracy, and optimizing database queries can further elevate the user experience.

The matching algorithm could also be expanded by incorporating additional factors such as song genres, curated playlists, API integrations with platforms like Spotify, and even analyzing user interaction patterns to suggest more meaningful connections.

This project is an ambitious attempt to merge music and social networking in an innovative way. With its carefully structured database and Django-based implementation, MusicLovahz lays the groundwork for a unique matchmaking experience.
