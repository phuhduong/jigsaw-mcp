# Deployment Guide for Jigsaw MCP Server

## Structure Overview

This is a barebones TypeScript MCP server following the Brave Search template pattern:

```
mcp_server/
├── src/
│   ├── index.ts          # Main entry point
│   ├── server.ts         # MCP server setup
│   ├── config.ts         # Configuration
│   ├── cli.ts            # CLI argument parsing
│   ├── tools/
│   │   ├── hello.ts      # Hello tool implementation
│   │   └── index.ts      # Tool exports
│   └── transport/
│       ├── http.ts       # HTTP/Streamable HTTP transport
│       ├── stdio.ts      # STDIO transport
│       └── index.ts      # Transport exports
├── dist/                 # Compiled JavaScript
├── package.json          # Dependencies and scripts
├── tsconfig.json         # TypeScript config
├── Dockerfile            # Docker build config
└── README.md
```

## Key Features

- **Single Tool**: `hello` - A simple greeting tool for testing
- **Streamable HTTP Transport**: Compatible with Dedalus deployment
- **Session Management**: Supports multiple concurrent connections
- **Health Check**: `/health` endpoint for monitoring

## Local Testing

```bash
# Build
npm install
npm run build

# Run HTTP transport
npm start

# Test health endpoint
curl http://localhost:8000/health

# Test MCP initialization
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {"tools": {}},
      "clientInfo": {"name": "TestClient", "version": "1.0.0"}
    }
  }'
```

## Deploy to Dedalus

1. **Push to GitHub**: Ensure all files are committed and pushed
2. **Deploy**: Run `dedalus deploy . --name "jigsaw-mcp"`
3. **Verify**: Check Dedalus dashboard for deployment status

## Differences from Python Template

- **Language**: TypeScript/Node.js instead of Python
- **Transport**: Uses `@modelcontextprotocol/sdk` directly
- **Structure**: Matches Brave Search template exactly
- **Tool**: Single `hello` tool instead of multiple utility tools

## Expected Behavior

When deployed to Dedalus, the server should:
1. Build successfully (TypeScript compilation)
2. Start on port 8000
3. Respond to `/health` endpoint
4. Accept MCP protocol requests on `/mcp`
5. List the `hello` tool when queried
6. Execute the `hello` tool when called

## Troubleshooting

If Dedalus validation fails:
1. Check build logs for TypeScript compilation errors
2. Verify Dockerfile builds successfully
3. Ensure `dist/index.js` exists after build
4. Check that port 8000 is exposed
5. Verify the server starts without errors

