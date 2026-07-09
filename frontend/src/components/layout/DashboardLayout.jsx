import { Box, Snackbar, Alert } from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import Header from './Header';
import Sidebar, { DRAWER_WIDTH } from './Sidebar';
import { toggleSidebar, hideSnackbar } from '../../store/uiSlice';

export default function DashboardLayout({ children }) {
  const dispatch = useDispatch();
  const { sidebarOpen, snackbar } = useSelector((state) => state.ui);

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
      <Sidebar open={sidebarOpen} />
      <Header sidebarOpen={sidebarOpen} onToggleSidebar={() => dispatch(toggleSidebar())} />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          mt: 8,
          width: sidebarOpen ? `calc(100% - ${DRAWER_WIDTH}px)` : '100%',
          transition: 'width 0.2s',
        }}
      >
        {children}
      </Box>
      <Snackbar
        open={snackbar.open}
        autoHideDuration={4000}
        onClose={() => dispatch(hideSnackbar())}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert severity={snackbar.severity} onClose={() => dispatch(hideSnackbar())} variant="filled">
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
}
