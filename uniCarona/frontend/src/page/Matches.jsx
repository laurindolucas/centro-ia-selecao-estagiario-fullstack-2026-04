import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { buscarMatches } from "../services/api";
import "./Matches.css";

export default function Matches() {
  const { rotaId } = useParams();
  const navigate = useNavigate();

  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    carregarMatches();
  }, []);

  const carregarMatches = async () => {
    try {
      const data = await buscarMatches(rotaId);
      setMatches(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const getCorScore = (score) => {
    if (score >= 70) return "score-alto";
    if (score >= 40) return "score-medio";
    return "score-baixo";
  };

  const getTextoCompatibilidade = (classificacao) => {
    if (classificacao === "alta") return "Boa compatibilidade";
    if (classificacao === "média") return "Compatibilidade moderada";
    return "Baixa compatibilidade";
  };

  return (
    <div className="matches-container">
      <div className="topo">
        <button onClick={() => navigate("/rota")}>← Nova busca</button>
        <h1>Caronas encontradas</h1>
      </div>

      {loading && <p className="mensagem">Buscando caronas...</p>}

      {!loading && matches.length === 0 && (
        <div className="sem-matches">
          <h2>Nenhuma carona encontrada</h2>
          <p>Tente ajustar o horário ou o local da rota</p>

          <button onClick={() => navigate("/rota")}>
            Tentar novamente
          </button>
        </div>
      )}

      {!loading && matches.length > 0 && (
        <div className="lista">
          {matches.map((m) => (
            <div className="card" key={m.rota_id}>
              
              <div className="card-header">
                <h2>Usuário #{m.usuario_id}</h2>

                <div className={`score ${getCorScore(m.score)}`}>
                  {m.score}%
                </div>
              </div>

              <div className="infos">
                <span>{(m.dist_origem_km * 1000).toFixed(0)}m de você</span>
                <span>{Math.round(m.diferenca_horario_min)} min de diferença</span>
              </div>

              <div className="box-ia">
                <strong>{getTextoCompatibilidade(m.classificacao)}</strong>
                <p>{m.explicacao}</p>
              </div>

              <div className="detalhes">
                <div>
                  <span>Rota</span>
                  <p>Origem → Destino</p>
                </div>

                <div>
                  <span>Horário</span>
                  <p>--:--</p>
                </div>
              </div>

              <button className="btn">Solicitar carona</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}