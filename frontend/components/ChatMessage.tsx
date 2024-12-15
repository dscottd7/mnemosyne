// components/ChatMessage.tsx
import { Paper } from '@mantine/core';

interface ChatMessageProps {
  message: {
    role: 'user' | 'assistant';
    content: string;
  };
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';

  return (
    <Paper
      p="sm"
      bg={isUser ? 'blue.1' : 'gray.0'}
      style={{
        marginLeft: isUser ? 'auto' : 0,
        marginRight: isUser ? 0 : 'auto',
        maxWidth: '80%',
      }}
    >
      {message.content}
    </Paper>
  );
}