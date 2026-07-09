import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { doctorApi } from '../services/api';

export const fetchDoctors = createAsyncThunk('doctors/fetchAll', async (params = {}) => {
  const response = await doctorApi.getAll(params);
  return response.data;
});

const doctorSlice = createSlice({
  name: 'doctors',
  initialState: {
    items: [],
    loading: false,
    error: null,
    selectedDoctor: null,
  },
  reducers: {
    setSelectedDoctor: (state, action) => {
      state.selectedDoctor = action.payload;
    },
    clearSelectedDoctor: (state) => {
      state.selectedDoctor = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchDoctors.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchDoctors.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
      })
      .addCase(fetchDoctors.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

export const { setSelectedDoctor, clearSelectedDoctor } = doctorSlice.actions;
export default doctorSlice.reducer;
