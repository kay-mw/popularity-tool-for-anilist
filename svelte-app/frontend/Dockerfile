FROM node:22 AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

CMD HOST=0.0.0.0 PORT=3000 ORIGIN=http://0.0.0.0:3000 node build
