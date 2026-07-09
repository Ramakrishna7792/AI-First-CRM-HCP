import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  IconButton,
  Tooltip,
} from '@mui/material';
import { Delete as DeleteIcon } from '@mui/icons-material';
import SentimentBadge from '../common/SentimentBadge';

export default function InteractionCard({ interaction, onDelete }) {
  const doctorName = interaction.doctor?.name || `Doctor #${interaction.doctor_id}`;

  return (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="flex-start">
          <Box>
            <Typography variant="subtitle1" fontWeight={600}>
              {doctorName}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {interaction.date} {interaction.time ? `• ${interaction.time}` : ''}
            </Typography>
          </Box>
          <Box display="flex" alignItems="center" gap={1}>
            <SentimentBadge sentiment={interaction.sentiment} />
            {interaction.interaction_type && (
              <Chip label={interaction.interaction_type} size="small" variant="outlined" />
            )}
            {onDelete && (
              <Tooltip title="Delete">
                <IconButton size="small" onClick={() => onDelete(interaction.id)} color="error">
                  <DeleteIcon fontSize="small" />
                </IconButton>
              </Tooltip>
            )}
          </Box>
        </Box>
        {interaction.topics && (
          <Typography variant="body2" mt={1.5}>
            <strong>Topics:</strong> {interaction.topics}
          </Typography>
        )}
        {interaction.outcomes && (
          <Typography variant="body2" mt={0.5} color="text.secondary">
            <strong>Outcome:</strong> {interaction.outcomes}
          </Typography>
        )}
        {interaction.followup && (
          <Typography variant="body2" mt={0.5} color="primary">
            <strong>Follow-up:</strong> {interaction.followup}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
}
