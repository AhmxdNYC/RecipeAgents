import Sidebar from "./components/Sidebar"
import ChatWindow from "./components/ChatWindow"
import { useEffect, useState } from "react"

const App = () => {
  const [isWaiting, setIsWaiting] = useState(false)
  const [status, setStatus] = useState<string | null>(null)

  useEffect(() => {
    const eventSource = new EventSource("http://127.0.0.1:5000/api/updates")

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setStatus(data.status + "...")
    }

    return () => {
      eventSource.close()
    }
  }, [])

  return (
    <div className="flex h-screen bg-gray-100 relative">
      <Sidebar />
      <main className="flex-1 p-4 flex flex-col">
        <div className="flex flex-col items-center justify-center h-full w-full relative">
          <h1 className="text-4xl font-bold text-yellow-500 mb-8">
            Recipe Agents
          </h1>
          <div className="w-full flex flex-col">
            <ChatWindow
              setIsWaiting={setIsWaiting}
              setStatus={setStatus}
            />
          </div>
          <p className="text-center text-gray-600 mt-4">
            Enter your dietary preferences and available ingredients, goals and
            or any useful information to get personalized 7 day meal plan by our
            5 agent team !!!
          </p>
          <p className="text-center text-gray-600 mt-4">
            Refresh to start a new conversation
          </p>
        </div>
        {isWaiting && (
          <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 z-10">
            <div className="bg-white p-6 rounded shadow-md text-center">
              <div className="flex justify-center mb-4">
                <div className="loader ease-linear rounded-full border-8 border-t-8 border-gray-200 h-10 w-10"></div>
              </div>
              <p>{status}</p>
              <p className="mt-2 text-sm text-gray-500">
                Do not reload the page, or you will lose the conversation.
              </p>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
