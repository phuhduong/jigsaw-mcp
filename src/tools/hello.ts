import { Tool, CallToolResult } from '@modelcontextprotocol/sdk/types.js';

/**
 * Tool definition for hello tool
 */
export const helloToolDefinition: Tool = {
    name: "hello",
    description: "A simple hello tool that greets the user. This is a barebones demo tool.",
    inputSchema: {
        type: "object",
        properties: {
            name: {
                type: "string",
                description: "Name to greet"
            },
        },
        required: ["name"],
    },
};

/**
 * Handles hello tool calls
 * @param {unknown} args - Tool call arguments
 * @returns {Promise<CallToolResult>} Tool call result
 */
export async function handleHelloTool(args: unknown): Promise<CallToolResult> {
    try {
        if (!args || typeof args !== 'object' || !('name' in args)) {
            throw new Error("Invalid arguments: 'name' is required");
        }

        const { name } = args as { name: string };
        const greeting = `Hello, ${name}! This is a barebones MCP server tool.`;

        return {
            content: [{ type: "text", text: greeting }],
            isError: false,
        };
    } catch (error) {
        return {
            content: [
                {
                    type: "text",
                    text: `Error: ${error instanceof Error ? error.message : String(error)}`,
                },
            ],
            isError: true,
        };
    }
}

