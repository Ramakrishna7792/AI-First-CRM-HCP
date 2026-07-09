import { alpha, createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: { main: '#0B5CAB', light: '#EAF5FE', dark: '#063E73' },
    secondary: { main: '#0176D3' },
    success: { main: '#2E844A', light: '#E8F5EC' },
    warning: { main: '#DD7A01', light: '#FFF4E5' },
    error: { main: '#BA0517' },
    background: { default: '#F3F5F7', paper: '#FFFFFF' },
    text: { primary: '#181818', secondary: '#5C5C5C' },
    divider: '#E5E7EB',
  },
  typography: {
    fontFamily: '"Inter", system-ui, -apple-system, sans-serif',
    h4: { fontWeight: 700, letterSpacing: '-0.025em' },
    h5: { fontWeight: 700 }, h6: { fontWeight: 700 },
    subtitle1: { fontWeight: 600 }, button: { textTransform: 'none', fontWeight: 600 },
  },
  shape: { borderRadius: 10 },
  components: {
    MuiCssBaseline: { styleOverrides: { body: { minWidth: 320 }, '*': { boxSizing: 'border-box' } } },
    MuiCard: { styleOverrides: { root: {
      border: '1px solid #E5E7EB', boxShadow: '0 1px 3px rgba(24,24,24,.08)',
    } } },
    MuiButton: { defaultProps: { disableElevation: true },
      styleOverrides: { root: { borderRadius: 6, minHeight: 40 } } },
    MuiTextField: { defaultProps: { size: 'small' } },
    MuiOutlinedInput: { styleOverrides: { root: {
      borderRadius: 6, '&.Mui-focused': { boxShadow: `0 0 0 3px ${alpha('#0176D3', .12)}` },
    } } },
  },
});
export default theme;
