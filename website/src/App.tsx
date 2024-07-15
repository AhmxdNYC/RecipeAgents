import "./index.css"
import UserInput from "./components/UserInput"

function App() {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center">
      <h1 className="text-4xl font-bold text-yellow-500 mb-8">Recipe Agents</h1>
      <div className="card">
        <UserInput />
      </div>
      <p className="text-center text-gray-600 mt-4">
        Enter your dietary preferences and available ingredients to get
        personalized recipes by our 5 agent team.
      </p>
    </div>
  )
}

export default App
