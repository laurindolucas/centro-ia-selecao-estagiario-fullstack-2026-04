import { useNavigate } from "react-router-dom";
import "./Story.css";

export default function Story() {
  const navigate = useNavigate();

  return (
    <div className="story-container">
      <div className="story-card">
        <h1>Bem-vindo ao UniCarona</h1>

        <p>
          Encontrar alguém com a mesma rota e se conectar na universidade nunca foi tão fácil.
        </p>

        <div className="steps">
          <div className="step">
            <h3>1. Crie sua rota</h3>
            <p>
              Informe de onde você sai, para onde vai e o horário.
            </p>
          </div>

          <div className="step">
            <h3>2. Nós encontramos matches</h3>
            <p>
              Usamos localização + IA para achar pessoas compatíveis com você.
            </p>
          </div>

          <div className="step">
            <h3>3. Escolha a melhor carona</h3>
            <p>
              Veja distância, horário e uma explicação inteligente da compatibilidade.
            </p>
          </div>
          <div className="step">
            <h3>4. Combine a carona</h3>
            <p>
              Converse com o universitário motorista e combinem a carona!
            </p>
          </div>
        </div>

        <button onClick={() => navigate("/rota")}>
          Começar 
        </button>
      </div>
    </div>
  );
}