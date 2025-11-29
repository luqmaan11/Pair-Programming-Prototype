import { createSlice } from '@reduxjs/toolkit'
import type { PayloadAction } from '@reduxjs/toolkit'

export type EditorState = {
  roomId: string
  text: string
  cursor: number
  suggestion: string
  status: 'idle' | 'connecting' | 'connected'
}

const initialState: EditorState = {
  roomId: '',
  text: '',
  cursor: 0,
  suggestion: '',
  status: 'idle',
}

const editorSlice = createSlice({
  name: 'editor',
  initialState,
  reducers: {
    enterRoom(state, action: PayloadAction<string>) {
      state.roomId = action.payload
      state.status = 'connecting'
    },
    updateText(state, action: PayloadAction<{ text: string; cursor: number }>) {
      state.text = action.payload.text
      state.cursor = action.payload.cursor
    },
    setSuggestion(state, action: PayloadAction<string>) {
      state.suggestion = action.payload
    },
    connectionReady(state) {
      state.status = 'connected'
    },
    resetState() {
      return initialState
    },
  },
})

export const { enterRoom, updateText, setSuggestion, connectionReady, resetState } = editorSlice.actions
export default editorSlice.reducer
