import { Alert, Box, Grid, Typography } from '@mui/material';
import InteractionForm from '../components/interactions/InteractionForm';
import AIChatPanel from '../components/chat/AIChatPanel';

export default function LogInteractionPage() {
  return (
    <Box>
      <Typography variant="h4" fontWeight={700} mb={1}>Log HCP Interaction</Typography>
      <Typography color="text.secondary" mb={3}>
        Enter details manually or describe the visit to the assistant.
      </Typography>
      <Alert severity="info" sx={{ mb: 3 }}>
        AI suggestions populate the same form and are never saved until you review and submit them.
      </Alert>
      <Grid container spacing={3}>
        <Grid item xs={12} lg={6}><InteractionForm /></Grid>
        <Grid item xs={12} lg={6}><AIChatPanel /></Grid>
      </Grid>
    </Box>
  );
}
