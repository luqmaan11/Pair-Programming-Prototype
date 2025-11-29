import { configureStore } from '@reduxjs/toolkit'
import editorReducer, { type EditorState } from './editorSlice'

export const store = configureStore({
  reducer: {
    editor: editorReducer,
  },
})

export type RootState = {
  editor: EditorState
}
export type AppDispatch = typeof store.dispatch
