import { useEffect, useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  fetchInteractions,
  createInteraction,
  updateFormField,
  resetForm,
} from '../store/interactionSlice';
import { showSnackbar } from '../store/uiSlice';

export function useInteractions() {
  const dispatch = useDispatch();
  const { items, form, loading, saving, error } = useSelector((state) => state.interactions);

  useEffect(() => {
    dispatch(fetchInteractions());
  }, [dispatch]);

  const handleFieldChange = useCallback(
    (field, value) => {
      dispatch(updateFormField({ field, value }));
    },
    [dispatch]
  );

  const handleSave = useCallback(async () => {
    if (!form.doctor_name?.trim()) {
      dispatch(showSnackbar({ message: 'Doctor name is required', severity: 'error' }));
      return;
    }
    const result = await dispatch(createInteraction(form));
    if (createInteraction.fulfilled.match(result)) {
      dispatch(showSnackbar({ message: 'Interaction saved successfully', severity: 'success' }));
      dispatch(fetchInteractions());
    } else {
      dispatch(showSnackbar({ message: 'Failed to save interaction', severity: 'error' }));
    }
  }, [dispatch, form]);

  const handleReset = useCallback(() => {
    dispatch(resetForm());
  }, [dispatch]);

  return {
    interactions: items,
    form,
    loading,
    saving,
    error,
    handleFieldChange,
    handleSave,
    handleReset,
    refresh: () => dispatch(fetchInteractions()),
  };
}

export default useInteractions;
