# Jigsaw MCP Server

A barebones MCP server for Dedalus deployment with a single demo tool.

## Features

- **Hello Tool**: A simple greeting tool for testing MCP server functionality
- **Streamable HTTP Transport**: Compatible with Dedalus deployment
- **TypeScript**: Type-safe implementation

## Tools

- **hello**
  - A simple greeting tool
  - Inputs:
    - `name` (string, required): Name to greet

## Build

```bash
npm install
npm run build
```

## Run

```bash
# HTTP transport (for Dedalus)
npm start

# Or with custom port
node dist/index.js --port 8000

# STDIO transport (for local testing)
node dist/index.js --stdio
```

## Docker

```bash
docker build -t jigsaw-mcp:latest .
docker run -p 8000:8000 jigsaw-mcp:latest
```

## Deploy to Dedalus

1. Push to GitHub
2. Deploy with: `dedalus deploy . --name "jigsaw-mcp"`
3. The server will be available at the Dedalus-provided URL

## License

MIT

