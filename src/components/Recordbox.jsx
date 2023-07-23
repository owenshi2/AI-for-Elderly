
const Recordbox = () => {
  return (
    <div className="bg-gray-200 fixed bottom-10 w-full py-10 shadow-lg">
      <form className="containerWrap flex">
        {/* <input value={value} onChange={e => setValue(e.target.value)} className="input w-full focus:outline-none bg-gray-100 rounded-r-none text-lg" type="text" /> */}
        <button className="btn btn-circle btn-outline">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" /></svg>
        </button>
        <button type="submit" className="w-auto bg-gray-500 text-white rounded-r-lg px-5 text-sm">Send</button>
      </form>
    </div>
  )
}

export default Recordbox