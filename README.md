### requirements:

    python 3.10

### how to run:

    # install requirments
    pip install poetry
    poetry install

    # pass the input file path through the env variable
    export CLOUD_ENVIRONMENT_FILE_PATH="absolute/path/to/your/file"

    # run application
    cd src
    poetry run uvicorn main:app

### swagger

    http://localhost:8000/docs
