import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Enable standalone output for better GCP compatibility
  output: 'standalone',
  
  // Enable transpilation of Mantine packages
  transpilePackages: [
    '@mantine/core',
    '@mantine/hooks',
    '@mantine/form',
    '@mantine/notifications'
  ],

  // Enable Docker hot reload for local development
  webpack: (config) => {
    config.watchOptions = {
      poll: 1000,
      aggregateTimeout: 300,
    }
    return config
  },

  // Configure API routing based on environment
  async rewrites() {
    // Get the API URL from environment variable
    const apiUrl = process.env.NEXT_PUBLIC_API_URL

    // If no API URL is set, assume we're in development
    if (!apiUrl) {
      return {
        beforeFiles: [{
          source: '/api/:path*',
          destination: 'http://backend:8000/api/:path*' // Docker service name
        }]
      }
    }

    // For production/GCP environment, use the provided API URL
    return {
      beforeFiles: [{
        source: '/api/:path*',
        destination: `${apiUrl}/api/:path*`
      }]
    }
  },

  // Environment variable configuration
  env: {
    // Make API URL available throughout the application
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  }
};

export default nextConfig;
