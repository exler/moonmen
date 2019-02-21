<h1 align="center">moonmen</h1>
<p align="center">Pain-free project manager for small teams</p>
<p align="center">
	<img src="https://img.shields.io/github/license/EXLER/moonmen.svg?style=flat-square">
	<img src="https://img.shields.io/badge/python-3.6-blue.svg?style=flat-square">
</p>

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

If ran again with the same command, the web interface will be made available with information printed to the console.

## License

Copyright (c) 2019 by ***Kamil Marut***.

*moonmen* is under the terms of the [GPLv3 License](https://www.tldrlegal.com/l/mit), following all clarifications stated in the [license file](LICENSE).
