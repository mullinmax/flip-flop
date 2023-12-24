const tabContainer = document.getElementById('tab-container');
const menuToggle = document.getElementById('menu-toggle');
let inactivityTimer;
let iframes = [];

// Load apps and setup tabs
function loadApps() {
    fetch('/docker-labels')
        .then(response => response.json())
        .then(setupTabs)
        .catch(error => console.error('Error loading apps:', error));
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
    Object.assign(iframe.style, {
        display: index === 0 ? 'block' : 'none',
        width: '100%',
        height: '100vh',
        border: 'none'
    });
    iframe.src = app.url;
    iframe.onerror = () => {
        console.error('Error loading iframe for:', app.url);
        iframe.style.display = 'none';
    };
    document.body.appendChild(iframe);
    iframes.push(iframe);
}

function createTab(app, index) {
    const tab = document.createElement('button');
    tab.className = 'tab tab-enhanced';
    tab.innerHTML = getTabContent(app);
    tab.onclick = () => {
        selectTab(index);
        hideMenu();
    };
    tabContainer.appendChild(tab);
}

function selectTab(index) {
    iframes.forEach((iframe, i) => iframe.style.display = i === index ? 'block' : 'none');
    document.querySelectorAll('.tab').forEach((tab, i) => tab.classList.toggle('active', i === index));
}

function getTabContent(app) {
    let iconContent;
    if (app.icon && app.icon.startsWith('http')) {
        // If the icon is a URL, use it as the source for an image
        iconContent = `<img src="${app.icon}" alt="" style="width: 16px; height: 16px; vertical-align: middle; margin-right: 8px;">`;
    } else if (app.icon) {
        // If the icon is not a URL, treat it as an emoji or text
        iconContent = `<span style="font-size: 16px; vertical-align: middle; margin-right: 8px;">${app.icon}</span>`;
    } else {
        // If no icon is provided, use the default favicon from the app's domain
        iconContent = `<img src="https://${getDomain(app.url)}/favicon.ico" alt="" style="width: 16px; height: 16px; vertical-align: middle; margin-right: 8px;">`;
    }
    return `${iconContent}${app.name}`;
}


function getDomain(url) {
    return new URL(url).hostname;
}

function toggleMenu() {
    if (isMenuOpen()) {
        hideMenu();
    } else {
        showMenu();
    }
}

function isMenuOpen() {
    return !tabContainer.classList.contains('closed');
}

function showMenu() {
    tabContainer.classList.remove('closed');
    darkenActiveIframe();
    iframes.forEach(iframe => iframe.classList.add('iframe-greyed-out'));
    clearTimeout(inactivityTimer);
    hideFAB();
}

function hideMenu() {
    tabContainer.classList.add('closed');
    undarkenAllIframes();
    iframes.forEach(iframe => iframe.classList.remove('iframe-greyed-out'));
    resetInactivityTimer();
}

function hideFAB() {
    menuToggle.style.right = '-60px';
    document.getElementById('overlay').style.display = 'block';
}

function showFAB() {
    menuToggle.style.right = '20px';
    document.getElementById('overlay').style.display = 'none';
}

function resetInactivityTimer() {
    clearTimeout(inactivityTimer);
    showFAB();
    inactivityTimer = setTimeout(hideFAB, 3000);
}

// Event listeners
['touchstart', 'mousemove', 'scroll', 'click', 'mousedown'].forEach(eventType => {
    document.addEventListener(eventType, resetInactivityTimer);
});

document.addEventListener('click', event => {
    if (!event.target.closest('#tab-container') && !event.target.closest('#menu-toggle') && isMenuOpen()) {
        hideMenu();
    }
});

function dismissBanner() {
    document.getElementById('banner').style.display = 'none';
}

// Initialize
loadApps();
resetInactivityTimer();

function darkenActiveIframe() {
    const activeIframe = document.querySelector('iframe.active');
    if (activeIframe) {
        activeIframe.classList.add('darken');
    }
}

function undarkenAllIframes() {
    const iframes = document.querySelectorAll('iframe');
    iframes.forEach(iframe => iframe.classList.remove('darken'));
}
