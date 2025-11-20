#!/usr/bin/env node

import { loadConfig } from './config.js';
import { parseArgs } from './cli.js';
import { createStandaloneServer } from './server.js';
import { runStdioTransport, startHttpTransport } from './transport/index.js';

/**
 * Main entry point for the Jigsaw MCP Server
 * 
 * Transport selection logic:
 * 1. --stdio flag forces STDIO transport
 * 2. --port flag or PORT env var triggers HTTP transport
 * 3. Default: HTTP for Dedalus deployment
 */
async function main() {
    try {
        const config = loadConfig();
        const cliOptions = parseArgs();
        
        // Determine transport mode
        const shouldUseHttp = cliOptions.port || (process.env.PORT && !cliOptions.stdio);
        const port = cliOptions.port || config.port;
        
        if (shouldUseHttp) {
            // HTTP transport for production/cloud deployment
            startHttpTransport({ ...config, port });
        } else {
            // STDIO transport for local development
            const server = createStandaloneServer();
            await runStdioTransport(server);
        }
    } catch (error) {
        console.error("Fatal error running Jigsaw MCP server:", error);
        process.exit(1);
    }
}

// Run the server
main();

