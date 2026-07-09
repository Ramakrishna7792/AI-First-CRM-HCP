import { Box, Button } from '@mui/material';
import { Add } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import PageHeader from '../components/common/PageHeader';
import InteractionList from '../components/interactions/InteractionList';

export default function InteractionsPage() {
  const navigate = useNavigate();
  return (
    <Box>
      <PageHeader title="Interaction History"
        subtitle="Search and review all recorded healthcare professional engagements"
        action={<Button variant="contained" startIcon={<Add />} onClick={() => navigate('/log')}>Log interaction</Button>} />
      <InteractionList />
    </Box>
  );
}
