# Flip-Flop

Flip-Flop is a web application designed to consolidate various web apps into a single, easy-to-navigate interface with a tabbed structure. It's ideal for integrating multiple self-hosted services like Plex, Flame, and others.

## Features

- Tabbed interface for easy navigation.
- Smooth transition between different web apps.
- Customizable tabs with support for favicons or icons.
- Responsive design for desktop and mobile compatibility.

## Installation

To run Flip-Flop, you need Docker installed on your system.

1. Clone the repository:

`git clone https://github.com/mullinmax/flip-flop.git`

2. Navigate to the project directory:

`cd flip-flop`

3. Build the Docker image:

`docker build -t flip-flop .`

4. Run the container:

`docker run -p 80:80 flip-flop`


The application should now be running on [http://localhost](http://localhost).

## Configuration

You can configure the tabs by editing the `apps` array in `app.js`.

## Contributing

Contributions are welcome. Please feel free to submit pull requests or open issues for improvements and bug fixes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## TODO

- dev:
    - [x] publish docker image
    - [x] testing
    - [x] reduce docker image size using slim/alpine base
    - [x] setup pre-commit
    - [x] protect main branch
    - [x] contibuting guide
    - [ ] setup releases
    - [ ] badges for tests passing, current version, etc.
- server:
    - [x] parse docker labels
    - [x] flask-ify
    - [ ] docker labels for order
    - [ ] yaml based config parsing
        - [ ] custom app name
        - [ ] custom themes/theme switching
        - [ ] manual url/icon/name additions
        - [ ] custom favicon for app
        - [ ] banner/alerts
- front end:
    - [ ] hide FAB when menu is open
    - [ ] close menu on any click away
    - [ ] grey-out iframe when menu is open
    - [ ] better menu item spacing/styles
    - [ ] show banners/alerts (downtime annoucements)
- documentation:
    - [ ] how to install
    - [ ] how to configure
