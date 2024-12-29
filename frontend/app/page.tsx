'use client';

import { useState, useEffect, useRef } from 'react';
import { Container, TextInput, Button, Stack, Title, Paper, Box, AppShell } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import ChatMessage from '../components/ChatMessage';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Create a ref for the messages container and the last message
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  // This effect handles scrolling to the latest message whenever messages change
  useEffect(() => {
    // We add a small delay to ensure the DOM has updated with the new message
    const scrollTimeout = setTimeout(() => {
      if (messagesEndRef.current) {
        messagesEndRef.current.scrollIntoView({ 
          behavior: 'smooth',
          block: 'end'
        });
      }
    }, 100);

    // Cleanup timeout to prevent memory leaks
    return () => clearTimeout(scrollTimeout);
  }, [messages]); // This effect runs whenever messages array changes

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    const API_URL = process.env.NODE_ENV === 'production' ?  'https://mnemosyne-backend-302656282665.us-central1.run.app' : 'http://localhost:8000';
    // const API_URL = 'https://mnemosyne-backend-302656282665.us-central1.run.app';
    console.log('NODE_ENV:', process.env.NODE_ENV);
    console.log('API_URL:', API_URL);

      try {
      const response = await fetch(`${API_URL}/api/v1/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: input }),
      });

      if (!response.ok) throw new Error('Failed to get response');

      const data = await response.json();
      
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.answer,
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      notifications.show({
        title: 'Error',
        message: 'Failed to get response from the server',
        color: 'red',
      });
    } finally {
      setIsLoading(false);
    }
  }

  return (
    // AppShell provides a base layout structure
    <AppShell
      header={{ height: 60 }}
      footer={{ height: 120 }}
      padding="md"
    >
      {/* Header Section */}
      <AppShell.Header>
        <Container size="lg" h="100%">
          <Box py="md">
            <Title order={1}>ScottGPT</Title>
          </Box>
        </Container>
      </AppShell.Header>

      {/* Main Content Section */}
      <AppShell.Main>
        <Container size="lg">
          <Paper 
            withBorder 
            p="md" 
            ref={scrollContainerRef}
            style={{ 
              minHeight: 'calc(100vh - 280px)',
              overflowY: 'auto',
              display: 'flex',
              flexDirection: 'column'
            }}
          >
            {/* Messages container with flex-grow to push content to the top */}
            <Stack gap="md" style={{ flexGrow: 1 }}>
              {messages.map((message, index) => (
                <ChatMessage key={index} message={message} />
              ))}
              {/* Invisible div that serves as our scroll target */}
              <div ref={messagesEndRef} style={{ height: 0 }} />
            </Stack>
          </Paper>
        </Container>
      </AppShell.Main>

      {/* Footer Section with Form */}
      <AppShell.Footer>
        <Container size="lg">
          <Box py="md">
            <form onSubmit={handleSubmit}>
              <Stack gap="sm">
                <TextInput
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Message ScottGPT"
                  disabled={isLoading}
                />
                <Button type="submit" loading={isLoading}>
                  Send
                </Button>
              </Stack>
            </form>
          </Box>
        </Container>
      </AppShell.Footer>
    </AppShell>
  );
}