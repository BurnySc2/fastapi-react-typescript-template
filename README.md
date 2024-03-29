# fastapi-react-typescript-template

# TODO
- explain folder structure
- explain each config file 
- add docker compose for development inside docker

# Requirement

- Python 3.7 or newer (for backend and e2e/integration tests)
- Node.js 12+ (for frontend)
- Docker (for e2e/integration test)

# Installation

Install node and python 3.7+

```
pip install poetry --user
poetry install
cd frontend && npm install && cd ..
```

# Development

```
npm run start
poetry run uvicorn backend.main:app --reload --host localhost --port 8000
```

# Deploy

Build the front end and host it somewhere (e.g. github pages)

```
npm run build
```

Launch the backend on a server

```
poetry run uvicorn backend.main:app --host localhost --port 8000
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

## Test backend

```
poetry run pytest backend/test
```

## Test frontend

```
npm run test
```

## End-to-end test

Start frontend dev server, then click a few buttons and make sure the site loads correctly (and how quickly, with benchmark tests).

```
poetry run pytest test/test_e2e.py
```

## Integration test

Start backend and frontend server, then make sure that server responses are correct.

```
poetry run pytest test/test_integration.py
```

# Install and run all pre-commit hook scripts

```py
poetry run pre-commit install
poetry run pre-commit run --all-files
```

This runs autoformatting, checks and tests

# Upgrade packages to latest major version
`npx npm-check-updates -u`

# Autoformatting

Done by pre commit hook

```
npx prettier --write "src/**/*.tsx"
yapf ./**/*.py -i
```
