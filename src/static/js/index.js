const tabContainer = document.getElementById('tab-container');
const menuToggle = document.getElementById('menu-toggle');
const menuCloseButton = document.getElementById('menu-close');
let inactivityTimer;

function selectTab(url) {
    // Hide all iframes
    document.querySelectorAll('.app-iframe').forEach(iframe => {
        iframe.style.display = 'none';
    });

    // Show the selected iframe
    const selectedIframe = document.querySelector(`iframe[src="${url}"]`);
    if (selectedIframe) {
        selectedIframe.style.display = 'block';
    }

    // Close the menu
    tabContainer.classList.add('close');
}

function toggleMenu() {
    tabContainer.classList.toggle('close');
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
