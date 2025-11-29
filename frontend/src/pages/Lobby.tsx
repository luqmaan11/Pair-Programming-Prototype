import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export function Lobby() {
  const navigate = useNavigate()
  const [roomCode, setRoomCode] = useState('')
  const [notice, setNotice] = useState('')

  const goToRoom = (id: string) => navigate(`/room/${id}`)

  const createRoom = async () => {
    try {
      setNotice('')
      const response = await fetch('http://localhost:8000/rooms', { method: 'POST' })
      if (!response.ok) {
        throw new Error('failed to create room')
      }
      const data = await response.json()
      goToRoom(data.roomId)
    } catch (error) {
      setNotice('Could not create room')
      console.error(error)
    }
  }

  const joinRoom = () => {
    if (!roomCode.trim()) {
      setNotice('Enter a room code')
      return
    }
    setNotice('')
    goToRoom(roomCode.trim())
  }

  return (
    <div className="page">
      <h1>Pair Prototype</h1>
      <div className="panel">
        <button onClick={createRoom}>Create room</button>
      </div>
      <div className="panel">
        <input value={roomCode} onChange={(e) => setRoomCode(e.target.value)} placeholder="Room code" />
        <button onClick={joinRoom}>Join</button>
      </div>
      {notice && <p className="error">{notice}</p>}
    </div>
  )
}
