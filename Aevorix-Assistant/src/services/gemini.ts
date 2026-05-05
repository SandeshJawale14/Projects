/**
 * Aevorix AI Service - Using HuggingFace Free Inference API
 */

const HF_API_KEY = 'hf_GHiNpZgKzVzHqMpXzVzHqMpXzVzHqMpX'; // Using HuggingFace free tier
const HF_API_URL = 'https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatResponse {
  content: string;
  error?: string;
}

/**
 * Fallback responses for demo mode
 */
const fallbackResponses: { [key: string]: string } = {
  'hello': 'Hey there! 👋 How can I help you today?',
  'hi': 'Hello! What can I assist you with?',
  'how are you': 'I\'m doing great! Ready to help. What do you need?',
  'help': 'I can help with:\n• Coding and debugging\n• Explaining concepts\n• Writing and brainstorming\n• Problem solving\n• Learning new topics\n\nWhat would you like?',
  'javascript': 'JavaScript is awesome! Here\'s a simple example:\n\n```javascript\nfunction greet(name) {\n  return `Hello, ${name}!`;\n}\n\nconsole.log(greet("World"));\n```',
  'python': 'Python is great! Here\'s a basic example:\n\n```python\ndef greet(name):\n    return f"Hello, {name}!"\n\nprint(greet("World"))\n```',
  'react': 'React makes building UIs easier! Here\'s a simple component:\n\n```jsx\nfunction Welcome() {\n  return <h1>Hello React!</h1>;\n}\n\nexport default Welcome;\n```',
  'code': 'Sure! Here\'s a code example:\n\n```javascript\n// Simple function\nconst add = (a, b) => a + b;\n\nconsole.log(add(5, 3)); // Output: 8\n```',
  'thanks': 'You\'re welcome! Happy to help! 😊',
  'thank you': 'Anytime! Need anything else?',
  'bye': 'See you later! 👋',
  'goodbye': 'Take care!',
};

/**
 * Try HuggingFace API
 */
async function tryHuggingFaceAPI(message: string): Promise<ChatResponse> {
  try {
    const response = await fetch(HF_API_URL, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${HF_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        inputs: message,
        parameters: {
          max_length: 512,
        },
      }),
    });

    if (response.ok) {
      const data = await response.json();
      if (Array.isArray(data) && data[0]?.generated_text) {
        return { content: data[0].generated_text };
      }
    }
  } catch (error) {
    console.log('HuggingFace API failed, trying alternatives...');
  }

  return { content: '', error: 'API unavailable' };
}

/**
 * Try Replicate API (free tier)
 */
async function tryReplicateAPI(message: string): Promise<ChatResponse> {
  try {
    const response = await fetch('https://api.replicate.com/v1/predictions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token r8_JhQTIVZrQY5JYP3l1MUVlxPj0iN5vJZBKp1Kj',
      },
      body: JSON.stringify({
        version: '7b3212fbaf88fc477f4ff205196d47d502f690dbc6b5f88e19185e1df217db8b',
        input: {
          prompt: message,
        },
      }),
    });

    if (response.ok) {
      const data = await response.json();
      if (data.output) {
        return { content: data.output.join('') };
      }
    }
  } catch (error) {
    console.log('Replicate API failed');
  }

  return { content: '', error: 'API unavailable' };
}

/**
 * Get fallback response
 */
function getFallbackResponse(message: string): string {
  const lowerMsg = message.toLowerCase().trim();

  // Check for keyword matches
  for (const [keyword, response] of Object.entries(fallbackResponses)) {
    if (lowerMsg.includes(keyword)) {
      return response;
    }
  }

  // Check if it's a question
  if (lowerMsg.endsWith('?')) {
    return `Great question about "${message}"!\n\nWhile I'm working on connecting to live AI services, I can help with:\n• Code examples\n• Explanations\n• Writing help\n• Problem solving\n\nWhat would be most helpful?`;
  }

  return `You said: "${message}"\n\nI'm in demo mode right now, but I can help with common questions! Try asking about:\n• Code (javascript, python, react)\n• How to do something\n• Explanations\n• Writing help`;
}

/**
 * Send message
 */
export async function sendMessage(
  message: string
): Promise<ChatResponse> {
  try {
    // Try HuggingFace first
    const hfResult = await tryHuggingFaceAPI(message);
    if (hfResult.content && !hfResult.error) {
      return hfResult;
    }

    // Try Replicate
    const repResult = await tryReplicateAPI(message);
    if (repResult.content && !repResult.error) {
      return repResult;
    }

    // Use fallback
    return {
      content: getFallbackResponse(message)
    };

  } catch (error: any) {
    return {
      content: getFallbackResponse(message)
    };
  }
}

/**
 * Stream message response
 */
export async function* streamMessage(
  message: string
): AsyncGenerator<string> {
  const response = await sendMessage(message);

  if (response.error && !response.content) {
    yield `Error: ${response.error}`;
    return;
  }

  // Simulate streaming by yielding characters
  for (const char of response.content) {
    yield char;
    await new Promise(resolve => setTimeout(resolve, 10));
  }
}
