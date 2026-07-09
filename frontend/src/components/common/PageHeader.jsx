import { Box, Stack, Typography } from '@mui/material';

export default function PageHeader({ title, subtitle, action }) {
  return (
    <Stack direction={{ xs: 'column', sm: 'row' }} justifyContent="space-between"
      alignItems={{ xs: 'flex-start', sm: 'center' }} spacing={2} mb={3}>
      <Box>
        <Typography variant="h4">{title}</Typography>
        {subtitle && <Typography color="text.secondary" mt={0.5}>{subtitle}</Typography>}
      </Box>
      {action}
    </Stack>
  );
}
