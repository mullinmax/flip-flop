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
    menuToggle.classList.toggle('hidden');
}

function resetInactivityTimer() {
    clearTimeout(inactivityTimer);
    inactivityTimer = setTimeout(() => menuToggle.classList.add('hidden'), 3000);
}
resetInactivityTimer();
// Event listeners
['touchstart', 'mousemove', 'scroll', 'click', 'mousedown'].forEach(eventType => {
    document.addEventListener(eventType, resetInactivityTimer);
});


function adjustTextSize() {
    const tabs = document.querySelectorAll('.tab-text-container span');

    tabs.forEach(tab => {
        let fontSize = 20; // Start with a max font size
        tab.style.fontSize = fontSize + 'px';

        while (tab.scrollWidth > tab.offsetWidth) {
            fontSize--;
            tab.style.fontSize = fontSize + 'px';
        }
    });
}

window.onload = adjustTextSize;
window.onresize = adjustTextSize; // Adjust text size on window resize
