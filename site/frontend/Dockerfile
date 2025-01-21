FROM oven/bun:1 AS base
WORKDIR /app

COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile

COPY . .
RUN bun --bun run build

USER bun
EXPOSE 3000/tcp
ENTRYPOINT [ "bun", "run", "./build/index.js" ]
