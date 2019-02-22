<h1 align="center"><img width="200px" src="./moonmen/static/images/icon-text.png" alt="moonmen"></h1>
<p align="center">Pain-free project manager so you can start developing faster.</p>
<p align="center">
	<img src="https://img.shields.io/github/license/EXLER/moonmen.svg?style=flat-square">
	<img src="https://img.shields.io/badge/python-3.6-blue.svg?style=flat-square">
</p>

***moonmen*** is gathering simple tools needed by many programmers and puts them in one, accessible place. Everything available in seconds after downloading.

## Requirements

* Python 3.6
* Flask 1.0.2 *or greater*
* Gevent 1.4.0 *or greater*

## Installation

```bash
$ pip install -r requirements.txt
```

## Usage

```bash
$ python3 moonmen.py project [-p | --port 8080] [--debug]
```

*moonmen* will detect if the project exists and if not, the user will be prompted for details about the project.  
Choose the password wisely, it **cannot be changed**.

If ran again with the same command, the web interface will be made available (default port: 8080).

## License

Copyright (c) 2019 by ***Kamil Marut***.

*moonmen* is under the terms of the [GPLv3 License](https://www.tldrlegal.com/l/mit), following all clarifications stated in the [license file](LICENSE).
