const tabContainer = document.getElementById('tab-container');
const menuToggle = document.getElementById('menu-toggle');
let inactivityTimer;
let iframes = [];

function loadApps() {
    fetch('/docker-labels')
        .then(response => response.json())
        .then(apps => {
            setupTabs(apps);
        })
        .catch(error => console.error('Error loading apps:', error));
}

function setupTabs(apps) {
    apps.forEach((app, index) => {
        const iframe = document.createElement('iframe');
        iframe.src = app.url;
        iframe.style.display = index === 0 ? 'block' : 'none';
        iframe.style.width = '100%';
        iframe.style.height = '100vh';
        iframe.style.border = 'none';
        iframe.onerror = () => {
            console.error('Error loading iframe for:', app.url);
            iframe.style.display = 'none';
        };
        document.body.appendChild(iframe);
        iframes.push(iframe);

        const tab = document.createElement('button');
        tab.className = 'tab tab-enhanced';
        tab.innerHTML = getTabContent(app);
        tab.onclick = () => {
            selectTab(index);
            hideMenu();
        };
        tabContainer.appendChild(tab);
    });
    selectTab(0);
}

function selectTab(index) {
    iframes.forEach((iframe, i) => {
        iframe.style.display = i === index ? 'block' : 'none';
    });
    document.querySelectorAll('.tab').forEach((tab, i) => {
        tab.classList.toggle('active', i === index);
    });
}

function getTabContent(app) {
    const faviconImg = app.icon ? getFaviconImg(app.icon) : `<img src="https://${getDomain(app.url)}/favicon.ico" alt="" style="width: 16px; height: 16px; vertical-align: middle; margin-right: 8px;">`;
    return `${faviconImg}${app.name}`;
}

function getDomain(url) {
    const a = document.createElement('a');
    a.href = url;
    return a.hostname;
}

function getFaviconImg(url) {
    if (url.startsWith('http')) {
        return `<img src="${url}" alt="" style="width: 16px; height: 16px; vertical-align: middle; margin-right: 8px;">`;
    } else {
        return `<span style="font-size: 16px; vertical-align: middle; margin-right: 8px;">${url}</span>`;
    }
}

function isMenuOpen() {
    return tabContainer.style.right === '0px';
}

function toggleMenu() {
    if (isMenuOpen()) {
        hideMenu();
        showFAB();
        return;
    }
    hideFAB();
    showMenu();
}

function hideMenu() {
    tabContainer.style.right = '-200px';
    tabContainer.classList.add('closed');
    iframes.forEach(iframe => iframe.classList.remove('iframe-greyed-out'));
    resetInactivityTimer();
}

function showMenu() {
    tabContainer.style.right = '0px';
    tabContainer.classList.remove('closed');
    iframes.forEach(iframe => iframe.classList.add('iframe-greyed-out'));
    clearTimeout(inactivityTimer);
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

['touchstart', 'mousemove', 'scroll', 'click', 'mousedown'].forEach(eventType => {
    document.addEventListener(eventType, resetInactivityTimer);
});

document.addEventListener('click', function(event) {
    let targetElement = event.target;

    do {
        if (targetElement == tabContainer) {
            return;
        }
        targetElement = targetElement.parentNode;
    } while (targetElement);

    if (isMenuOpen()) {
        hideMenu();
        showFAB();
    }
});

function dismissBanner() {
    document.getElementById('banner').style.display = 'none';
}

// Initialize
resetInactivityTimer();
loadApps();
