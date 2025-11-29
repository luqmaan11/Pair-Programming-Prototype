import { useCallback, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { enterRoom, setSuggestion, updateText } from '../state/editorSlice'
import { useAppDispatch, useAppSelector } from '../state/hooks'
import type { RootState } from '../state/store'
import { useCollab } from '../hooks/useCollab'

const AUTOCOMPLETE_DELAY = 600

export function Room() {
  const { roomId = '' } = useParams()
  const navigate = useNavigate()
  const dispatch = useAppDispatch()
  const editor = useAppSelector((state: RootState) => state.editor)
  const { sendUpdate } = useCollab(roomId)
  const timerRef = useRef<number | null>(null)
  const textareaRef = useRef<HTMLTextAreaElement | null>(null)

  useEffect(() => {
    if (!roomId) {
      navigate('/')
      return undefined
    }
    dispatch(enterRoom(roomId))
    return () => {
      if (timerRef.current) {
        window.clearTimeout(timerRef.current)
        timerRef.current = null
      }
    }
  }, [roomId, dispatch, navigate])

  const requestSuggestion = useCallback(
    (value: string, caret: number) => {
      if (timerRef.current) {
        window.clearTimeout(timerRef.current)
      }
      timerRef.current = window.setTimeout(async () => {
        try {
          const response = await fetch('http://localhost:8000/autocomplete', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: value, cursorPosition: caret, language: 'python' }),
          })
          if (!response.ok) {
            throw new Error('failed request')
          }
          const data = await response.json()
          dispatch(setSuggestion(data.suggestion ?? ''))
        } catch (error) {
          dispatch(setSuggestion(''))
          console.error('autocomplete failed', error)
        }
      }, AUTOCOMPLETE_DELAY)
    },
    [dispatch],
  )

  const applyEditorUpdate = useCallback(
    (value: string, caret: number) => {
      dispatch(updateText({ text: value, cursor: caret }))
      sendUpdate(value, caret)
      requestSuggestion(value, caret)
    },
    [dispatch, requestSuggestion, sendUpdate],
  )

  const handleChange = useCallback(
    (event: React.ChangeEvent<HTMLTextAreaElement>) => {
      const value = event.target.value
      const caret = event.target.selectionStart ?? value.length
      applyEditorUpdate(value, caret)
    },
    [applyEditorUpdate],
  )

  const handleKeyDown = useCallback(
    (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
      if (event.key !== 'Tab') {
        return
      }
      event.preventDefault()
      const { selectionStart = 0, selectionEnd = selectionStart, value } = event.currentTarget
      const insertion = '	'
      const nextValue = `${value.slice(0, selectionStart)}${insertion}${value.slice(selectionEnd)}`
      const nextCaret = selectionStart + insertion.length
      applyEditorUpdate(nextValue, nextCaret)
      window.requestAnimationFrame(() => {
        const node = textareaRef.current
        if (node) {
          node.selectionStart = node.selectionEnd = nextCaret
        }
      })
    },
    [applyEditorUpdate],
  )

  return (
    <div className="page">
      <header className="panel">
        <span>Room {roomId}</span>
        <button onClick={() => navigate('/')}>Leave</button>
      </header>
      <textarea
        ref={textareaRef}
        className="editor"
        value={editor.text}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        spellCheck={false}
      />
      {editor.suggestion && (
        <div className="suggestion">
          Suggestion: <code>{editor.suggestion}</code>
        </div>
      )}
    </div>
  )
}
