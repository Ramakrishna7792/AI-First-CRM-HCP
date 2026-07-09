import {
  Box, Divider, Drawer, List, ListItemButton, ListItemIcon, ListItemText, Toolbar, Typography,
} from '@mui/material';
import {
  Dashboard, EditNote, History, LocalHospital, PeopleAltOutlined,
} from '@mui/icons-material';
import { useLocation, useNavigate } from 'react-router-dom';

const DRAWER_WIDTH = 264;
const navItems = [
  { label: 'Dashboard', path: '/', icon: <Dashboard /> },
  { label: 'Log HCP Interaction', path: '/log', icon: <EditNote /> },
  { label: 'Interaction History', path: '/interactions', icon: <History /> },
];

export default function Sidebar({ open, mobile, onClose }) {
  const navigate = useNavigate();
  const location = useLocation();
  const go = (path) => { navigate(path); if (mobile) onClose(); };
  const content = (
    <>
      <Toolbar sx={{ px: 2.5, minHeight: '65px !important' }}>
        <Box sx={{ width: 38, height: 38, bgcolor: 'primary.main', color: 'white', borderRadius: 2,
          display: 'grid', placeItems: 'center', mr: 1.5 }}><LocalHospital /></Box>
        <Box>
          <Typography fontWeight={800} color="primary.main" lineHeight={1.2}>MedConnect</Typography>
          <Typography variant="caption" color="text.secondary">AI-first HCP CRM</Typography>
        </Box>
      </Toolbar>
      <Divider />
      <Box px={2} pt={2.5}>
        <Typography variant="overline" color="text.secondary" fontWeight={700}>Workspace</Typography>
      </Box>
      <List sx={{ px: 1.5, pt: 0.5 }}>
        {navItems.map((item) => {
          const active = item.path === '/' ? location.pathname === '/' : location.pathname.startsWith(item.path);
          return (
            <ListItemButton key={item.path} selected={active} onClick={() => go(item.path)}
              sx={{ borderRadius: 1.5, mb: 0.5, '&.Mui-selected': {
                bgcolor: 'primary.light', color: 'primary.dark',
                '& .MuiListItemIcon-root': { color: 'primary.main' },
              } }}>
              <ListItemIcon sx={{ minWidth: 40 }}>{item.icon}</ListItemIcon>
              <ListItemText primary={item.label} primaryTypographyProps={{ fontSize: 14, fontWeight: 600 }} />
            </ListItemButton>
          );
        })}
      </List>
      <Box sx={{ mt: 'auto', p: 2 }}>
        <Box sx={{ p: 2, bgcolor: 'primary.light', borderRadius: 2 }}>
          <PeopleAltOutlined color="primary" />
          <Typography variant="body2" fontWeight={700} mt={1}>HCP engagement</Typography>
          <Typography variant="caption" color="text.secondary">Capture accurate field insights with AI assistance.</Typography>
        </Box>
      </Box>
    </>
  );
  return (
    <Drawer variant={mobile ? 'temporary' : 'persistent'} open={open} onClose={onClose}
      ModalProps={{ keepMounted: true }} sx={{
        width: open ? DRAWER_WIDTH : 0, flexShrink: 0,
        '& .MuiDrawer-paper': { width: DRAWER_WIDTH, boxSizing: 'border-box', bgcolor: 'background.paper' },
      }}>
      {content}
    </Drawer>
  );
}
export { DRAWER_WIDTH };
