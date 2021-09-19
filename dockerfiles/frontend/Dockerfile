FROM node:16.9.1-slim

ENV IS_INSIDE_DOCKER=1

# Copy local files over
COPY . $HOME/frontend/
WORKDIR $HOME/frontend

# TEMP debug
RUN echo pwd
RUN ls -la

# Install dependencies
RUN npm install

# Run work script
CMD [ "npm", "run", "start" ]

