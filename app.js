const apps = [
    { name: "Plex", url: "https://plex.doze.dev" },
    { name: "Flame", url: "https://start.doze.dev", icon: "🔥" },
    { name: "Media Status Dashboard", url: "https://uptime.doze.dev/status/plex" },
    { name: "Media Requests", url: "https://requests.doze.dev" }
];

const tabContainer = document.getElementById('tab-container');
const appFrame = document.getElementById('app-frame');

apps.forEach(app => {
    const faviconImg = app.icon ? getFaviconImg(app.icon) : `<img src="http://${getDomain(app.url)}/favicon.ico" alt="" style="width: 16px; height: 16px; vertical-align: middle; margin-right: 8px;">`;

    const tab = document.createElement('button');
    tab.className = 'tab';
    tab.innerHTML = `${faviconImg}${app.name}`;
    tab.onclick = () => {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        appFrame.src = app.url;
    };
    tabContainer.appendChild(tab);
});

const firstButton = tabContainer.querySelector('button');
if (firstButton) {
    firstButton.click();
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

let inactivityTimer;

function resetTimer() {
    clearTimeout(inactivityTimer);
    inactivityTimer = setTimeout(() => {
        if (window.innerWidth < 768 && tabContainer.style.right === '0px') {
            toggleMenu();
        }
    }, 5000); // 5 seconds of inactivity
}

function toggleMenu() {
    tabContainer.style.right = tabContainer.style.right === '0px' ? '-200px' : '0px';
}

window.onload = resetTimer;
document.addEventListener('touchstart', resetTimer);
document.addEventListener('click', resetTimer);
document.addEventListener('scroll', resetTimer);

window.onload = () => {
    if (window.innerWidth < 768) {
        tabContainer.style.right = '-200px';
    }
};
