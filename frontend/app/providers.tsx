'use client';

import { MantineProvider, createTheme } from '@mantine/core';
import { Notifications } from '@mantine/notifications';

// Create a theme with your preferred configurations
const theme = createTheme({
  /** Put your theme override here */
  primaryColor: 'blue',
  fontFamily: 'Inter, sans-serif', // Sets the default font family
  fontFamilyMonospace: 'Monaco, Courier, monospace', // Sets the monospace font family
  headings: {
    // Customizes all heading elements (h1-h6)
    fontFamily: 'Roboto, sans-serif',
    sizes: {
      h1: {
        fontSize: '2.25rem',
        fontWeight: '700',
        lineHeight: '1.3',
      },
      h2: { fontSize: '1.875rem' },
      h3: { fontSize: '1.5rem' },
      // ... and so on for other heading levels
    },
  },
  components: {
    // Customize specific components
    Text: {
      defaultProps: {
        size: 'md',
        fw: 400, // font-weight
      },
    },
    Title: {
      defaultProps: {
        fw: 600,
      },
    },
  },
});

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <MantineProvider theme={theme}>
      <Notifications />
      {children}
    </MantineProvider>
  );
}