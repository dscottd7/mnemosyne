'use client';

import { MantineProvider, createTheme } from '@mantine/core';
import { Notifications } from '@mantine/notifications';

// Create a theme with your preferred configurations
const theme = createTheme({
  /** Put your theme override here */
  primaryColor: 'blue',
  fontFamily: 'var(--font-inter)', // if you're using a custom font
});

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <MantineProvider theme={theme}>
      <Notifications />
      {children}
    </MantineProvider>
  );
}