import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Paper,
} from '@mui/material';
import {
  People as PeopleIcon,
  EventNote as EventIcon,
  SentimentSatisfied as SentimentIcon,
  TrendingUp as TrendIcon,
} from '@mui/icons-material';
import { fetchInteractions } from '../store/interactionSlice';
import { fetchDoctors } from '../store/doctorSlice';
import InteractionCard from '../components/interactions/InteractionCard';
import LoadingSpinner from '../components/common/LoadingSpinner';

function StatCard({ title, value, icon, color }) {
  return (
    <Card>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Box>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              {title}
            </Typography>
            <Typography variant="h4" fontWeight={700}>
              {value}
            </Typography>
          </Box>
          <Paper
            sx={{
              p: 1.5,
              bgcolor: `${color}.50`,
              color: `${color}.main`,
              borderRadius: 2,
            }}
            elevation={0}
          >
            {icon}
          </Paper>
        </Box>
      </CardContent>
    </Card>
  );
}

export default function DashboardPage() {
  const dispatch = useDispatch();
  const { items: interactions, loading } = useSelector((state) => state.interactions);
  const { items: doctors } = useSelector((state) => state.doctors);

  useEffect(() => {
    dispatch(fetchInteractions({ limit: 10 }));
    dispatch(fetchDoctors());
  }, [dispatch]);

  const positiveCount = interactions.filter((i) => i.sentiment === 'Positive').length;
  const recentInteractions = interactions.slice(0, 5);

  if (loading && interactions.length === 0) return <LoadingSpinner />;

  return (
    <Box>
      <Typography variant="h4" fontWeight={700} mb={1}>
        Dashboard
      </Typography>
      <Typography variant="body1" color="text.secondary" mb={3}>
        AI-First CRM overview for Healthcare Professional interactions
      </Typography>

      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard title="Total Interactions" value={interactions.length} icon={<EventIcon />} color="primary" />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard title="HCPs in Network" value={doctors.length || '—'} icon={<PeopleIcon />} color="secondary" />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard title="Positive Sentiment" value={positiveCount} icon={<SentimentIcon />} color="success" />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Engagement Rate"
            value={interactions.length ? `${Math.round((positiveCount / interactions.length) * 100)}%` : '—'}
            icon={<TrendIcon />}
            color="warning"
          />
        </Grid>
      </Grid>

      <Typography variant="h6" fontWeight={600} mb={2}>
        Recent Interactions
      </Typography>
      {recentInteractions.length === 0 ? (
        <Typography color="text.secondary">No recent interactions. Log your first HCP visit!</Typography>
      ) : (
        recentInteractions.map((interaction) => (
          <InteractionCard key={interaction.id} interaction={interaction} />
        ))
      )}
    </Box>
  );
}
