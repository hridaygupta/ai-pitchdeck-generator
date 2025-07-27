import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { startupAPI } from '../../services/api';

interface Startup {
  id: string;
  name: string;
  tagline?: string;
  description?: string;
  website?: string;
  industry: string;
  funding_stage: string;
  revenue_model: string;
  problem_statement?: string;
  solution_description?: string;
  unique_value_proposition?: string;
  target_market?: string;
  team_size?: number;
  customer_count?: number;
  current_revenue?: number;
  funding_ask?: number;
  created_at: string;
  updated_at: string;
}

interface StartupState {
  startups: Startup[];
  currentStartup: Startup | null;
  isLoading: boolean;
  error: string | null;
}

const initialState: StartupState = {
  startups: [],
  currentStartup: null,
  isLoading: false,
  error: null,
};

// Async thunks
export const createStartup = createAsyncThunk(
  'startup/create',
  async (startupData: Partial<Startup>, { rejectWithValue }) => {
    try {
      const response = await startupAPI.create(startupData);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to create startup');
    }
  }
);

export const fetchStartups = createAsyncThunk(
  'startup/fetchAll',
  async (_, { rejectWithValue }) => {
    try {
      const response = await startupAPI.getAll();
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch startups');
    }
  }
);

export const fetchStartupById = createAsyncThunk(
  'startup/fetchById',
  async (id: string, { rejectWithValue }) => {
    try {
      const response = await startupAPI.getById(id);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch startup');
    }
  }
);

export const updateStartup = createAsyncThunk(
  'startup/update',
  async ({ id, startupData }: { id: string; startupData: Partial<Startup> }, { rejectWithValue }) => {
    try {
      const response = await startupAPI.update(id, startupData);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to update startup');
    }
  }
);

const startupSlice = createSlice({
  name: 'startup',
  initialState,
  reducers: {
    setCurrentStartup: (state, action: PayloadAction<Startup | null>) => {
      state.currentStartup = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Create startup
      .addCase(createStartup.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(createStartup.fulfilled, (state, action) => {
        state.isLoading = false;
        state.startups.push(action.payload.startup);
        state.currentStartup = action.payload.startup;
      })
      .addCase(createStartup.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      
      // Fetch all startups
      .addCase(fetchStartups.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchStartups.fulfilled, (state, action) => {
        state.isLoading = false;
        state.startups = action.payload;
      })
      .addCase(fetchStartups.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      
      // Fetch startup by ID
      .addCase(fetchStartupById.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchStartupById.fulfilled, (state, action) => {
        state.isLoading = false;
        state.currentStartup = action.payload;
      })
      .addCase(fetchStartupById.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      
      // Update startup
      .addCase(updateStartup.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(updateStartup.fulfilled, (state, action) => {
        state.isLoading = false;
        const updatedStartup = action.payload;
        
        // Update in startups array
        const index = state.startups.findIndex(s => s.id === updatedStartup.id);
        if (index !== -1) {
          state.startups[index] = updatedStartup;
        }
        
        // Update current startup if it's the same one
        if (state.currentStartup?.id === updatedStartup.id) {
          state.currentStartup = updatedStartup;
        }
      })
      .addCase(updateStartup.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const {
  setCurrentStartup,
  clearError,
} = startupSlice.actions;

export default startupSlice.reducer; 