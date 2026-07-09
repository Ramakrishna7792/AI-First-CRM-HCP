import { createSlice } from '@reduxjs/toolkit';

const uiSlice = createSlice({
  name: 'ui',
  initialState: {
    sidebarOpen: true,
    snackbar: { open: false, message: '', severity: 'success' },
    activeTab: 0,
    complianceDialogOpen: false,
    summaryDialogOpen: false,
    followupDialogOpen: false,
  },
  reducers: {
    toggleSidebar: (state) => {
      state.sidebarOpen = !state.sidebarOpen;
    },
    setSidebarOpen: (state, action) => {
      state.sidebarOpen = action.payload;
    },
    showSnackbar: (state, action) => {
      state.snackbar = { open: true, ...action.payload };
    },
    hideSnackbar: (state) => {
      state.snackbar.open = false;
    },
    setActiveTab: (state, action) => {
      state.activeTab = action.payload;
    },
    setComplianceDialogOpen: (state, action) => {
      state.complianceDialogOpen = action.payload;
    },
    setSummaryDialogOpen: (state, action) => {
      state.summaryDialogOpen = action.payload;
    },
    setFollowupDialogOpen: (state, action) => {
      state.followupDialogOpen = action.payload;
    },
  },
});

export const {
  toggleSidebar,
  setSidebarOpen,
  showSnackbar,
  hideSnackbar,
  setActiveTab,
  setComplianceDialogOpen,
  setSummaryDialogOpen,
  setFollowupDialogOpen,
} = uiSlice.actions;

export default uiSlice.reducer;
