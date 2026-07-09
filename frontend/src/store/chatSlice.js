import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { chatApi } from '../services/api';

export const sendChatMessage = createAsyncThunk('chat/send', async (message, { getState, rejectWithValue }) => {
  try {
    let sessionId = getState().chat.sessionId;
    if (!sessionId) sessionId = (await chatApi.createSession()).data.id;
    return (await chatApi.send(sessionId, message)).data;
  } catch (error) {
    return rejectWithValue(error.response?.data?.detail || 'AI assistant is unavailable');
  }
});
const welcome = {
  id: 'welcome', role: 'assistant',
  content: 'Describe your doctor interaction naturally. I will fill the form for your review.',
};
const chatSlice = createSlice({
  name: 'chat',
  initialState: { sessionId: null, messages: [welcome], loading: false, warnings: [], error: null },
  reducers: {
    addUserMessage(state, action) {
      state.messages.push({ id: crypto.randomUUID(), role: 'user', content: action.payload });
    },
    clearChat(state) {
      state.sessionId = null; state.messages = [welcome]; state.warnings = []; state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendChatMessage.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(sendChatMessage.fulfilled, (state, action) => {
        state.loading = false; state.sessionId = action.payload.session_id;
        state.warnings = action.payload.validation_warnings;
        state.messages.push({ id: crypto.randomUUID(), role: 'assistant', content: action.payload.reply });
      })
      .addCase(sendChatMessage.rejected, (state, action) => {
        state.loading = false; state.error = action.payload;
        state.messages.push({ id: crypto.randomUUID(), role: 'assistant', content: action.payload });
      });
  },
});
export const { addUserMessage, clearChat } = chatSlice.actions;
export default chatSlice.reducer;
