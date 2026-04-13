import { BrowserRouter, Routes, Route } from "react-router-dom";

import Splash from "./page/Splash";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Splash />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;