<p align="center">
	<img width="200px" src="moonmen/static/images/icon-text.png" alt="moonmen">
</p>
<p align="center">Pain-free self-hosted project management app for small teams</p>
<p align="center">
	<img src="https://img.shields.io/github/license/EXLER/moonmen.svg?style=flat-square">
</p>

## Requirements

* Python >= 3.6
* Flask >= 2.0.2

## Installation

```bash
$ poetry install
```

## Usage

```bash
$ export FLASK_APP=moonmen

# Initialize SQLite database
$ flask init-db

# Initialize project (instance)
$ flask init-project <project_name>

# Run using Flask's development server
$ flask run

# Run using Gunicorn
$ gunicorn -w 4 -b 127.0.0.1:8000 "moonmen:create_app()"
```

## License

Copyright (c) 2019-2021 by ***Kamil Marut***.

*moonmen* is under the terms of the [MIT License](https://tldrlegal.com/license/mit-license), following all clarifications stated in the [license file](LICENSE).
