import { useState, useRef, useEffect } from 'react';
import {
  Card,
  CardContent,
  CardHeader,
  Box,
  TextField,
  IconButton,
  Divider,
  Alert,
  Chip,
  Typography,
} from '@mui/material';
import { Send as SendIcon, DeleteSweep as ClearIcon, SmartToy as AIIcon } from '@mui/icons-material';
import { useDispatch } from 'react-redux';
import useChat from '../../hooks/useChat';
import ChatMessage from './ChatMessage';
import { clearChat } from '../../store/chatSlice';

const EXAMPLE_PROMPT =
  'I visited Dr Sharma today. He liked Product X. Asked for brochure. Requested samples. Follow-up next week.';

export default function AIChatPanel() {
  const [input, setInput] = useState('');
  const { messages, loading, warnings, sendMessage } = useChat();
  const dispatch = useDispatch();
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;
    const msg = input;
    setInput('');
    await sendMessage(msg);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardHeader
        avatar={<AIIcon color="primary" />}
        title="AI Chat Assistant"
        subheader="Powered by LangGraph + Groq"
        titleTypographyProps={{ fontWeight: 600 }}
        action={
          <IconButton onClick={() => dispatch(clearChat())} title="Clear chat">
            <ClearIcon />
          </IconButton>
        }
      />
      <Divider />
      <CardContent sx={{ flex: 1, display: 'flex', flexDirection: 'column', p: 0 }}>
        <Box
          sx={{
            flex: 1,
            overflowY: 'auto',
            p: 2,
            minHeight: 400,
            maxHeight: 500,
          }}
        >
          {messages.map((msg) => (
            <ChatMessage key={msg.id} message={msg} />
          ))}
          {loading && (
            <Typography variant="body2" color="text.secondary" sx={{ pl: 6, fontStyle: 'italic' }}>
              AI is analyzing your message...
            </Typography>
          )}
          <div ref={messagesEndRef} />
        </Box>

        {warnings.length > 0 && (
          <Box px={2} pb={1}>
            {warnings.map((w, i) => (
              <Alert key={i} severity="warning" sx={{ mb: 0.5 }} variant="outlined">
                {w}
              </Alert>
            ))}
          </Box>
        )}

        <Box px={2} pb={1}>
          <Chip
            label="Try example"
            size="small"
            variant="outlined"
            onClick={() => setInput(EXAMPLE_PROMPT)}
            sx={{ cursor: 'pointer' }}
          />
        </Box>

        <Divider />
        <Box display="flex" gap={1} p={2}>
          <TextField
            fullWidth
            multiline
            maxRows={3}
            placeholder="Describe your HCP visit..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={loading}
            size="small"
          />
          <IconButton
            color="primary"
            onClick={handleSend}
            disabled={!input.trim() || loading}
            sx={{ alignSelf: 'flex-end' }}
          >
            <SendIcon />
          </IconButton>
        </Box>
      </CardContent>
    </Card>
  );
}
