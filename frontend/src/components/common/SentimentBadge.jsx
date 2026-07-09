import { Chip } from '@mui/material';

const sentimentConfig = {
  Positive: { color: 'success', label: 'Positive' },
  Neutral: { color: 'default', label: 'Neutral' },
  Negative: { color: 'error', label: 'Negative' },
};

export default function SentimentBadge({ sentiment }) {
  const config = sentimentConfig[sentiment] || sentimentConfig.Neutral;
  return <Chip label={config.label} color={config.color} size="small" variant="outlined" />;
}
