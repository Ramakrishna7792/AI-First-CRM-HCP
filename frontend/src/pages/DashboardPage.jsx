import { useEffect } from 'react';
import { Box, Button, Card, CardContent, Grid, Stack, Typography } from '@mui/material';
import { Add, EventNote, People, SentimentSatisfied, TrendingUp } from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { fetchInteractions } from '../store/interactionSlice';
import { fetchDoctors } from '../store/doctorSlice';
import PageHeader from '../components/common/PageHeader';
import SummaryCard from '../components/common/SummaryCard';
import InteractionCard from '../components/interactions/InteractionCard';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ErrorState from '../components/common/ErrorState';
import EmptyState from '../components/common/EmptyState';

export default function DashboardPage() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const interactions = useSelector((state) => state.interactions);
  const doctors = useSelector((state) => state.doctors);
  useEffect(() => { dispatch(fetchInteractions()); dispatch(fetchDoctors()); }, [dispatch]);
  const positive = interactions.items.filter((item) => item.sentiment === 'Positive').length;
  const rate = interactions.items.length ? `${Math.round(positive / interactions.items.length * 100)}%` : '0%';
  return (
    <Box>
      <PageHeader title="Dashboard" subtitle="Your HCP engagement performance at a glance"
        action={<Button variant="contained" startIcon={<Add />} onClick={() => navigate('/log')}>Log interaction</Button>} />
      <Grid container spacing={2.5} mb={3.5}>
        <Grid item xs={12} sm={6} lg={3}><SummaryCard label="Total interactions" value={interactions.items.length}
          helper="All recorded visits" icon={<EventNote />} /></Grid>
        <Grid item xs={12} sm={6} lg={3}><SummaryCard label="HCP network" value={doctors.items.length}
          helper="Doctors in your workspace" icon={<People />} color="secondary" /></Grid>
        <Grid item xs={12} sm={6} lg={3}><SummaryCard label="Positive outcomes" value={positive}
          helper="Engaged HCP interactions" icon={<SentimentSatisfied />} color="success" /></Grid>
        <Grid item xs={12} sm={6} lg={3}><SummaryCard label="Positive sentiment" value={rate}
          helper="Across recorded visits" icon={<TrendingUp />} color="warning" /></Grid>
      </Grid>
      <Card>
        <CardContent>
          <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
            <Box><Typography variant="h6">Recent interactions</Typography>
              <Typography variant="body2" color="text.secondary">Latest field activity</Typography></Box>
            <Button onClick={() => navigate('/interactions')}>View all</Button>
          </Stack>
          {interactions.loading && !interactions.items.length ? <LoadingSpinner /> :
            interactions.error && !interactions.items.length ? <ErrorState message={interactions.error}
              onRetry={() => dispatch(fetchInteractions())} /> :
              !interactions.items.length ? <EmptyState title="No activity yet"
                description="Your most recent HCP interactions will appear here."
                actionLabel="Log interaction" onAction={() => navigate('/log')} /> :
                <Stack spacing={1.5}>{interactions.items.slice(0, 5).map((item) =>
                  <InteractionCard key={item.id} interaction={item} compact />)}</Stack>}
        </CardContent>
      </Card>
    </Box>
  );
}
