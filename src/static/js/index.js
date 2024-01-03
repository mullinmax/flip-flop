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
    const selectedTab = document.querySelector(`.tab[onclick="selectTab('${url}')"]`);
    if (selectedTab) {
        selectedTab.classList.add('selected');
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




const spinner = document.querySelector('.loading-spinner');
const radius = window.innerWidth * 0.15; // Radius of the central area

for (let i = 0; i < 100; i++) {
    const star = document.createElement('div');
    star.classList.add('star');
    const angle = Math.random() * Math.PI * 2; // Random angle
    const distance = Math.random() * radius; // Random distance within the radius
    const x = Math.cos(angle) * distance; // X position
    const y = Math.sin(angle) * distance; // Y position
    star.style.left = `calc(50% + ${x}px)`;
    star.style.top = `calc(50% + ${y}px)`;
    const translateX = Math.cos(angle) * (window.innerWidth / 2); // X translation
    const translateY = Math.sin(angle) * (window.innerHeight / 2); // Y translation
    star.style.setProperty('--translateX', `${translateX}px`);
    star.style.setProperty('--translateY', `${translateY}px`);
    star.style.animationDuration = `${Math.random() * 3 + 2}s`; // Random duration between 2 to 5 seconds
    spinner.appendChild(star);
}
