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
    const apiUrl = process.env.NEXT_PUBLIC_API_URL

    // Define the API rewrite rule
    const apiRewrite = {
      source: '/api/:path*',
      destination: apiUrl 
        ? `${apiUrl}/api/:path*`
        : 'http://backend:8000/api/:path*'
    }

    // Return complete rewrite configuration with all required stages
    return {
      beforeFiles: [apiRewrite],  // Your API routing rule
      afterFiles: [],             // Required by type system but empty
      fallback: []               // Required by type system but empty
    }
  },

  // Environment variable configuration
  env: {
    // Make API URL available throughout the application
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  }
};

export default nextConfig;
