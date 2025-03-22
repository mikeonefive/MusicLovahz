
async function createPaginationControls(jsonData, currentPage) {
    const paginationContainer = document.querySelector('#pagination-container');
    
    // Remove existing pagination if any
    paginationContainer.innerHTML = '';

    const totalNumberProfiles = jsonData.profiles.length;

    // create previous button
    if (currentPage > 1) {
        const prevButton = document.createElement('li');
        prevButton.classList.add('page-item');
        prevButton.innerHTML = `
            <a class="page-link" id="prev-page"><<</a>
        `;
        paginationContainer.appendChild(prevButton);

        // previous button click event
        prevButton.querySelector('a').addEventListener('click', async (event) => {
            event.preventDefault();
            currentPage = currentPage - 1;
            console.log(currentPage);
            let response = await loadProfiles('/show_matches/', currentPage);
            console.log(response);
        });
    }

    // create next button
    if (currentPage < totalNumberProfiles) {
        const nextButton = document.createElement('li');
        nextButton.classList.add('page-item');
        nextButton.innerHTML = `
            <a class="page-link" id="next-page">>></a>
        `;
        paginationContainer.appendChild(nextButton);

        // Next button click event
        nextButton.querySelector('a').addEventListener('click', async (event) => {
            event.preventDefault();
            currentPage = currentPage + 1;
            console.log(currentPage);
            let response = await loadProfiles('/show_matches/', currentPage);
            console.log(response);
        });
    }
}