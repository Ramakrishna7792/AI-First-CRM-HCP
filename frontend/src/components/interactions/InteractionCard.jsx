import { Box, Card, CardActionArea, CardContent, Chip, Divider, Stack, Typography } from '@mui/material';
import { ArrowForward, CalendarTodayOutlined, PlaceOutlined } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import SentimentBadge from '../common/SentimentBadge';

export default function InteractionCard({ interaction, compact = false }) {
  const navigate = useNavigate();
  const doctorName = interaction.doctor?.name || interaction.doctor_name || `Doctor #${interaction.doctor_id}`;
  return (
    <Card>
      <CardActionArea onClick={() => navigate(`/doctors/${interaction.doctor_id}`)}>
        <CardContent>
          <Stack direction={{ xs: 'column', sm: 'row' }} justifyContent="space-between" gap={1.5}>
            <Box>
              <Typography variant="subtitle1">{doctorName}</Typography>
              <Stack direction="row" spacing={1.5} mt={0.5} color="text.secondary">
                <Stack direction="row" gap={0.5} alignItems="center">
                  <CalendarTodayOutlined sx={{ fontSize: 15 }} />
                  <Typography variant="caption">{interaction.date}{interaction.time ? ` · ${interaction.time.slice(0, 5)}` : ''}</Typography>
                </Stack>
                {interaction.doctor?.hospital && <Stack direction="row" gap={0.5} alignItems="center">
                  <PlaceOutlined sx={{ fontSize: 15 }} /><Typography variant="caption">{interaction.doctor.hospital}</Typography>
                </Stack>}
              </Stack>
            </Box>
            <Stack direction="row" alignItems="center" spacing={1}>
              <SentimentBadge sentiment={interaction.sentiment} />
              <Chip label={interaction.interaction_type} size="small" variant="outlined" />
              <ArrowForward fontSize="small" color="action" />
            </Stack>
          </Stack>
          {!compact && <>
            <Divider sx={{ my: 1.75 }} />
            <Typography variant="body2" color="text.secondary" sx={{
              display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden',
            }}>{interaction.summary || interaction.topics || 'No summary available'}</Typography>
            {interaction.followup && <Typography variant="body2" color="primary.main" fontWeight={600} mt={1}>
              Follow-up: {interaction.followup}
            </Typography>}
          </>}
        </CardContent>
      </CardActionArea>
    </Card>
  );
}
