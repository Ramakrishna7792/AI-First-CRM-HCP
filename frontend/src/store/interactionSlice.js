import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { interactionApi } from '../services/api';

export const fetchInteractions = createAsyncThunk(
  'interactions/fetchAll',
  async (params = {}) => {
    const response = await interactionApi.getAll(params);
    return response.data;
  }
);

export const createInteraction = createAsyncThunk(
  'interactions/create',
  async (data) => {
    const response = await interactionApi.create(data);
    return response.data;
  }
);

export const updateInteraction = createAsyncThunk(
  'interactions/update',
  async ({ id, data }) => {
    const response = await interactionApi.update(id, data);
    return response.data;
  }
);

export const deleteInteraction = createAsyncThunk(
  'interactions/delete',
  async (id) => {
    await interactionApi.delete(id);
    return id;
  }
);

const initialFormState = {
  doctor_id: null,
  doctor_name: '',
  interaction_type: 'In-Person',
  date: new Date().toISOString().split('T')[0],
  time: '',
  attendees: '',
  topics: '',
  materials: '',
  samples: '',
  sentiment: 'Neutral',
  outcomes: '',
  followup: '',
  summary: '',
  entry_source: 'form',
};

const interactionSlice = createSlice({
  name: 'interactions',
  initialState: {
    items: [],
    form: { ...initialFormState },
    loading: false,
    saving: false,
    error: null,
    selectedId: null,
  },
  reducers: {
    updateFormField: (state, action) => {
      const { field, value } = action.payload;
      state.form[field] = value;
    },
    setFormData: (state, action) => {
      state.form = { ...state.form, ...action.payload };
    },
    resetForm: (state) => {
      state.form = { ...initialFormState, date: new Date().toISOString().split('T')[0] };
    },
    autoFillForm: (state, action) => {
      const data = action.payload;
      Object.keys(data).forEach((key) => {
        if (data[key] != null && key in state.form) {
          state.form[key] = data[key];
        }
        if (key === 'doctor_name' && data[key]) {
          state.form.doctor_name = data[key];
        }
      });
    },
    setSelectedInteraction: (state, action) => {
      state.selectedId = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchInteractions.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchInteractions.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
      })
      .addCase(fetchInteractions.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      .addCase(createInteraction.pending, (state) => {
        state.saving = true;
        state.error = null;
      })
      .addCase(createInteraction.fulfilled, (state, action) => {
        state.saving = false;
        state.items.unshift(action.payload);
        state.form = { ...initialFormState, date: new Date().toISOString().split('T')[0] };
      })
      .addCase(createInteraction.rejected, (state, action) => {
        state.saving = false;
        state.error = action.error.message;
      })
      .addCase(updateInteraction.fulfilled, (state, action) => {
        const index = state.items.findIndex((i) => i.id === action.payload.id);
        if (index !== -1) state.items[index] = action.payload;
      })
      .addCase(deleteInteraction.fulfilled, (state, action) => {
        state.items = state.items.filter((i) => i.id !== action.payload);
      });
  },
});

export const {
  updateFormField,
  setFormData,
  resetForm,
  autoFillForm,
  setSelectedInteraction,
  clearError,
} = interactionSlice.actions;

export default interactionSlice.reducer;
