import { useCallback, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { createInteraction, fetchInteractions, resetForm, updateFormField } from '../store/interactionSlice';
import { showSnackbar } from '../store/uiSlice';

export function useInteractions({ load = false } = {}) {
  const dispatch = useDispatch();
  const state = useSelector((store) => store.interactions);
  useEffect(() => { if (load) dispatch(fetchInteractions()); }, [dispatch, load]);
  const handleFieldChange = useCallback((field, value) => dispatch(updateFormField({ field, value })), [dispatch]);
  const handleSave = useCallback(async () => {
    if (!state.form.doctor_name?.trim() || !state.form.date || !state.form.summary?.trim()) {
      dispatch(showSnackbar({ message: 'Doctor, date, and summary are required', severity: 'error' }));
      return false;
    }
    const payload = { ...state.form };
    if (!payload.doctor_id) delete payload.doctor_id;
    if (!payload.time) delete payload.time;
    const result = await dispatch(createInteraction(payload));
    if (createInteraction.fulfilled.match(result)) {
      dispatch(showSnackbar({ message: 'Interaction saved successfully', severity: 'success' }));
      return true;
    }
    dispatch(showSnackbar({ message: result.payload || 'Could not save interaction', severity: 'error' }));
    return false;
  }, [dispatch, state.form]);
  return {
    interactions: state.items, form: state.form, loading: state.loading,
    saving: state.saving, error: state.error, handleFieldChange, handleSave,
    handleReset: () => dispatch(resetForm()), refresh: () => dispatch(fetchInteractions()),
  };
}
export default useInteractions;
