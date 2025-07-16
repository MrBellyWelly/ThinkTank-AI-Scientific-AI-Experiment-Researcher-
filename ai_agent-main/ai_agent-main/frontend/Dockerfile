# Use Node.js 20
FROM node:20

WORKDIR /app

# Install dependencies
COPY package.json yarn.lock ./
RUN yarn install

# Copy all files
COPY . .

# Build and start the app
RUN yarn build
CMD ["yarn", "start"]
