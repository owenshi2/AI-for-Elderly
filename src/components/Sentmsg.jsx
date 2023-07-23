import { useState } from "react"

const Sentmsg = () => {
  const [value, setValue] = useState("");
  const handleSendMessage = (e) => {
    e.preventDefault();
    console.log(value);
  }
  return (
    <div className="bg-gray-200 fixed bottom-0 w-full py-10 shadow-lg">
      <form onSubmit={handleSendMessage} className="containerWrap flex">
        <input value={value} onChange={e => setValue(e.target.value)} className="input w-full focus:outline-none bg-gray-100 rounded-r-none text-lg" type="text" />
        <button type="submit" className="w-auto bg-gray-500 text-white rounded-r-lg px-5 text-sm">Send</button>
      </form>
    </div>
  )
}

export default Sentmsg