import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  duration?: number;
}

interface Modal {
  id: string;
  isOpen: boolean;
  props?: any;
}

interface UIState {
  theme: 'light' | 'dark';
  sidebarOpen: boolean;
  notifications: Notification[];
  modals: Modal[];
  loadingStates: Record<string, boolean>;
}

const initialState: UIState = {
  theme: 'light',
  sidebarOpen: true,
  notifications: [],
  modals: [],
  loadingStates: {},
};

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    toggleTheme: (state) => {
      state.theme = state.theme === 'light' ? 'dark' : 'light';
    },
    setTheme: (state, action: PayloadAction<'light' | 'dark'>) => {
      state.theme = action.payload;
    },
    toggleSidebar: (state) => {
      state.sidebarOpen = !state.sidebarOpen;
    },
    setSidebarOpen: (state, action: PayloadAction<boolean>) => {
      state.sidebarOpen = action.payload;
    },
    addNotification: (state, action: PayloadAction<Omit<Notification, 'id'>>) => {
      const id = Date.now().toString();
      state.notifications.push({
        ...action.payload,
        id,
      });
    },
    removeNotification: (state, action: PayloadAction<string>) => {
      state.notifications = state.notifications.filter(
        notification => notification.id !== action.payload
      );
    },
    clearNotifications: (state) => {
      state.notifications = [];
    },
    openModal: (state, action: PayloadAction<{ id: string; props?: any }>) => {
      const existingModal = state.modals.find(modal => modal.id === action.payload.id);
      if (existingModal) {
        existingModal.isOpen = true;
        existingModal.props = action.payload.props;
      } else {
        state.modals.push({
          id: action.payload.id,
          isOpen: true,
          props: action.payload.props,
        });
      }
    },
    closeModal: (state, action: PayloadAction<string>) => {
      const modal = state.modals.find(modal => modal.id === action.payload);
      if (modal) {
        modal.isOpen = false;
      }
    },
    setLoadingState: (state, action: PayloadAction<{ key: string; isLoading: boolean }>) => {
      state.loadingStates[action.payload.key] = action.payload.isLoading;
    },
    clearLoadingState: (state, action: PayloadAction<string>) => {
      delete state.loadingStates[action.payload];
    },
  },
});

export const {
  toggleTheme,
  setTheme,
  toggleSidebar,
  setSidebarOpen,
  addNotification,
  removeNotification,
  clearNotifications,
  openModal,
  closeModal,
  setLoadingState,
  clearLoadingState,
} = uiSlice.actions;

export default uiSlice.reducer; 