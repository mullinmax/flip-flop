const tabContainer = document.getElementById('tab-container');
const menuToggle = document.getElementById('menu-toggle');
const menuCloseButton = document.getElementById('menu-close');
let inactivityTimer;
let iframes = [];

// Load apps and setup tabs
async function loadApps() {
    try {
        const response = await fetch('/docker-labels');
        const apps = await response.json();
        setupTabs(apps);
    } catch (error) {
        console.error('Error loading apps:', error);
    }
}

function setupTabs(apps) {
    apps.forEach((app, index) => {
        createIframe(app, index);
        createTab(app, index);
    });
    selectTab(0);
}

function createIframe(app, index) {
    const iframe = document.createElement('iframe');
    iframe.style.cssText = `display: ${index === 0 ? 'block' : 'none'}; width: 100%; height: 100vh; border: none;`;
    iframe.src = app.url;
    iframe.onerror = () => console.error('Error loading iframe for:', app.url);
    document.body.appendChild(iframe);
    iframes.push(iframe);
}

function createTab(app, index) {
    const tab = document.createElement('button');
    tab.className = 'tab tab-enhanced';
    tab.innerHTML = getTabContent(app);
    tab.onclick = () => {
        selectTab(index);
        toggleMenu();
    };
    document.getElementById('grid-container').appendChild(tab);
}

function selectTab(index) {
    iframes.forEach((iframe, i) => iframe.style.display = i === index ? 'block' : 'none');
    document.querySelectorAll('.tab').forEach(tab => tab.classList.toggle('active', tab.dataset.index === index.toString()));
}

function getTabContent(app) {
    const iconContent = app.icon ? (app.icon.startsWith('http') ? `<img src="${app.icon}" alt="" class="tab-icon">` : `<span class="tab-icon">${app.icon}</span>`) : `<img src="https://${getDomain(app.url)}/favicon.ico" alt="" class="tab-icon">`;
    return `${iconContent}${app.name}`;
}

function getDomain(url) {
    return new URL(url).hostname;
}

function toggleMenu() {
    tabContainer.classList.toggle('close');
    menuToggle.classList.toggle('hidden');
}

function isMenuOpen() {
    return !tabContainer.classList.contains('close');
}

function resetInactivityTimer() {
    clearTimeout(inactivityTimer);
    inactivityTimer = setTimeout(() => menuToggle.classList.add('hidden'), 3000);
}

// Event listeners
['touchstart', 'mousemove', 'scroll', 'click', 'mousedown'].forEach(eventType => {
    document.addEventListener(eventType, resetInactivityTimer);
});


menuCloseButton.addEventListener('click', toggleMenu);

// Initialize
loadApps();
resetInactivityTimer();
