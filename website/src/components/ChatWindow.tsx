import React, { useState } from "react"
import axios from "axios"
import ChatMessage from "./ChatMessage"
import Message from "../TS/types"

const ChatWindow: React.FC<{
  setIsWaiting: (waiting: boolean) => void
  setStatus: (status: string | null) => void
}> = ({ setIsWaiting, setStatus }) => {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [localIsWaiting, setLocalIsWaiting] = useState(false)

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim() !== "") {
      const newMessageId = Date.now()
      const userMessage: Message = {
        id: newMessageId,
        text: input,
        sender: "user",
      }
      setMessages((prevMessages) => [...prevMessages, userMessage])
      setInput("")
      setLocalIsWaiting(true)
      setIsWaiting(true)
      setStatus("Processing...")

      try {
        const response = await axios.post("http://127.0.0.1:5000/api/data", {
          text: input,
        })

        const { generated, grading_score, hellucination_score } = response.data
        const botMessageId = newMessageId + 1

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
        setLocalIsWaiting(false)
        setIsWaiting(false)
        setStatus(null)
      }
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value)
  }

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
          disabled={localIsWaiting}
        />
        <button
          type="submit"
          className="px-6 py-3 bg-yellow-500 text-white rounded hover:bg-yellow-700"
          style={{ height: "70px" }}
          disabled={localIsWaiting}
        >
          Send
        </button>
      </form>
    </div>
  )
}

export default ChatWindow
