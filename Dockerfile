# Use official Node.js runtime as base image
FROM public.ecr.aws/docker/library/node:22-alpine

# Set working directory inside container
WORKDIR /app

# Copy package files first for better caching
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install --ignore-scripts

# Copy source code
COPY . .

# Build the TypeScript code
RUN npm run build

# Create a non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S mcp -u 1001

# Change ownership of app directory to non-root user
RUN chown -R mcp:nodejs /app

# Switch to non-root user
USER mcp

# Set environment variables for Lambda Web Adapter
ENV NODE_ENV=production
ENV PORT=8000
ENV AWS_LAMBDA_EXEC_WRAPPER=/opt/extensions/lambda-adapter

# Expose port 8000 for the MCP server
EXPOSE 8000

# Command to run the server
CMD ["node", "dist/index.js", "--port", "8000"]

