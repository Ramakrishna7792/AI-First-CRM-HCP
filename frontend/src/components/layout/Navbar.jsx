import {
  AppBar, Avatar, Box, Button, Chip, IconButton, Stack, Toolbar, Tooltip, Typography,
} from '@mui/material';
import { Logout, Menu as MenuIcon, NotificationsNone, SmartToy } from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { logout } from '../../store/authSlice';
import { DRAWER_WIDTH } from './Sidebar';

export default function Navbar({ desktopSidebarOpen, onToggleSidebar }) {
  const dispatch = useDispatch();
  const user = useSelector((state) => state.auth.user);
  return (
    <AppBar position="fixed" elevation={0} sx={{
      width: { md: desktopSidebarOpen ? `calc(100% - ${DRAWER_WIDTH}px)` : '100%' },
      ml: { md: desktopSidebarOpen ? `${DRAWER_WIDTH}px` : 0 },
      bgcolor: 'background.paper', color: 'text.primary', borderBottom: 1, borderColor: 'divider',
    }}>
      <Toolbar>
        <IconButton edge="start" onClick={onToggleSidebar} sx={{ mr: 1.5 }}><MenuIcon /></IconButton>
        <Box sx={{ flexGrow: 1 }}>
          <Typography fontWeight={700}>Healthcare Professional CRM</Typography>
          <Typography variant="caption" color="text.secondary" sx={{ display: { xs: 'none', sm: 'block' } }}>
            Field engagement workspace
          </Typography>
        </Box>
        <Stack direction="row" alignItems="center" spacing={1}>
          <Chip icon={<SmartToy />} label="AI ready" color="primary" variant="outlined"
            size="small" sx={{ display: { xs: 'none', sm: 'flex' } }} />
          <Tooltip title="Notifications"><IconButton><NotificationsNone /></IconButton></Tooltip>
          <Avatar sx={{ width: 34, height: 34, bgcolor: 'primary.main', fontSize: 14 }}>
            {user?.full_name?.split(' ').map((part) => part[0]).slice(0, 2).join('') || 'MR'}
          </Avatar>
          <Button color="inherit" startIcon={<Logout />} onClick={() => dispatch(logout())}
            sx={{ display: { xs: 'none', lg: 'flex' } }}>Sign out</Button>
        </Stack>
      </Toolbar>
    </AppBar>
  );
}
