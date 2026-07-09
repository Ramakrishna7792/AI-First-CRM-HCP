import { Box, Card, CardContent, Stack, Typography } from '@mui/material';

export default function SummaryCard({ label, value, helper, icon, color = 'primary' }) {
  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
          <Box>
            <Typography variant="body2" color="text.secondary" fontWeight={600}>{label}</Typography>
            <Typography variant="h4" mt={1}>{value}</Typography>
            {helper && <Typography variant="caption" color="text.secondary">{helper}</Typography>}
          </Box>
          <Box sx={{ width: 44, height: 44, borderRadius: 2, display: 'grid', placeItems: 'center',
            color: `${color}.main`, bgcolor: `${color}.light` }}>{icon}</Box>
        </Stack>
      </CardContent>
    </Card>
  );
}
