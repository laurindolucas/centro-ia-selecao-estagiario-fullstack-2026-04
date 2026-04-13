import { BrowserRouter, Routes, Route } from "react-router-dom";

import Splash from "./page/Splash";
import Cadastro from "./page/Cadastro";


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Splash />} />
        <Route path="/cadastro" element={<Cadastro />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;