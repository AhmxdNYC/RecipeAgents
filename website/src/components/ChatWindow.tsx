import React, { useState } from "react"
import axios from "axios"
import ChatMessage from "./ChatMessage"

type Message = {
  id: number
  text: string
  sender: "user" | "bot"
}

const ChatWindow = () => {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim() !== "") {
      const newMessageId = Date.now()
      // Add the user's message to the state
      setMessages([
        ...messages,
        { id: newMessageId, text: input, sender: "user" },
      ])
      console.log("User input:", input)

      try {
        // Send the user's input to the server
        const response = await axios.post("http://127.0.0.1:5000/api/data", {
          text: input,
        })

        // Log the server response
        console.log("Server response:", response.data)

        // Retrieve the modified text from the server's response
        const { generated, grading_score, hellucination_score } = response.data
        const botMessageId = newMessageId + 1

        // Add the bot's message to the state
        setMessages((prevMessages) => [
          ...prevMessages,
          {
            id: botMessageId,
            text: `${generated}\n\nGrading Score: ${grading_score}\nHellucination Score: ${hellucination_score}`,
            sender: "bot",
          },
        ])
      } catch (error) {
        console.error("Error sending data", error)
      }

      // Clear the input field
      setInput("")
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value)
  }

  return (
    <div className="flex flex-col h-full max-w-6xl mx-auto">
      {" "}
      {/* Adjust the width here */}
      <div className="flex-grow overflow-auto p-6">
        {" "}
        {/* Increased padding */}
        {messages.map((message) => (
          <ChatMessage
            key={message.id}
            message={message}
          />
        ))}
      </div>
      <form
        onSubmit={handleSend}
        className="mt-auto"
      >
        <textarea
          value={input}
          onChange={handleChange}
          placeholder="Type your message here..."
          className="w-full h-32 p-3 border rounded-md resize-none" // Adjusted the height and padding
        />
        <button
          type="submit"
          className="px-6 py-3 bg-blue-500 text-white rounded hover:bg-blue-600 mt-2" // Increased padding and margin
        >
          Send
        </button>
      </form>
    </div>
  )
}

export default ChatWindow
