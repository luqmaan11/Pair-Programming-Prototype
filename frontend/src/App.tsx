import { useEffect } from 'react'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { Provider } from 'react-redux'
import { store } from './state/store.ts'
import { Lobby } from './pages/Lobby.tsx'
import { Room } from './pages/Room.tsx'

const router = createBrowserRouter([
  { path: '/', element: <Lobby /> },
  { path: '/room/:roomId', element: <Room /> },
])

export default function App() {
  useEffect(() => {
    document.title = 'Pair Prototype'
  }, [])
  return (
    <Provider store={store}>
      <RouterProvider router={router} />
    </Provider>
  )
}
