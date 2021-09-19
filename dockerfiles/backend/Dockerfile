FROM python:3.9.6-slim-buster

ENV IS_INSIDE_DOCKER=1

# Install poetry
RUN pip install --no-cache-dir poetry

# Install requirements
RUN mkdir -p $HOME/backend
WORKDIR $HOME/backend
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install -r requirements.txt
# Better use pip instead of poetry while inside docker container

# Copy work scripts
COPY ./backend/ .

# Run work script
CMD [ "poetry", "run", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]


