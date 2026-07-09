import {
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Box,
  Typography,
  Divider,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  EditNote as LogIcon,
  List as ListIcon,
  LocalHospital as HospitalIcon,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

const DRAWER_WIDTH = 260;

const navItems = [
  { label: 'Dashboard', path: '/', icon: <DashboardIcon /> },
  { label: 'Log Interaction', path: '/log', icon: <LogIcon /> },
  { label: 'Interactions', path: '/interactions', icon: <ListIcon /> },
];

export default function Sidebar({ open }) {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <Drawer
      variant="persistent"
      open={open}
      sx={{
        width: open ? DRAWER_WIDTH : 0,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: DRAWER_WIDTH,
          boxSizing: 'border-box',
          borderRight: '1px solid #E8ECF0',
          bgcolor: '#FFFFFF',
        },
      }}
    >
      <Toolbar sx={{ px: 2 }}>
        <HospitalIcon color="primary" sx={{ mr: 1.5 }} />
        <Box>
          <Typography variant="subtitle1" fontWeight={700} color="primary" lineHeight={1.2}>
            AI-First CRM
          </Typography>
          <Typography variant="caption" color="text.secondary">
            HCP Interaction Module
          </Typography>
        </Box>
      </Toolbar>
      <Divider />
      <List sx={{ px: 1, pt: 2 }}>
        {navItems.map((item) => (
          <ListItemButton
            key={item.path}
            selected={location.pathname === item.path}
            onClick={() => navigate(item.path)}
            sx={{
              borderRadius: 2,
              mb: 0.5,
              '&.Mui-selected': {
                bgcolor: 'primary.main',
                color: 'white',
                '& .MuiListItemIcon-root': { color: 'white' },
                '&:hover': { bgcolor: 'primary.dark' },
              },
            }}
          >
            <ListItemIcon sx={{ minWidth: 40, color: location.pathname === item.path ? 'white' : 'text.secondary' }}>
              {item.icon}
            </ListItemIcon>
            <ListItemText primary={item.label} primaryTypographyProps={{ fontWeight: 500 }} />
          </ListItemButton>
        ))}
      </List>
    </Drawer>
  );
}

export { DRAWER_WIDTH };
