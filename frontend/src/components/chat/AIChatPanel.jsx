import { useEffect, useRef, useState } from 'react';
import {
  Alert, Box, Button, Card, CardContent, CardHeader, Chip, CircularProgress, Divider,
  IconButton, Stack, TextField, Typography,
} from '@mui/material';
import { AutoAwesome, DeleteSweep, Send } from '@mui/icons-material';
import { useDispatch } from 'react-redux';
import useChat from '../../hooks/useChat';
import ChatMessage from './ChatMessage';
import { clearChat } from '../../store/chatSlice';

const example = 'I met Dr. Sharma today in person. We discussed Product X efficacy. I shared the clinical brochure and two sample packs. The response was positive and I will follow up next week.';

export default function AIChatPanel() {
  const [input, setInput] = useState('');
  const { messages, loading, warnings, sendMessage } = useChat();
  const dispatch = useDispatch();
  const endRef = useRef(null);
  useEffect(() => { endRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages, loading]);
  const submit = () => {
    const message = input.trim();
    if (!message || loading) return;
    setInput(''); sendMessage(message);
  };
  return (
    <Card sx={{ height: '100%', minHeight: 680, display: 'flex', flexDirection: 'column',
      position: { lg: 'sticky' }, top: { lg: 88 } }}>
      <CardHeader avatar={<Box sx={{ bgcolor: 'primary.light', color: 'primary.main', borderRadius: 2,
        width: 40, height: 40, display: 'grid', placeItems: 'center' }}><AutoAwesome /></Box>}
        title="AI Chat" subheader="Describe the visit naturally"
        action={<IconButton aria-label="Clear conversation" onClick={() => dispatch(clearChat())}><DeleteSweep /></IconButton>} />
      <Divider />
      <CardContent sx={{ p: 0, display: 'flex', flexDirection: 'column', flex: 1, minHeight: 0 }}>
        <Box sx={{ p: 2, flex: 1, overflowY: 'auto', minHeight: 420, maxHeight: 600 }}>
          {messages.map((message) => <ChatMessage key={message.id} message={message} />)}
          {loading && <Stack direction="row" alignItems="center" gap={1.5} ml={5.5}>
            <CircularProgress size={16} /><Typography variant="body2" color="text.secondary">Extracting interaction details…</Typography>
          </Stack>}
          <div ref={endRef} />
        </Box>
        {!!warnings.length && <Box px={2}>{warnings.map((warning) =>
          <Alert key={warning} severity="warning" sx={{ mb: 1 }}>{warning}</Alert>)}</Box>}
        <Box px={2} pb={1.5}>
          <Typography variant="caption" color="text.secondary">Need an example?</Typography>
          <Chip label="Use sample visit" size="small" variant="outlined" onClick={() => setInput(example)}
            sx={{ ml: 1, cursor: 'pointer' }} />
        </Box>
        <Divider />
        <Box p={2}>
          <TextField fullWidth multiline minRows={3} maxRows={6} value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); submit(); } }}
            placeholder="Tell me who you met, what you discussed, the outcome, and next steps…"
            disabled={loading} />
          <Stack direction="row" justifyContent="space-between" alignItems="center" mt={1.25}>
            <Typography variant="caption" color="text.secondary">Enter to send · Shift+Enter for a new line</Typography>
            <Button variant="contained" endIcon={<Send />} onClick={submit} disabled={!input.trim() || loading}>Send</Button>
          </Stack>
        </Box>
      </CardContent>
    </Card>
  );
}
