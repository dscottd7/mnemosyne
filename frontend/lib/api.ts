const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function queryDocument(question: string) {
  const response = await fetch(`${API_URL}/api/v1/query`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    throw new Error('Failed to fetch response');
  }

  return response.json();
}
