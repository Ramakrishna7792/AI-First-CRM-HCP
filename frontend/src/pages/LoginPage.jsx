import { useState } from 'react';
import {
  Alert, Box, Button, Card, CardContent, Container, Link, Stack, TextField, Typography,
} from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import { Navigate } from 'react-router-dom';
import { login, register } from '../store/authSlice';

export default function LoginPage() {
  const dispatch = useDispatch();
  const { user, loading, error } = useSelector((state) => state.auth);
  const [isRegistering, setRegistering] = useState(false);
  const [form, setForm] = useState({ full_name: '', email: '', password: '' });
  if (user) return <Navigate to="/" replace />;

  const submit = (event) => {
    event.preventDefault();
    dispatch(isRegistering ? register(form) : login({ email: form.email, password: form.password }));
  };
  return (
    <Box sx={{ minHeight: '100vh', display: 'grid', placeItems: 'center', bgcolor: 'background.default' }}>
      <Container maxWidth="xs">
        <Card elevation={8}>
          <CardContent sx={{ p: 4 }}>
            <Typography variant="h4" fontWeight={800}>HCP CRM</Typography>
            <Typography color="text.secondary" mb={3}>Secure medical representative workspace</Typography>
            <Stack component="form" spacing={2} onSubmit={submit}>
              {error && <Alert severity="error">{error}</Alert>}
              {isRegistering && (
                <TextField required label="Full name" value={form.full_name}
                  onChange={(e) => setForm({ ...form, full_name: e.target.value })} />
              )}
              <TextField required type="email" label="Email" value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })} />
              <TextField required type="password" label="Password" value={form.password}
                inputProps={{ minLength: 8 }}
                onChange={(e) => setForm({ ...form, password: e.target.value })} />
              <Button type="submit" size="large" variant="contained" disabled={loading}>
                {loading ? 'Please wait…' : isRegistering ? 'Create account' : 'Sign in'}
              </Button>
              <Link component="button" type="button" textAlign="center"
                onClick={() => setRegistering(!isRegistering)}>
                {isRegistering ? 'Already registered? Sign in' : 'New representative? Create account'}
              </Link>
            </Stack>
          </CardContent>
        </Card>
      </Container>
    </Box>
  );
}
