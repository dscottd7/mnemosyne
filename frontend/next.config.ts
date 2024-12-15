import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Enable transpilation of Mantine packages
  transpilePackages: [
    '@mantine/core',
    '@mantine/hooks',
    '@mantine/form',
    '@mantine/notifications'
  ],
  // Enable Docker hot reload
  webpack: (config) => {
    config.watchOptions = {
      poll: 1000,
      aggregateTimeout: 300,
    }
    return config
  },
  // Ensure proper output directory permissions
  output: 'standalone',
  // Add any other Next.js config options
};

export default nextConfig;
