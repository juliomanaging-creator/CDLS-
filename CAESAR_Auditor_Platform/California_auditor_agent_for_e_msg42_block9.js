// No API calls - all local processing
const response = await ollama.chat({
  model: 'llama3.2:3b',
  messages: [{ role: 'user', content: prompt }]
});