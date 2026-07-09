import { useEffect, useMemo, useState } from 'react';
import { Box, InputAdornment, MenuItem, Stack, TextField } from '@mui/material';
import { Search } from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { fetchInteractions } from '../../store/interactionSlice';
import InteractionCard from './InteractionCard';
import LoadingSpinner from '../common/LoadingSpinner';
import ErrorState from '../common/ErrorState';
import EmptyState from '../common/EmptyState';

export default function InteractionList() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { items, loading, error } = useSelector((state) => state.interactions);
  const [query, setQuery] = useState('');
  const [sentiment, setSentiment] = useState('All');
  useEffect(() => { dispatch(fetchInteractions()); }, [dispatch]);
  const filtered = useMemo(() => items.filter((item) => {
    const matchesText = `${item.doctor?.name || ''} ${item.summary || ''} ${item.topics || ''}`
      .toLowerCase().includes(query.toLowerCase());
    return matchesText && (sentiment === 'All' || item.sentiment === sentiment);
  }), [items, query, sentiment]);
  if (loading && !items.length) return <LoadingSpinner label="Loading interaction history…" />;
  if (error && !items.length) return <ErrorState message={error} onRetry={() => dispatch(fetchInteractions())} />;
  return (
    <Stack spacing={2}>
      <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1.5}>
        <TextField fullWidth placeholder="Search doctor, topic, or summary" value={query}
          onChange={(e) => setQuery(e.target.value)}
          InputProps={{ startAdornment: <InputAdornment position="start"><Search /></InputAdornment> }} />
        <TextField select value={sentiment} onChange={(e) => setSentiment(e.target.value)}
          sx={{ minWidth: { sm: 180 } }} label="Sentiment">
          {['All', 'Positive', 'Neutral', 'Negative'].map((item) => <MenuItem key={item} value={item}>{item}</MenuItem>)}
        </TextField>
      </Stack>
      {!filtered.length ? <Box bgcolor="background.paper" border={1} borderColor="divider" borderRadius={2}>
        <EmptyState title="No interactions found"
          description={items.length ? 'Try adjusting your search or filters.' : 'Log your first HCP interaction to get started.'}
          actionLabel={!items.length ? 'Log interaction' : undefined}
          onAction={!items.length ? () => navigate('/log') : undefined} />
      </Box> : filtered.map((item) => <InteractionCard key={item.id} interaction={item} />)}
    </Stack>
  );
}
