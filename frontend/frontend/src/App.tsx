import { useState } from "react";
import { Routes, Route, Link } from "react-router-dom";
import { Test } from "./pages/test";
import "./App.css";
import Login from "./pages/login";
import Dash from "./pages/dash";

function App() {
  const [count, setCount] = useState(0);

  return (
    <Routes>
      <Route path="test" element={<Test />}></Route>
      <Route path="login" element={<Login />}></Route>
      <Route path="dash" element={<Dash />}></Route>
    </Routes>
  );
}

export default App;
