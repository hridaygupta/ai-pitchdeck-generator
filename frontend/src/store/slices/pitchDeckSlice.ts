import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { pitchDeckAPI } from '../../services/api';

interface Slide {
  id: string;
  title: string;
  slide_type: string;
  content: any;
  order: number;
  status: string;
}

interface PitchDeck {
  id: string;
  title: string;
  description: string;
  status: string;
  template: string;
  total_slides: number;
  slides: Slide[];
  created_at: string;
  updated_at: string;
}

interface PitchDeckState {
  pitchDecks: PitchDeck[];
  currentPitchDeck: PitchDeck | null;
  isLoading: boolean;
  error: string | null;
  generationStatus: {
    isGenerating: boolean;
    progress: number;
    estimatedTime: number;
  };
}

const initialState: PitchDeckState = {
  pitchDecks: [],
  currentPitchDeck: null,
  isLoading: false,
  error: null,
  generationStatus: {
    isGenerating: false,
    progress: 0,
    estimatedTime: 0,
  },
};

// Async thunks
export const generatePitchDeck = createAsyncThunk(
  'pitchDeck/generate',
  async (request: any, { rejectWithValue }) => {
    try {
      const response = await pitchDeckAPI.generate(request);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Generation failed');
    }
  }
);

export const getPitchDeckStatus = createAsyncThunk(
  'pitchDeck/getStatus',
  async (pitchDeckId: string, { rejectWithValue }) => {
    try {
      const response = await pitchDeckAPI.getStatus(pitchDeckId);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to get status');
    }
  }
);

export const fetchPitchDecks = createAsyncThunk(
  'pitchDeck/fetchAll',
  async (_, { rejectWithValue }) => {
    try {
      const response = await pitchDeckAPI.getAll();
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch pitch decks');
    }
  }
);

export const fetchPitchDeckById = createAsyncThunk(
  'pitchDeck/fetchById',
  async (id: string, { rejectWithValue }) => {
    try {
      const response = await pitchDeckAPI.getById(id);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch pitch deck');
    }
  }
);

const pitchDeckSlice = createSlice({
  name: 'pitchDeck',
  initialState,
  reducers: {
    setCurrentPitchDeck: (state, action: PayloadAction<PitchDeck | null>) => {
      state.currentPitchDeck = action.payload;
    },
    updateSlide: (state, action: PayloadAction<{ slideId: string; updates: Partial<Slide> }>) => {
      if (state.currentPitchDeck) {
        const slideIndex = state.currentPitchDeck.slides.findIndex(
          slide => slide.id === action.payload.slideId
        );
        if (slideIndex !== -1) {
          state.currentPitchDeck.slides[slideIndex] = {
            ...state.currentPitchDeck.slides[slideIndex],
            ...action.payload.updates,
          };
        }
      }
    },
    reorderSlides: (state, action: PayloadAction<string[]>) => {
      if (state.currentPitchDeck) {
        const newOrder = action.payload;
        const reorderedSlides = newOrder.map((slideId, index) => {
          const slide = state.currentPitchDeck!.slides.find(s => s.id === slideId);
          return slide ? { ...slide, order: index + 1 } : null;
        }).filter(Boolean) as Slide[];
        
        state.currentPitchDeck.slides = reorderedSlides;
      }
    },
    clearError: (state) => {
      state.error = null;
    },
    resetGenerationStatus: (state) => {
      state.generationStatus = {
        isGenerating: false,
        progress: 0,
        estimatedTime: 0,
      };
    },
  },
  extraReducers: (builder) => {
    builder
      // Generate pitch deck
      .addCase(generatePitchDeck.pending, (state) => {
        state.isLoading = true;
        state.error = null;
        state.generationStatus.isGenerating = true;
        state.generationStatus.progress = 0;
      })
      .addCase(generatePitchDeck.fulfilled, (state, action) => {
        state.isLoading = false;
        state.generationStatus.isGenerating = true;
        state.generationStatus.estimatedTime = action.payload.estimated_completion_time || 300;
      })
      .addCase(generatePitchDeck.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
        state.generationStatus.isGenerating = false;
      })
      
      // Get pitch deck status
      .addCase(getPitchDeckStatus.fulfilled, (state, action) => {
        const { status, progress, completed_slides } = action.payload;
        
        if (status === 'completed') {
          state.generationStatus.isGenerating = false;
          state.generationStatus.progress = 100;
          
          // Update current pitch deck with completed slides
          if (state.currentPitchDeck) {
            state.currentPitchDeck.slides = completed_slides;
            state.currentPitchDeck.status = 'completed';
            state.currentPitchDeck.total_slides = completed_slides.length;
          }
        } else {
          state.generationStatus.progress = progress.completed_slides / progress.total_slides * 100;
        }
      })
      
      // Fetch all pitch decks
      .addCase(fetchPitchDecks.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchPitchDecks.fulfilled, (state, action) => {
        state.isLoading = false;
        state.pitchDecks = action.payload;
      })
      .addCase(fetchPitchDecks.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      
      // Fetch pitch deck by ID
      .addCase(fetchPitchDeckById.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchPitchDeckById.fulfilled, (state, action) => {
        state.isLoading = false;
        state.currentPitchDeck = action.payload;
      })
      .addCase(fetchPitchDeckById.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const {
  setCurrentPitchDeck,
  updateSlide,
  reorderSlides,
  clearError,
  resetGenerationStatus,
} = pitchDeckSlice.actions;

export default pitchDeckSlice.reducer; 