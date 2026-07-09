import { Alert, Box, Snackbar, Toolbar, useMediaQuery, useTheme } from '@mui/material';
import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import Navbar from './Navbar';
import Sidebar, { DRAWER_WIDTH } from './Sidebar';
import { hideSnackbar, setSidebarOpen, toggleSidebar } from '../../store/uiSlice';

export default function DashboardLayout({ children }) {
  const dispatch = useDispatch();
  const theme = useTheme();
  const mobile = useMediaQuery(theme.breakpoints.down('md'));
  const { sidebarOpen, snackbar } = useSelector((state) => state.ui);
  useEffect(() => { dispatch(setSidebarOpen(!mobile)); }, [dispatch, mobile]);
  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
      <Sidebar open={sidebarOpen} mobile={mobile} onClose={() => dispatch(setSidebarOpen(false))} />
      <Navbar desktopSidebarOpen={!mobile && sidebarOpen} onToggleSidebar={() => dispatch(toggleSidebar())} />
      <Box component="main" sx={{
        flexGrow: 1, minWidth: 0,
        width: { md: sidebarOpen ? `calc(100% - ${DRAWER_WIDTH}px)` : '100%' },
        transition: theme.transitions.create('width'),
      }}>
        <Toolbar />
        <Box sx={{ p: { xs: 2, sm: 3, xl: 4 }, maxWidth: 1600, mx: 'auto' }}>{children}</Box>
      </Box>
      <Snackbar open={snackbar.open} autoHideDuration={4000}
        onClose={() => dispatch(hideSnackbar())} anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}>
        <Alert severity={snackbar.severity} variant="filled" onClose={() => dispatch(hideSnackbar())}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
}
