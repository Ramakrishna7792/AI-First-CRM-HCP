import { Alert, Button, Stack, Typography } from '@mui/material';
import { Refresh } from '@mui/icons-material';

export default function ErrorState({ title = 'Something went wrong', message, onRetry }) {
  return (
    <Alert severity="error" variant="outlined">
      <Stack spacing={1} alignItems="flex-start">
        <Typography fontWeight={700}>{title}</Typography>
        <Typography variant="body2">{message || 'Please try again in a moment.'}</Typography>
        {onRetry && <Button size="small" startIcon={<Refresh />} onClick={onRetry}>Try again</Button>}
      </Stack>
    </Alert>
  );
}
