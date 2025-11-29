import { useEffect, useRef } from 'react'
import { useDispatch } from 'react-redux'
import type { AppDispatch } from '../state/store'
import { updateText, connectionReady } from '../state/editorSlice'

export function useCollab(roomId: string) {
  const dispatch = useDispatch<AppDispatch>()
  const socketRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    if (!roomId) {
      return
    }
    const socket = new WebSocket(`ws://localhost:8000/ws/${roomId}`)
    socketRef.current = socket
    socket.onopen = () => dispatch(connectionReady())
    socket.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data)
        dispatch(
          updateText({
            text: String(payload.code ?? ''),
            cursor: Number(payload.cursor ?? 0),
          }),
        )
      } catch (error) {
        console.error('invalid payload', error)
      }
    }
    socket.onerror = () => console.warn('socket error')
    socket.onclose = () => console.info('socket closed')
    return () => socket.close()
  }, [roomId, dispatch])

  return {
    sendUpdate: (text: string, cursor: number) => {
      const socket = socketRef.current
      if (!socket || socket.readyState !== WebSocket.OPEN) {
        return
      }
      socket.send(JSON.stringify({ code: text, cursor }))
    },
  }
}
