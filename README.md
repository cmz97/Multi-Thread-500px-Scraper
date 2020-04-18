
[![Contributors][contributors-shield]][contributors-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<br />
<p align="center">

  <h1 align="center">Muti-Threaded 500px Scraper</h1>

  <p align="center">
    Selenium based mutilthreaded image scraper for 500px.com
    <br />
    <a href="https://github.com/cmz97/Multi-Thread-500px-Scraper"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/cmz97/Multi-Thread-500px-Scraper">View Demo</a>
    ·
    <a href="https://github.com/cmz97/Multi-Thread-500px-Scraper/issues">Multi-Thread-500px-Scraperrt Bug</a>
    ·
    <a href="https://github.com/cmz97/Multi-Thread-500px-Scraper/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)



<!-- ABOUT THE PROJECT -->
## About The Project

![](https://github.com/cmz97/Multi-Thread-500px-Scraper/blob/master/readmeMedia/cmd.gif)

### Built With

* [Selenium](https://selenium-python.readthedocs.io/)
* [tqdm](https://github.com/tqdm/tqdm)


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* Selenium Python
```sh
pip install selenium
```

* geckodriver

[Get latest releases](https://github.com/mozilla/geckodriver/releases)

_Selenium requires a driver to interface with the chosen browser. Firefox, for example, requires geckodriver, which needs to be installed before the below examples can be run. Make sure it’s in your PATH, e. g., place it in /usr/bin or /usr/local/bin. Failure to observe this step will give you an error selenium.common.exceptions.WebDriverException: Message: ‘geckodriver’ executable needs to be in PATH._

* Python Image Library
```sh
pip install Pillow
```


### Installation

1. Clone the Multi-Thread-500px-Scraper
```sh
git clone https://github.com/cmz97/Multi-Thread-500px-Scraper.git
```

<!-- USAGE EXAMPLES -->
## Usage
```sh
  python3 ./500pxScraperParallelProcess 'kordan'
```
This will download all the picture from user ```kordan``` to directory ```./kordan```. In which there is two folder named ```./kordan/nsfw``` for image that is NSFW and ```./kordan/sfw``` for image that is SFW

The program has only one required input, ```USERNAME```, which is the exact username of your target on 500px.
For example, ```https://500px.com/kordan``` has a username that is ```kordan```
Please always refer to the username from the URL.

Optional argument is defined as follow
```txt
500pxScraperParallelProcess.py -h
usage: 500pxScraperParallelProcess.py [-h] [--MIN_WIDTH]
                                      [--MIN_HEIGHT]
                                      [--MAX_RECAPTURE_TIME]
                                      [--INFINITE_SCROLL_LOAD_WAIT_TIME]
                                      [--INFINITE_SCROLL_END_CONFIRM_REDUN]
                                      [--IMAGE_PAGE_LOAD_TIMEOUT]
                                      [--PORTFOLIO_PAGE_LOAD_TIMEOUT]
                                      [--STUCK_REFRESH_INTERVAL]
                                      [--DEBUG_FLAG]
                                      [--SHOW_BROWSER]
                                      [--NUM_OF_THREAD]
                                      [--IMAGE_FETCH_WAIT]
                                      USER_NAME

Selenium based mutilthreaded image scraper for 500px.com

positional arguments:
  USER_NAME             username from 500px, must be exact

optional arguments:
  -h, --help            show this help message and exit
  --MIN_WIDTH MIN_WIDTH
                        Minimum width of the image to feteched
  --MIN_HEIGHT MIN_HEIGHT
                        Minimum height of the image to feteched
  --MAX_RECAPTURE_TIME MAX_RECAPTURE_TIME
                        Max number of time to try to recapture
  --INFINITE_SCROLL_LOAD_WAIT_TIME INFINITE_SCROLL_LOAD_WAIT_TIME
                        Time in second that the infinite scroll function wait
                        per scroll down motion that allow page to load
  --INFINITE_SCROLL_END_CONFIRM_REDUN INFINITE_SCROLL_END_CONFIRM_REDUN
                        usage refer to github page
  --IMAGE_PAGE_LOAD_TIMEOUT IMAGE_PAGE_LOAD_TIMEOUT
                        Time out in second used by the image fetecher,
                        fetecher re-fectech the image after timed out
  --PORTFOLIO_PAGE_LOAD_TIMEOUT PORTFOLIO_PAGE_LOAD_TIMEOUT
                        Time out in second used by the portfolio list
                        fetecher, fetecher re-fectech the image list after
                        timed out
  --STUCK_REFRESH_INTERVAL STUCK_REFRESH_INTERVAL
                        Time in second that the process wait when a page is
                        unresponsive, i.e, passed the timeout value
  --DEBUG_FLAG DEBUG_FLAG
                        Toggle Verbose Debug Information Display
  --SHOW_BROWSER SHOW_BROWSER
                        Toggle browser visibility
  --NUM_OF_THREAD NUM_OF_THREAD
                        Number of thread used in the program
  --IMAGE_FETCH_WAIT IMAGE_FETCH_WAIT
                        Time in second the thread wait per fetecher process
```

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/cmz97/Multi-Thread-500px-Scraper/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Chengming Zhang - cmkz97@gmail.com

Project Link: [https://github.com/cmz97/Multi-Thread-500px-Scraper](https://github.com/cmz97/Multi-Thread-500px-Scraper)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/badge/contributors-1-brightgreen
[contributors-url]: https://github.com/cmz97/Multi-Thread-500px-Scraper/pulse
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=flat-square
[license-url]: https://github.com/cmz97/Multi-Thread-500px-Scraper/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/chengmingzhang/
[product-screenshot]: images/screenshot.png
