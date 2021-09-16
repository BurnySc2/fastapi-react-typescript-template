# fastapi-react-typescript-template

# Requirement

-   Python 3.7 or newer
-   Node.js

# Installation

Install node and python 3.7+

```
pip install poetry --user
poetry install
npm install
```

# Development

```
npm run start
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

# Deploy

Build the front end and host it somewhere (e.g. github pages)

```
npm run build
```

Launch the backend on a server

```
poetry install
poetry run uvicorn main:app --host 0.0.0.0 --port 5000
```

# Functionality

## Requests

[x] Communicate between front and backend

[ ] Accept file download (sent via backend)

[ ] Accept file upload

[ ] User register

[ ] User login

[ ] Use cookies to store login? https://sanic.readthedocs.io/en/latest/sanic/cookies.html

# Tests

[ ] How to test a webserver?



# Install and run all pre-commit hook scripts
```py
poetry run pre-commit install
poetry run pre-commit run --all-files
```

This runs pylint, mypy, pytest tests, apply autoformatter yapf

# Upgrade packages to latest major version
`npx npm-check-updates -u`

# Autoformatting

```
npx prettier --write "src/**/*.tsx"
yapf ./**/*.py -i
```
