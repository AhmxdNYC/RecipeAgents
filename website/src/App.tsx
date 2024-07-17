import Sidebar from "./components/Sidebar"
import ChatWindow from "./components/ChatWindow"

const App = () => {
  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar />
      <main className="flex-1 p-4 flex flex-col">
        <div className="flex flex-col items-center justify-center h-full w-full">
          <h1 className="text-4xl font-bold text-yellow-500 mb-8">
            Recipe Agents
          </h1>
          <div className="w-full flex flex-col">
            <ChatWindow />
          </div>
          <p className="text-center text-gray-600 mt-4">
            Enter your dietary preferences and available ingredients, goals and
            or any useful information to get personalized 7 day meal plan by our
            5 agent team !!!
          </p>
        </div>
      </main>
    </div>
  )
}

export default App
