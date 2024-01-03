# <img src="./src/static/img/flip_flop_logo.jpg" height="40px"> Flip-Flop


![GitHub Actions Status](https://github.com/mullinmax/flip-flop/actions/workflows/docker-publish.yml/badge.svg)
![GitHub Actions Status](https://github.com/mullinmax/flip-flop/actions/workflows/python-tests.yml/badge.svg)
![GitHub Release](https://img.shields.io/github/v/release/mullinmax/flip-flop)
![GitHub issues](https://img.shields.io/github/issues/mullinmax/flip-flop)


Do you self host a suite of containerized web applications and struggle to keep friends and family up to date on what's available and where? Flip-Flop might be the tool for you. It's goal is simple, give users one page to bookmark where they can actually use the applications they want. Flip-Flop uses docker labels to bring all your web interfaces into a tabbed structure with additional features to help communicate things like scheduled maitinance to users.


checkout the [Demo instance!](https://flip-flop-demo.doze.dev)

## Features

- Tabbed interface for easy navigation between apps.
- Customizeable themes, favicons, etc.
- Responsive design for desktop and mobile compatibility. There's room to improve here.
- Banner alerts to communicate with users
- multiple instance support; run as many instances of flip-flop on one host as you like with different content
- minimal if any configuration required. All options available as an environment variable or yaml

## Setup

#### Docker Compose

```docker
version: "3.8"

services:
  flip-flop:
    image: ghcr.io/mullinmax/flip-flop:main
    restart: unless-stopped
    ports:
      - "80:80"
    volumes:
      - "flip-flop-data:/config" # optionally add config.yaml for configuration
      - "/var/run/docker.sock:/var/run/docker.sock:ro" #mount your docker socket as read only
    environment:
    # Sets the page title (what the tab name is)
    - FLIP_FLOP_NAME=Maxwell's Dashboard

    # sets the name of the instance, defaults to "default"
    # allows for multiple flip-flops to run on the same system and have different content
    - FLIP_FLOP_INSTANCE=main

    # Banner information
    - FLIP_FLOP_BANNER_TITLE=Scheduled Downtime 1/1/23
    - FLIP_FLOP_BANNER_BODY=Expect services to be down for scheduled maitinance 1pm-5pm

    # Use to override default
    #- FLIP_FLOP_FAVICON=/config/custom_favicon.ico
    #- FLIP_FLOP_THEME=/config/custom_theme.css

    # Sets internal port number, defaults to 80
    #- FLIP_FLOP_PORT=80

    # Use if your setup requires for some reason
    #- FLIP_FLOP_DOCKER_SOCKET_PATH=/var/run/docker.sock
volumes:
  flip-flop-data:
```

#### Config.yaml
Optionally any configuration variable can be set via `config.yaml` file instead of environment variables. You can even mix-and-match configuration vs env variables. If for example you have two instances with different ports or names you could define those in the environment variables and define things like theme or docker socket path in your config file. Flip-Flop will always first consider environment variables, then the config file and finally defautls. Here is an example setup:

```yaml
# /config/config.yaml

# Sets the page title (what the tab name is)
FLIP_FLOP_NAME: "Maxwell's Dashboard"

# Sets the name of the instance, defaults to "default"
# Allows for multiple flip-flops to run on the same system and have different content
FLIP_FLOP_INSTANCE: "main"

# Banner information
FLIP_FLOP_BANNER_TITLE: "Scheduled Downtime 1/1/23"
FLIP_FLOP_BANNER_BODY: "Expect services to be down for scheduled maintenance 1pm-5pm"

# Use to override defaults
# FLIP_FLOP_FAVICON: "/config/custom_favicon.ico"
# FLIP_FLOP_THEME: "/config/custom_theme.css"

# Sets internal port number, defaults to 80
# FLIP_FLOP_PORT: 80

# Use if your setup requires for some reason
# FLIP_FLOP_DOCKER_SOCKET_PATH: "/var/run/docker.sock"
```

#### Docker Labels

Flip-Flop parses labels on your docker containers to figure out what tabs it should show in the web UI. Here's an example of how they are defined:
```docker
version: "3.8"

networks:
  default:
    external: true
    name: "traefik_default"

services:
  uptime-kuma:
    image: louislam/uptime-kuma:latest
    labels:
      - "traefik.http.routers.uptime-kuma.rule=Host(`uptime.doze.dev`)"
      - "traefik.http.services.uptime-kuma.loadbalancer.server.port=3001"

      # allow iframes: see common issues before using
      #- "traefik.http.routers.uptime-kuma.middlewares=uptime-kuma-modify-headers"
      #- "traefik.http.middlewares.uptime-kuma-modify-headers.headers.customresponseheaders.X-Frame-Options="

      - "flip-flop.main.name=Status Dashboard"
      - "flip-flop.main.priority=5"

      # note that for url and icon I chose not to include main
      # this makes these fields apply to all instances that parse the container
      # This way I onny need to redefine priority and name to add this to another instance
      - "flip-flop.url=https://uptime.doze.dev/status/plex"
      # you only need to define this if you don't want to use the app's favicon. You can use an emoji
      # in the future this will support custom paths to image files
      - "flip-flop.icon=📈"

    volumes:
      - "uptime-kuma-data:/app/data"
volumes:
  uptime-kuma-data:
```

## Common issues

#### X-Frame-Options

Flip-Flop uses iframes in order to allow users to switch between apps without leaving the central page. For good reason, many web applications disable being put into iframes. This prevents [Click jacking](https://en.wikipedia.org/wiki/Clickjacking). The example above includes labels you can use when using traefik as a reverse proxy to allow your app to be put into an iframe. Carefully consider how this impacts your security of yourself and your users. **Use at your own risk**. Thankfully many apps do not have this constraint so you don't have to do this often.

#### Automatic Favicon/Icon not working


Flip-Flop does it's best to automatically grab the best favicon from each app to use as the icon in the menu. Some common causes for it not correctly grabbing the favicon are:
- The app url gets redirected (flip-flop does not currently follow redirects). For example If you host Navidrome at `https://music.domain.com` it will automatically redirect to `https://music.domain.com/app/`. You will need to set the flip flop URL to this second url for the favicon to work.
- The app has basic http authentication enabled. In order for the favicon to be retreived Flip-Flop would need to log into the app. As a rule Flip-Flop is not designed to handle security critical things like passwords so it does not support this.
- leaving off the `https://` or `http://` from the url.

## Contributing

Contributions are welcome. Please feel free to submit pull requests or open issues for improvements and bug fixes. This project is being actively developed and I would love to adapt this to something that's as useful to as many people as possible. I would especially love some help refining the CSS styles and adding some great themes.

A development instance is available [here](https://flip-flop-main.doze.dev) this instance will track the main branch.

## License

This project is licensed under the MIT License - see [the LICENSE file](./LICENSE) for details.

## TODO

These are very roughly in order
#### 1.0:
- dev:
    - [x] publish docker image
    - [x] testing
    - [x] reduce docker image size using slim/alpine base
    - [x] setup pre-commit
    - [x] protect main branch
    - [x] contibuting guide
    - [x] setup releases
    - [x] badges for tests passing, current version, etc.
    - [x] "dev mode" to allow for easier development
- server:
    - [x] parse docker labels
    - [x] flask-ify
    - [x] docker labels for order
    - [x] yaml based config parsing
        - [x] custom app name
        - [x] custom favicon for app
        - [x] banner/alerts
    - [x] different labels for each instance flip-flop.instance.url
- documentation:
    - [x] how to install
    - [x] how to configure
    - [x] iframe headers
    - [x] demo and dev instances
- front end:
    - [x] show banners/alerts (downtime annoucements)
    - [x] hide FAB when menu is open
    - [x] close menu on any click away
    - [x] grey-out iframe when menu is open
    - [x] better menu item spacing/styles
    - [x] FAB hides after so many seconds of inactivity
    - [x] better text scaling for app icons
#### 1.1:
  - [x] crop favicons to content for consistent sizes
  - [x] non- .ico favicon formats when available
  - [x] remove menu close button
  - [x] enforce same-size icons
  - [x] pre-load content for fast load times
  - [x] background process to periodically refresh icons
  - [x] banner overlaps with title on phone screens
  - [x] highlight last active app
  - [x] remove title link
  - [x] make menu button look like app drawer
#### Future:
- front end:
    - [x] spinner when iframe is loading
    - [x] show version in menu
    - [x] "full screen" button
    - [x] add footer/padding at the bottom of the menu
    - [ ] custom colored banners
    - [ ] support for icon set in addition to emojis
    - [ ] split screen apps
    - [ ] Locally Saved Or Server Configured Layouts Of Split Screen Apps
    - [x] repo link in footer
    - [ ] PWA support
    - [ ] tab categories
    - [ ] if iframe fails to load log error and do not display
- server:
    - [x] make minifying js and css optional
    - [ ] reduce size of favicon image (automated resizing?)
    - [ ] transparency detection for favicon creation
    - [ ] custom themes/theme switching
    - [ ] non-docker url/icon/name additions
    - [ ] multiple docker socks support
    - [ ] minifier
    - [ ] bake-in images to html
    - [ ] multi-Emoji Icons Text Wrap So They Fit In Square Image
- dev:
    - [x] automatically update main branch and demo instances on update via webhook
    - [ ] coverage report
    - [ ] increase testing
    - [ ] type hints
    - [ ] sponsor / support via github
