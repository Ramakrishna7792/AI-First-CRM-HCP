import { Alert, Box, Grid } from '@mui/material';
import PageHeader from '../components/common/PageHeader';
import InteractionForm from '../components/interactions/InteractionForm';
import AIChatPanel from '../components/chat/AIChatPanel';

export default function LogInteractionPage() {
  return (
    <Box>
      <PageHeader title="Log HCP Interaction"
        subtitle="Capture a visit manually or let the AI assistant structure your notes" />
      <Alert severity="info" variant="outlined" sx={{ mb: 3 }}>
        AI chat updates the form automatically. Review every populated field before saving the interaction.
      </Alert>
      <Grid container spacing={3} alignItems="stretch">
        <Grid item xs={12} lg={7}><InteractionForm /></Grid>
        <Grid item xs={12} lg={5}><AIChatPanel /></Grid>
      </Grid>
    </Box>
  );
}
