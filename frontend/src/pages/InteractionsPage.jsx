import { Typography, Box } from '@mui/material';
import InteractionList from '../components/interactions/InteractionList';

export default function InteractionsPage() {
  return (
    <Box>
      <Typography variant="h4" fontWeight={700} mb={1}>
        Interaction History
      </Typography>
      <Typography variant="body1" color="text.secondary" mb={3}>
        View and manage all logged HCP interactions
      </Typography>
      <InteractionList />
    </Box>
  );
}
