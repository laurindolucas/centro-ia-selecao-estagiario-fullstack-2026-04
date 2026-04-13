import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { criarRota } from "../services/api";
import "./Rota.css";

export default function Rota() {
  const navigate = useNavigate();

  const [origem, setOrigem] = useState("");
  const [destino, setDestino] = useState("");
  const [horario, setHorario] = useState("");

  const handleSubmit = async () => {
    const user_id = localStorage.getItem("user_id");

    if (!origem || !destino || !horario) {
      alert("Preencha todos os campos");
      return;
    }

    const data = await criarRota({
      usuario_id: Number(user_id),
      origem,
      destino,
      horario
    });

    navigate(`/matches/${data.id}`);
  };

  return (
    <div className="rota-container">
      <div className="rota-card">
        <h1>Buscar carona</h1>

        <label>Origem</label>
        <input
          type="text"
          placeholder="Ex: Casa Amarela"
          value={origem}
          onChange={(e) => setOrigem(e.target.value)}
        />

        <label>Destino</label>
        <input
          type="text"
          placeholder="Ex: UNICAP"
          value={destino}
          onChange={(e) => setDestino(e.target.value)}
        />

        <label>Horário</label>
        <input
          type="time"
          value={horario}
          onChange={(e) => setHorario(e.target.value)}
        />

        <button onClick={handleSubmit}>
          Buscar caronas
        </button>
      </div>
    </div>
  );
}