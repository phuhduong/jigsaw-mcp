import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import {
    CallToolRequestSchema,
    ErrorCode,
    ListToolsRequestSchema,
    McpError,
} from '@modelcontextprotocol/sdk/types.js';
import {
    helloToolDefinition,
    handleHelloTool
} from './tools/index.js';

/**
 * Factory function for creating standalone server instances
 * Used by HTTP transport for session-based connections
 * @returns {Server} Configured MCP server instance
 */
export function createStandaloneServer(): Server {
    const server = new Server(
        {
            name: "jigsaw-mcp-server",
            version: "1.0.0",
        },
        {
            capabilities: {
                tools: {},
            },
        },
    );

    // Set up handlers
    server.setRequestHandler(ListToolsRequestSchema, async () => ({
        tools: [helloToolDefinition],
    }));

    server.setRequestHandler(CallToolRequestSchema, async (request) => {
        const { name, arguments: args } = request.params;

        switch (name) {
            case 'hello':
                return handleHelloTool(args);
            
            default:
                throw new McpError(
                    ErrorCode.MethodNotFound,
                    `Unknown tool: ${name}`
                );
        }
    });

    return server;
}

