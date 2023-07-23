import Message from "../components/Message";

const Chatbox = () => {
  const messages = [
    {
      id: 1,
      message: "Hello, I am your virtual assistant that can help with scheduling your medication and other important tasks for the week.",
      name: "Assistant"
    },
    {
      id: 2,
      message: "Please say what you need help with scheduling, and I'll figure out how to set the times.",
      name: "Assistant"
    }
  ]
  return (
    <div className="pb-44 pt-20 containerWrap">
      {messages.map(message => (
        <Message key={message.id} message={message} />
      ))}
    </div>
  )
}

export default Chatbox