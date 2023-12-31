const menu = document.getElementById('menu');
const menuToggle = document.getElementById('menu-toggle');
let inactivityTimer;

function selectTab(index) {
    // Hide all iframes and remove 'selected' class from all tabs
    document.querySelectorAll('.app-iframe').forEach(iframe => {
        iframe.style.display = 'none';
    });
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('selected');
    });

    // Get the URL from the tabsData array using the index
    const url = tabsData[index].url;

    // Find the iframe corresponding to the clicked tab
    let selectedIframe = document.getElementById(`iframe-${index}`);
    if (selectedIframe.getAttribute('data-loaded') === 'false') {
        // If the iframe hasn't been loaded yet, set its src and mark it as loaded
        selectedIframe.src = url;
        selectedIframe.setAttribute('data-loaded', 'true');
    }

    // Display the selected iframe
    selectedIframe.style.display = 'block';

    // Add 'selected' class to the clicked tab
    const selectedTab = document.querySelector(`.tab[onclick="selectTab(${index})"]`);
    if (selectedTab) {
        selectedTab.classList.add('selected');

        // Get the icon source from the clicked tab
        const iconSrc = selectedTab.querySelector('.tab-image-container img').src;

        // Display the app icon near the spinner
        const appIcon = document.querySelector('.loader-icon'); // Ensure you have this element in your HTML
        appIcon.src = iconSrc;
        appIcon.style.display = 'block';
    }

    // Close the menu
    menu.classList.add('close');
}

function toggleMenu() {
    menu.classList.toggle('close');
    menuToggle.classList.toggle('close');
}

function resetInactivityTimer() {
    clearTimeout(inactivityTimer);

    // Ensure FAB is visible and iframes are interactive
    menuToggle.classList.remove('close');
    document.querySelectorAll('iframe').forEach(iframe => iframe.style.pointerEvents = 'auto');

    // Set a timer to hide the FAB and disable interaction with iframes
    inactivityTimer = setTimeout(() => {
        menuToggle.classList.add('close');
        document.querySelectorAll('iframe').forEach(iframe => iframe.style.pointerEvents = 'none');
    }, 3000);
}

// Reset the inactivity timer on various user interactions
['touchstart', 'mousemove', 'scroll', 'click', 'mousedown'].forEach(eventType => {
    document.addEventListener(eventType, resetInactivityTimer);
});


document.getElementById('fullscreenButton').addEventListener('click', function() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
        this.textContent = 'Exit Full Screen';
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
            this.textContent = 'Go Full Screen';
        }
    }
});
