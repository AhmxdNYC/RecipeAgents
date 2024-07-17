import React, { useState, useEffect } from "react"
import axios from "axios"
import ChatMessage from "./ChatMessage"
import Message from "../TS/types"

const ChatWindow: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isWaiting, setIsWaiting] = useState(false)
  const [status, setStatus] = useState<string | null>(null) // Track the status

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim() !== "") {
      const newMessageId = Date.now()
      // Add the user message to the state
      const userMessage: Message = {
        id: newMessageId,
        text: input,
        sender: "user",
      }
      setMessages((prevMessages) => [...prevMessages, userMessage])
      console.log("User input:", input)
      setInput("")
      setIsWaiting(true)
      setStatus("Processing...")

      try {
        // Send the user input to the server
        const response = await axios.post("http://127.0.0.1:5000/api/data", {
          text: input,
        })

        console.log("Server response:", response.data)

        // Retrieve response from Agent Graph
        const { generated, grading_score, hellucination_score } = response.data
        const botMessageId = newMessageId + 1

        // Add the bot's message to the state
        const botMessage: Message = {
          id: botMessageId,
          text: `${generated}\n\nGrading Score: ${grading_score}%\nHellucination Score: ${Math.round(
            hellucination_score
          )}%`,
          sender: "bot",
        }
        setMessages((prevMessages) => [...prevMessages, botMessage])
      } catch (error) {
        console.error("Error sending data", error)
      } finally {
        setIsWaiting(false) // Reset waiting state
        setStatus(null) // Clear status
      }
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value)
  }

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
    <div
      className="flex flex-col h-full w-[70%] max-w-6xl mx-auto relative"
      style={{ height: "70vh" }}
    >
      <div
        className="flex-grow overflow-auto p-6"
        style={{ maxHeight: "55vh", overflowY: "auto" }}
      >
        {messages.map((message) => (
          <ChatMessage
            key={message.id}
            message={message}
          />
        ))}
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
      <form
        onSubmit={handleSend}
        className="mt-auto flex items-center space-x-2"
      >
        <textarea
          value={input}
          onChange={handleChange}
          placeholder="Type your message here..."
          className="p-3 border rounded-md resize-none w-full"
          style={{ height: "70px", flex: "1" }}
          disabled={isWaiting} // Disable textarea while waiting
        />
        <button
          type="submit"
          className="px-6 py-3 bg-yellow-500 text-white rounded hover:bg-blue-700"
          style={{ height: "70px" }}
          disabled={isWaiting} // Disable button while waiting
        >
          Send
        </button>
      </form>
    </div>
  )
}

export default ChatWindow
