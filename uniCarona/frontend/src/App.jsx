import { BrowserRouter, Routes, Route } from "react-router-dom";

import Splash from "./page/Splash";
import Cadastro from "./page/Cadastro";
import Story from "./page/Story";
import Rota from "./page/CriarRota"
import Matches from "./page/Matches";


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Splash />} />
        <Route path="/cadastro" element={<Cadastro />} />
        <Route path="/Story" element={<Story/>} />
        <Route path="/Rota" element={<Rota/>} />
        <Route path="/matches/:rotaId" element={<Matches />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;