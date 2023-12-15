// Sample data, replace with dynamic data from config file later
const apps = [
    { name: "Plex", url: "https://plex.doze.dev"},
    { name: "Flame", url: "https://start.doze.dev", icon: "🔥" },
    { name: "Media Status Dashboard", url: "https://uptime.doze.dev/status/plex" },
    { name: "Media Requests", url: "https://requests.doze.dev"}
];

const tabContainer = document.getElementById('tab-container');
const appFrame = document.getElementById('app-frame');

apps.forEach(app => {
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
// Find the first button in the tabContainer and click it
const firstButton = tabContainer.querySelector('button');
if (firstButton) {
    firstButton.click();
}


let hoverTimeout;

tabContainer.onmouseover = () => {
    clearTimeout(hoverTimeout);
    tabContainer.style.top = '0';
};

tabContainer.onmouseout = () => {
    hoverTimeout = setTimeout(() => {
        tabContainer.style.top = '-50px'; // Adjust based on your tab container height
    }, 3000); // Time in milliseconds; adjust as needed
};

function toggleTabBar() {
    const currentTop = tabContainer.style.top;
    tabContainer.style.top = currentTop === '0px' ? '-50px' : '0';
}