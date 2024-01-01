const menu = document.getElementById('menu');
const menuToggle = document.getElementById('menu-toggle');
let inactivityTimer;

function selectTab(url) {
    // Hide all iframes and remove 'selected' class from all tabs
    document.querySelectorAll('.app-iframe').forEach(iframe => {
        iframe.style.display = 'none';
    });
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('selected');
    });

    // Show the selected iframe and add 'selected' class to the clicked tab
    const selectedIframe = document.querySelector(`iframe[src="${url}"]`);
    if (selectedIframe) {
        selectedIframe.style.display = 'block';
        const selectedTab = document.querySelector(`.tab[onclick="selectTab('${url}')"]`);
        if (selectedTab) {
            selectedTab.classList.add('selected');
        }
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
