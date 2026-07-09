import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { authApi } from '../services/api';

const savedUser = JSON.parse(localStorage.getItem('user') || 'null');

export const login = createAsyncThunk('auth/login', async (credentials, { rejectWithValue }) => {
  try {
    const { data } = await authApi.login(credentials);
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('user', JSON.stringify(data.user));
    return data;
  } catch (error) {
    return rejectWithValue(error.response?.data?.detail || 'Unable to sign in');
  }
});
export const register = createAsyncThunk('auth/register', async (details, { dispatch, rejectWithValue }) => {
  try {
    await authApi.register(details);
    return dispatch(login({ email: details.email, password: details.password })).unwrap();
  } catch (error) {
    return rejectWithValue(error.response?.data?.detail || 'Unable to create account');
  }
});

const authSlice = createSlice({
  name: 'auth',
  initialState: { user: savedUser, loading: false, error: null },
  reducers: {
    logout(state) {
      localStorage.removeItem('access_token'); localStorage.removeItem('user'); state.user = null;
    },
    clearAuthError(state) { state.error = null; },
  },
  extraReducers: (builder) => {
    builder
      .addMatcher((a) => [login.pending.type, register.pending.type].includes(a.type), (state) => {
        state.loading = true; state.error = null;
      })
      .addMatcher((a) => [login.fulfilled.type, register.fulfilled.type].includes(a.type), (state, action) => {
        state.loading = false; state.user = action.payload.user;
      })
      .addMatcher((a) => [login.rejected.type, register.rejected.type].includes(a.type), (state, action) => {
        state.loading = false; state.error = action.payload || 'Authentication failed';
      });
  },
});
export const { logout, clearAuthError } = authSlice.actions;
export default authSlice.reducer;
