import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import ChatRoom from "./pages/ChatRoom";
import Login from "./pages/Login";
import { PrivateRoute } from "./routes/PrivateRoute";

function App() {

  return (
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/chat" element=
        {
          <PrivateRoute>
            <ChatRoom />
          </PrivateRoute>
        } />
      </Routes>
    </div>
  )
}

export default App
