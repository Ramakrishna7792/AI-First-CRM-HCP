import { useEffect } from 'react';
import {
  Autocomplete, Box, Button, Card, CardContent, CardHeader, Chip, Divider, Grid,
  MenuItem, Stack, TextField, Typography,
} from '@mui/material';
import { AutoAwesome, RestartAlt, SaveOutlined } from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { fetchDoctors } from '../../store/doctorSlice';
import useInteractions from '../../hooks/useInteractions';

const interactionTypes = ['In-Person', 'Virtual', 'Phone', 'Conference'];
const sentiments = ['Positive', 'Neutral', 'Negative'];

export default function InteractionForm() {
  const dispatch = useDispatch();
  const doctors = useSelector((state) => state.doctors.items);
  const { form, saving, handleFieldChange, handleSave, handleReset } = useInteractions();
  useEffect(() => { if (!doctors.length) dispatch(fetchDoctors()); }, [dispatch, doctors.length]);
  const field = (name) => ({
    value: form[name] || '',
    onChange: (event) => handleFieldChange(name, event.target.value),
  });
  return (
    <Card>
      <CardHeader title="Traditional Form" subheader="Required fields are marked with an asterisk"
        action={form.entry_source === 'ai_assisted' && (
          <Chip icon={<AutoAwesome />} label="AI populated" color="primary" size="small" />
        )} />
      <Divider />
      <CardContent>
        <Grid container spacing={2.25}>
          <Grid item xs={12}>
            <Autocomplete freeSolo options={doctors} getOptionLabel={(option) =>
              typeof option === 'string' ? option : option.name}
              value={doctors.find((d) => d.id === form.doctor_id) || form.doctor_name || null}
              onChange={(_, value) => {
                handleFieldChange('doctor_id', typeof value === 'object' ? value?.id || null : null);
                handleFieldChange('doctor_name', typeof value === 'object' ? value?.name || '' : value || '');
              }}
              onInputChange={(_, value, reason) => {
                if (reason === 'input') { handleFieldChange('doctor_id', null); handleFieldChange('doctor_name', value); }
              }}
              renderInput={(params) => <TextField {...params} required label="Doctor Name"
                placeholder="Search or enter an HCP" />} />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField select fullWidth required label="Interaction Type" {...field('interaction_type')}>
              {interactionTypes.map((item) => <MenuItem key={item} value={item}>{item}</MenuItem>)}
            </TextField>
          </Grid>
          <Grid item xs={12} sm={3}>
            <TextField fullWidth required type="date" label="Date" InputLabelProps={{ shrink: true }} {...field('date')} />
          </Grid>
          <Grid item xs={12} sm={3}>
            <TextField fullWidth type="time" label="Time" InputLabelProps={{ shrink: true }} {...field('time')} />
          </Grid>
          <Grid item xs={12}>
            <TextField fullWidth label="Attendees" placeholder="Names and roles of attendees" {...field('attendees')} />
          </Grid>
          <Grid item xs={12}>
            <TextField fullWidth multiline minRows={2} label="Topics Discussed"
              placeholder="Products, evidence, treatment needs…" {...field('topics')} />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField fullWidth multiline minRows={2} label="Materials Shared"
              placeholder="Brochures, studies, digital assets…" {...field('materials')} />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField fullWidth multiline minRows={2} label="Samples Distributed"
              placeholder="Product and quantity" {...field('samples')} />
          </Grid>
          <Grid item xs={12} sm={5}>
            <TextField select fullWidth label="Sentiment" {...field('sentiment')}>
              {sentiments.map((item) => <MenuItem key={item} value={item}>{item}</MenuItem>)}
            </TextField>
          </Grid>
          <Grid item xs={12}>
            <TextField fullWidth multiline minRows={2} label="Outcome"
              placeholder="Interest, objections, agreements…" {...field('outcomes')} />
          </Grid>
          <Grid item xs={12}>
            <TextField fullWidth multiline minRows={2} label="Follow-up"
              placeholder="Next action, owner, and timing" {...field('followup')} />
          </Grid>
          <Grid item xs={12}>
            <TextField fullWidth required multiline minRows={3} label="Interaction Summary"
              placeholder="Concise, factual summary of the interaction" {...field('summary')} />
          </Grid>
        </Grid>
        <Divider sx={{ my: 3 }} />
        <Stack direction={{ xs: 'column-reverse', sm: 'row' }} justifyContent="space-between" gap={1.5}>
          <Button color="inherit" startIcon={<RestartAlt />} onClick={handleReset}>Reset form</Button>
          <Box>
            <Typography variant="caption" color="text.secondary" mr={2}
              sx={{ display: { xs: 'none', md: 'inline' } }}>Review all AI-populated fields before saving.</Typography>
            <Button variant="contained" startIcon={<SaveOutlined />} onClick={handleSave} disabled={saving}>
              {saving ? 'Saving…' : 'Save interaction'}
            </Button>
          </Box>
        </Stack>
      </CardContent>
    </Card>
  );
}
