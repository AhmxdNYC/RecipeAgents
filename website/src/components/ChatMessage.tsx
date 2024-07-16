type Message = {
  id: number
  text: string
  sender: "user" | "bot"
}

const ChatMessage = ({ message }: { message: Message }) => {
  const formattedText = message.text.replace(/\n/g, "<br />")

  return (
    <div
      className={`flex ${
        message.sender === "user" ? "justify-end" : "justify-start"
      } mb-4`}
    >
      <div
        className={`${
          message.sender === "user"
            ? "bg-blue-500 text-white"
            : "bg-gray-300 text-gray-700"
        } p-4 rounded-lg max-w-lg`}
        dangerouslySetInnerHTML={{ __html: formattedText }}
      />
    </div>
  )
}

export default ChatMessage
