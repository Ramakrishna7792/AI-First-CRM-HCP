import {
  Card,
  CardContent,
  CardHeader,
  Grid,
  TextField,
  MenuItem,
  Button,
  Box,
  Divider,
} from '@mui/material';
import { Save as SaveIcon, Refresh as ResetIcon } from '@mui/icons-material';
import useInteractions from '../../hooks/useInteractions';

const INTERACTION_TYPES = ['In-Person', 'Virtual', 'Phone', 'Conference'];
const SENTIMENTS = ['Positive', 'Neutral', 'Negative'];

export default function InteractionForm() {
  const { form, saving, handleFieldChange, handleSave, handleReset } = useInteractions();

  return (
    <Card>
      <CardHeader
        title="Traditional Form"
        subheader="Log HCP interaction manually or review AI-extracted data"
        titleTypographyProps={{ fontWeight: 600 }}
      />
      <Divider />
      <CardContent>
        <Grid container spacing={2.5}>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              required
              label="Doctor Name"
              value={form.doctor_name}
              onChange={(e) => handleFieldChange('doctor_name', e.target.value)}
              placeholder="Dr. Rajesh Sharma"
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              select
              label="Interaction Type"
              value={form.interaction_type}
              onChange={(e) => handleFieldChange('interaction_type', e.target.value)}
            >
              {INTERACTION_TYPES.map((type) => (
                <MenuItem key={type} value={type}>{type}</MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              type="date"
              label="Date"
              value={form.date}
              onChange={(e) => handleFieldChange('date', e.target.value)}
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              type="time"
              label="Time"
              value={form.time}
              onChange={(e) => handleFieldChange('time', e.target.value)}
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Attendees"
              value={form.attendees}
              onChange={(e) => handleFieldChange('attendees', e.target.value)}
              placeholder="Dr. Sharma, Medical Representative"
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              multiline
              rows={2}
              label="Topics Discussed"
              value={form.topics}
              onChange={(e) => handleFieldChange('topics', e.target.value)}
              placeholder="Product efficacy, clinical data, treatment guidelines"
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              multiline
              rows={2}
              label="Materials Shared"
              value={form.materials}
              onChange={(e) => handleFieldChange('materials', e.target.value)}
              placeholder="Brochures, clinical trial data"
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              multiline
              rows={2}
              label="Samples Distributed"
              value={form.samples}
              onChange={(e) => handleFieldChange('samples', e.target.value)}
              placeholder="Product X sample pack (10 units)"
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              select
              label="Observed Sentiment"
              value={form.sentiment}
              onChange={(e) => handleFieldChange('sentiment', e.target.value)}
            >
              {SENTIMENTS.map((s) => (
                <MenuItem key={s} value={s}>{s}</MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              multiline
              rows={2}
              label="Outcomes"
              value={form.outcomes}
              onChange={(e) => handleFieldChange('outcomes', e.target.value)}
              placeholder="Doctor expressed interest in prescribing"
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              multiline
              rows={2}
              label="Follow-up Actions"
              value={form.followup}
              onChange={(e) => handleFieldChange('followup', e.target.value)}
              placeholder="Schedule follow-up next week with RWE data"
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              multiline
              rows={2}
              label="Summary"
              value={form.summary}
              onChange={(e) => handleFieldChange('summary', e.target.value)}
              placeholder="Brief meeting summary"
            />
          </Grid>
        </Grid>
        <Box display="flex" gap={2} mt={3}>
          <Button
            variant="contained"
            startIcon={<SaveIcon />}
            onClick={handleSave}
            disabled={saving}
            size="large"
          >
            {saving ? 'Saving...' : 'Save Interaction'}
          </Button>
          <Button variant="outlined" startIcon={<ResetIcon />} onClick={handleReset}>
            Reset Form
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
}
