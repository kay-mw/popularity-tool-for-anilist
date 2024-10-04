FROM caddy:2.8.4-alpine

COPY Caddyfile /etc/caddy/Caddyfile
RUN setcap cap_net_bind_service=+ep $(which caddy)
