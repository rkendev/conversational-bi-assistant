# mcp_server/Dockerfile
FROM node:20-alpine

# native build deps **plus** CA certificates for HTTPS-Git
RUN apk add --no-cache git python3 make g++ ca-certificates \
 && update-ca-certificates

# 1) clone the public fork
WORKDIR /opt
RUN git clone --depth=1 https://github.com/guidelesslab/postgres-mcp-server.git

# 2) install & build
WORKDIR /opt/postgres-mcp-server
RUN npm ci --omit=dev  \
 && npm run build      \
 && npm link           # adds `postgres-mcp-server` to PATH

# 3) runtime folder
WORKDIR /app
COPY mcp_config.json .

EXPOSE 4000
CMD ["postgres-mcp-server", "--config", "mcp_config.json", "--port", "4000"]
