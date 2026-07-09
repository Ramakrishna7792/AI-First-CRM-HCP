import { useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { addUserMessage, sendChatMessage } from '../store/chatSlice';
import { autoFillForm } from '../store/interactionSlice';
import { showSnackbar } from '../store/uiSlice';

export function useChat() {
  const dispatch = useDispatch();
  const chat = useSelector((state) => state.chat);
  const sendMessage = useCallback(async (message) => {
    if (!message.trim()) return;
    dispatch(addUserMessage(message));
    const result = await dispatch(sendChatMessage(message));
    if (sendChatMessage.fulfilled.match(result)) {
      dispatch(autoFillForm({ ...result.payload.interaction_draft, entry_source: 'ai_assisted' }));
      dispatch(showSnackbar({ message: 'Draft updated—please review before saving', severity: 'info' }));
    }
  }, [dispatch]);
  return { ...chat, sendMessage };
}
export default useChat;
