import { Box, Paper, Typography, Avatar } from '@mui/material';
import { SmartToy as AIIcon, Person as PersonIcon } from '@mui/icons-material';

export default function ChatMessage({ message }) {
  const isUser = message.role === 'user';

  return (
    <Box
      display="flex"
      flexDirection={isUser ? 'row-reverse' : 'row'}
      gap={1.5}
      mb={2}
      alignItems="flex-start"
    >
      <Avatar
        sx={{
          width: 32,
          height: 32,
          bgcolor: isUser ? 'secondary.main' : 'primary.main',
        }}
      >
        {isUser ? <PersonIcon fontSize="small" /> : <AIIcon fontSize="small" />}
      </Avatar>
      <Paper
        elevation={0}
        sx={{
          p: 1.5,
          maxWidth: '80%',
          bgcolor: isUser ? 'primary.main' : 'grey.50',
          color: isUser ? 'white' : 'text.primary',
          borderRadius: 2,
          border: isUser ? 'none' : '1px solid #E8ECF0',
        }}
      >
        <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
          {message.content}
        </Typography>
      </Paper>
    </Box>
  );
}
