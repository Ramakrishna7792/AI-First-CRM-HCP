import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { interactionApi } from '../services/api';

export const fetchInteractions = createAsyncThunk('interactions/fetchAll', async (_, { rejectWithValue }) => {
  try { return (await interactionApi.getAll()).data; }
  catch (error) { return rejectWithValue(error.response?.data?.detail || 'Could not load interactions'); }
});
export const createInteraction = createAsyncThunk('interactions/create', async (data, { rejectWithValue }) => {
  try { return (await interactionApi.create(data)).data; }
  catch (error) { return rejectWithValue(error.response?.data?.detail || 'Could not save interaction'); }
});

const freshForm = () => ({
  doctor_id: null, doctor_name: '', interaction_type: 'In-Person',
  date: new Date().toISOString().slice(0, 10), time: '', attendees: '', topics: '',
  materials: '', samples: '', sentiment: 'Neutral', outcomes: '', followup: '',
  summary: '', entry_source: 'form',
});
const interactionSlice = createSlice({
  name: 'interactions',
  initialState: { items: [], form: freshForm(), loading: false, saving: false, error: null },
  reducers: {
    updateFormField(state, action) {
      state.form[action.payload.field] = action.payload.value;
      if (action.payload.field !== 'entry_source') state.form.entry_source ||= 'form';
    },
    autoFillForm(state, action) {
      Object.entries(action.payload).forEach(([key, value]) => {
        if (key in state.form && value !== null && value !== undefined && value !== '') state.form[key] = value;
      });
      state.form.entry_source = 'ai_assisted';
    },
    resetForm(state) { state.form = freshForm(); },
    clearInteractionError(state) { state.error = null; },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchInteractions.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchInteractions.fulfilled, (state, action) => { state.loading = false; state.items = action.payload; })
      .addCase(fetchInteractions.rejected, (state, action) => { state.loading = false; state.error = action.payload; })
      .addCase(createInteraction.pending, (state) => { state.saving = true; state.error = null; })
      .addCase(createInteraction.fulfilled, (state, action) => {
        state.saving = false; state.items.unshift(action.payload); state.form = freshForm();
      })
      .addCase(createInteraction.rejected, (state, action) => { state.saving = false; state.error = action.payload; });
  },
});
export const { updateFormField, autoFillForm, resetForm, clearInteractionError } = interactionSlice.actions;
export default interactionSlice.reducer;
