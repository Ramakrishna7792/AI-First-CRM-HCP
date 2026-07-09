import { AppBar, Toolbar, IconButton, Typography, Box, Avatar, Chip, Button } from '@mui/material';
import { Menu as MenuIcon, SmartToy as AIIcon, Logout } from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { logout } from '../../store/authSlice';
import { DRAWER_WIDTH } from './Sidebar';

export default function Header({ sidebarOpen, onToggleSidebar }) {
  const dispatch = useDispatch();
  const user = useSelector((state) => state.auth.user);
  return (
    <AppBar position="fixed" elevation={0} sx={{
      width: sidebarOpen ? `calc(100% - ${DRAWER_WIDTH}px)` : '100%',
      ml: sidebarOpen ? `${DRAWER_WIDTH}px` : 0, bgcolor: 'background.paper',
      borderBottom: '1px solid #E8ECF0', color: 'text.primary',
    }}>
      <Toolbar>
        <IconButton edge="start" onClick={onToggleSidebar} sx={{ mr: 2 }}><MenuIcon /></IconButton>
        <Typography variant="h6" fontWeight={600} sx={{ flexGrow: 1 }}>HCP CRM</Typography>
        <Box display="flex" alignItems="center" gap={1.5}>
          <Chip icon={<AIIcon />} label="AI assisted" size="small" color="primary" variant="outlined" />
          <Avatar sx={{ bgcolor: 'primary.main' }}>{user?.full_name?.[0] || 'M'}</Avatar>
          <Button size="small" startIcon={<Logout />} onClick={() => dispatch(logout())}>Sign out</Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
}
