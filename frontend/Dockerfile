# Use Node 18 as our base image
FROM node:18-slim

# Set working directory
WORKDIR /app

# First, copy only package files to leverage Docker caching
COPY package*.json ./

# Install dependencies with clean npm cache and proper error logging
RUN set -ex; \
    npm cache clean --force && \
    npm install && \
    # Verify Mantine packages are installed
    npm list @mantine/core && \
    npm list @mantine/hooks && \
    npm list @mantine/notifications

# Copy the rest of the application
# This includes our Next.js config and source files
COPY . .

# Ensure proper permissions for Next.js
RUN chmod -R 777 /app/.next || true

# Expose the port Next.js runs on
EXPOSE 3000

# Set proper environment variables for Next.js
ENV HOSTNAME "0.0.0.0"
ENV PORT 3000
ENV NODE_ENV development

# Start the development server
CMD ["npm", "run", "dev"]