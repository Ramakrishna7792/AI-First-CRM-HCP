import { Box, Button, Typography } from '@mui/material';
import { Add } from '@mui/icons-material';

export default function EmptyState({ title, description, actionLabel, onAction }) {
  return (
    <Box textAlign="center" py={7} px={2}>
      <Typography variant="h6" mb={0.5}>{title}</Typography>
      <Typography color="text.secondary" mb={2}>{description}</Typography>
      {onAction && <Button variant="contained" startIcon={<Add />} onClick={onAction}>{actionLabel}</Button>}
    </Box>
  );
}
