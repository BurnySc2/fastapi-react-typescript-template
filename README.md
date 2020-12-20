# sanic-react-typescript-template

# Requirement

- Python 3.7 or newer 
- Node.js

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
poetry run python main.py
```
Or to autorestart backend server:
```
poetry run uvicorn main:app --reload
```

# Deploy

Create the front end and host it somewhere (e.g. github pages)
```
npm run build
```

Launch the backend on a server
```
pip install poetry --user
poetry install
poetry run python main.py
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

# Autoformatting

```
npx prettier --write "**/*.tsx"
black --line-length 120 .
```


