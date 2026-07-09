import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Box, Typography } from '@mui/material';
import { fetchInteractions, deleteInteraction } from '../../store/interactionSlice';
import { showSnackbar } from '../../store/uiSlice';
import InteractionCard from './InteractionCard';
import LoadingSpinner from '../common/LoadingSpinner';

export default function InteractionList() {
  const dispatch = useDispatch();
  const { items, loading } = useSelector((state) => state.interactions);

  useEffect(() => {
    dispatch(fetchInteractions());
  }, [dispatch]);

  const handleDelete = async (id) => {
    await dispatch(deleteInteraction(id));
    dispatch(showSnackbar({ message: 'Interaction deleted', severity: 'info' }));
  };

  if (loading) return <LoadingSpinner />;

  if (items.length === 0) {
    return (
      <Box textAlign="center" py={6}>
        <Typography color="text.secondary">No interactions recorded yet.</Typography>
      </Box>
    );
  }

  return (
    <Box>
      {items.map((interaction) => (
        <InteractionCard key={interaction.id} interaction={interaction} onDelete={handleDelete} />
      ))}
    </Box>
  );
}
