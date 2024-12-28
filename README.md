# ntmn

Network monitor that tracks and logs latency and disconnections.

## installation

Create a virtual environment and install the app with deps:

```sh
pip install .
```

### development

For development and testing:

```sh
pip install -e .[test]
```

Run tests:

```sh
make test
```

Run linter:

```sh
make lint
```

## usage

Start the monitor with:

```sh
python src/ntmn/core.py
```

Start the API server with:

```sh
./start
```

## api

The app provides the following views:

* [Ping History (100)](http://localhost:8000/pings/)
* [Ping History (custom)](http://localhost:8000/pings/1000/)
* [Disconnect history (100)](http://localhost:8000/)
* [Disconnect history (custom)](http://localhost:8000/1000/)
