import { Box, CircularProgress, Skeleton, Stack, Typography } from '@mui/material';

export default function LoadingSpinner({ size = 36, label = 'Loading…', skeleton = false }) {
  if (skeleton) {
    return <Stack spacing={1.5}><Skeleton height={88} /><Skeleton height={88} /><Skeleton height={88} /></Stack>;
  }
  return (
    <Box display="flex" flexDirection="column" gap={1.5} justifyContent="center" alignItems="center" p={5}>
      <CircularProgress size={size} />
      <Typography variant="body2" color="text.secondary">{label}</Typography>
    </Box>
  );
}
