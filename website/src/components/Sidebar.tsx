import { useState } from "react"
const Sidebar = () => {
  const [threads, setThreads] = useState(["Thread 1", "Thread 2"])
  const [newThreadName, setNewThreadName] = useState("")

  const handleAddThread = () => {
    if (newThreadName.trim() !== "") {
      setThreads([...threads, newThreadName])
      setNewThreadName("")
    }
  }

  return (
    <aside className="w-64 bg-gray-800 text-white flex flex-col p-4">
      <h2 className="text-2xl font-bold mb-4">Threads</h2>
      <ul>
        {threads.map((thread, index) => (
          <li
            key={index}
            className="mb-2"
          >
            <a
              href="#"
              className="hover:underline"
            >
              {thread}
            </a>
          </li>
        ))}
        <li className="mt-4">
          <input
            type="text"
            value={newThreadName}
            onChange={(e) => setNewThreadName(e.target.value)}
            placeholder="New thread name"
            className="w-full p-2 rounded mb-2 text-gray-700"
          />
          <button
            onClick={handleAddThread}
            className="bg-blue-500 text-white font-bold py-2 px-4 rounded w-full"
          >
            + Add Thread
          </button>
        </li>
      </ul>
    </aside>
  )
}

export default Sidebar
