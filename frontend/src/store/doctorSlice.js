import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { doctorApi } from '../services/api';

export const fetchDoctors = createAsyncThunk('doctors/fetchAll', async (search, { rejectWithValue }) => {
  try { return (await doctorApi.getAll(search)).data; }
  catch (error) { return rejectWithValue(error.response?.data?.detail || 'Could not load doctors'); }
});
const doctorSlice = createSlice({
  name: 'doctors',
  initialState: { items: [], loading: false, error: null },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchDoctors.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchDoctors.fulfilled, (state, action) => { state.loading = false; state.items = action.payload; })
      .addCase(fetchDoctors.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});
export default doctorSlice.reducer;
