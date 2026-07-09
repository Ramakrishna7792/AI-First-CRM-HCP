import { useEffect } from 'react';
import {
  Avatar, Box, Button, Card, CardContent, Chip, Divider, Grid, Stack, Typography,
} from '@mui/material';
import { ArrowBack, BusinessOutlined, LocalHospital, LocationOnOutlined, PersonOutline } from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate, useParams } from 'react-router-dom';
import { fetchDoctors } from '../store/doctorSlice';
import { fetchInteractions } from '../store/interactionSlice';
import InteractionCard from '../components/interactions/InteractionCard';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ErrorState from '../components/common/ErrorState';
import EmptyState from '../components/common/EmptyState';

export default function DoctorDetailsPage() {
  const { doctorId } = useParams();
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const doctors = useSelector((state) => state.doctors);
  const interactions = useSelector((state) => state.interactions);
  useEffect(() => {
    if (!doctors.items.length) dispatch(fetchDoctors());
    if (!interactions.items.length) dispatch(fetchInteractions());
  }, [dispatch, doctors.items.length, interactions.items.length]);
  const doctor = doctors.items.find((item) => String(item.id) === doctorId)
    || interactions.items.find((item) => String(item.doctor_id) === doctorId)?.doctor;
  const history = interactions.items.filter((item) => String(item.doctor_id) === doctorId);
  if ((doctors.loading || interactions.loading) && !doctor) return <LoadingSpinner label="Loading doctor profile…" />;
  if (!doctor) return <ErrorState title="Doctor not found"
    message="This doctor may not be available in your workspace."
    onRetry={() => { dispatch(fetchDoctors()); dispatch(fetchInteractions()); }} />;
  return (
    <Box>
      <Button startIcon={<ArrowBack />} color="inherit" onClick={() => navigate(-1)} sx={{ mb: 2 }}>Back</Button>
      <Card sx={{ mb: 3, overflow: 'visible' }}>
        <CardContent sx={{ p: { xs: 2.5, md: 4 } }}>
          <Stack direction={{ xs: 'column', sm: 'row' }} alignItems={{ xs: 'flex-start', sm: 'center' }}
            justifyContent="space-between" gap={2}>
            <Stack direction="row" alignItems="center" spacing={2}>
              <Avatar sx={{ width: 68, height: 68, bgcolor: 'primary.light', color: 'primary.main' }}>
                <PersonOutline fontSize="large" />
              </Avatar>
              <Box>
                <Typography variant="h4">{doctor.name}</Typography>
                <Stack direction="row" gap={1} mt={1} flexWrap="wrap">
                  <Chip size="small" icon={<LocalHospital />} label={doctor.specialization || 'General practice'} />
                  <Chip size="small" variant="outlined" label={`${history.length} interactions`} />
                </Stack>
              </Box>
            </Stack>
            <Button variant="contained" onClick={() => navigate('/log')}>Log new interaction</Button>
          </Stack>
          <Divider sx={{ my: 3 }} />
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <Stack direction="row" spacing={1.5}><BusinessOutlined color="action" />
                <Box><Typography variant="caption" color="text.secondary">Institution</Typography>
                  <Typography>{doctor.hospital || 'Not provided'}</Typography></Box></Stack>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Stack direction="row" spacing={1.5}><LocationOnOutlined color="action" />
                <Box><Typography variant="caption" color="text.secondary">Location</Typography>
                  <Typography>{doctor.city || 'Not provided'}</Typography></Box></Stack>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
      <Typography variant="h5" mb={0.5}>Interaction history</Typography>
      <Typography color="text.secondary" mb={2.5}>Previous engagements with this HCP</Typography>
      {!history.length ? <Card><EmptyState title="No interactions yet"
        description="Start building this HCP relationship by logging an interaction."
        actionLabel="Log interaction" onAction={() => navigate('/log')} /></Card> :
        <Stack spacing={2}>{history.map((item) => <InteractionCard key={item.id} interaction={item} />)}</Stack>}
    </Box>
  );
}
