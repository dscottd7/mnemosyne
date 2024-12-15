// app/page.tsx
'use client';

import { useState } from 'react';
import { Container, TextInput, Button, Stack, Title, Paper } from '@mantine/core';
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

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/v1/query', {
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
    <Container size="lg">
      <Stack>
        <Title order={1}>ScottGPT</Title>
        
        <Paper withBorder p="md">
          <Stack gap="md">
            {messages.map((message, index) => (
              <ChatMessage key={index} message={message} />
            ))}
          </Stack>
        </Paper>

        <form onSubmit={handleSubmit}>
          <Stack gap="sm">
            <TextInput
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question..."
              disabled={isLoading}
            />
            <Button type="submit" loading={isLoading}>
              Send
            </Button>
          </Stack>
        </form>
      </Stack>
    </Container>
  );
}