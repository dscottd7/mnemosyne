# Base stage with shared configuration
FROM node:18-slim AS base
WORKDIR /app

# Development stage for local development
FROM base AS development
COPY package*.json ./
RUN npm install

# Copy the rest of the application
# In development, this will be overridden by the volume mount in docker-compose
COPY . .

# Set development environment and expose Next.js development port
ENV NODE_ENV=development
ENV PORT=3000
EXPOSE 3000

# Start Next.js in development mode with hot reloading
CMD ["npm", "run", "dev"]

# Builder stage for production
FROM base AS builder
COPY package*.json ./
RUN npm install
COPY . .

# Add build-time environment configuration
# This ensures Next.js can handle both development and production API URLs
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

RUN npm run build

# Production stage
FROM base AS production
# Copy built application from builder
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/public ./public

# Set production environment
ENV NODE_ENV=production
# Use PORT 8080 for Cloud Run but allow override
ENV PORT=${PORT:-8080}
EXPOSE ${PORT}

# Runtime environment variable configuration
# This allows the API URL to be configured at runtime
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

# Start the application
CMD ["npm", "start"]