
async function createPaginationControls() {
    const paginationContainer = document.querySelector('#pagination-container');
    
    // Remove existing pagination if any
    paginationContainer.innerHTML = '';

    // create previous button
    if (currentProfileIndex > 0) {
        const prevButton = document.createElement('li');
        prevButton.classList.add('page-item');
        prevButton.innerHTML = `
            <a class="page-link" id="prev-page"><<</a>
        `;

        paginationContainer.appendChild(prevButton);
        
        // previous button click event
        prevButton.querySelector('a').addEventListener('click', async (event) => {
            event.preventDefault();
            currentProfileIndex--;
            displayProfile(currentProfileIndex);
            createPaginationControls();
        });
    }

    // create next button
    if (currentProfileIndex < profiles.length - 1) {
        const nextButton = document.createElement('li');
        nextButton.classList.add('page-item');
        nextButton.innerHTML = `
            <a class="page-link" id="next-page">>></a>
        `;

        paginationContainer.appendChild(nextButton);
        
        // Next button click event
        nextButton.querySelector('a').addEventListener('click', async (event) => {
            event.preventDefault();
            currentProfileIndex++;
            displayProfile(currentProfileIndex);
            createPaginationControls();
        });
        
    }
}