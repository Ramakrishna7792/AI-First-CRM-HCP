import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';
import chatReducer from './chatSlice';
import doctorReducer from './doctorSlice';
import interactionReducer from './interactionSlice';
import uiReducer from './uiSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    chat: chatReducer,
    doctors: doctorReducer,
    interactions: interactionReducer,
    ui: uiReducer,
  },
});
