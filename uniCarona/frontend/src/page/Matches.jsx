import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { buscarMatches } from "../services/api";
import "./Matches.css";

export default function Matches() {
  const { rotaId } = useParams();
  const navigate = useNavigate();

  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modalAberto, setModalAberto] = useState(false);
  const [usuarioSelecionado, setUsuarioSelecionado] = useState(null);
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

  const formatarRota = (origem, destino) => {
    if (!origem && !destino) return null;
    const o = origem || "Origem não informada";
    const d = destino || "Destino não informado";
    return `${o} → ${d}`;
  };

  const formatarHorario = (horario) => {
    if (!horario) return null;
    return horario;
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
          <button onClick={() => navigate("/rota")}>Tentar novamente</button>
        </div>
      )}

      {!loading && matches.length > 0 && (
        <div className="lista">
          {matches.map((m) => {
            const rota = formatarRota(m.origem, m.destino);
            const horario = formatarHorario(m.horario);
            const temDetalhes = rota || horario;

            return (
              <div className="card" key={m.rota_id}>
                <div className="card-header">
                  <h2>{m.nome_usuario}</h2>
                  <div className={`score ${getCorScore(m.score_ia)}`}>
                    {m.score_ia}%
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

                {temDetalhes ? (
                  <div className="detalhes">
                    <div>
                      <span>Rota</span>
                      <p>{m.origem} → {m.destino}</p>
                    </div>
                    <div>
                      <span>Horário</span>
                      <p>{m.horario}</p>
                    </div>
                  </div>
                ) : (
                  <div className="detalhes-ausentes">
                    <span>Detalhes da rota não disponíveis</span>
                  </div>
                )}

                <button
                  className="btn"
                  onClick={() => {
                    setUsuarioSelecionado(m.nome_usuario);
                    setModalAberto(true);
                  }}
                >
                  Solicitar carona
                </button>
              </div>
            );
          })}
        </div>
      )}
      {modalAberto && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>Solicitação enviada</h2>
            <p>
              Sua solicitação de carona para <strong>{usuarioSelecionado}</strong> foi enviada! Vocês foram conectados e entraram em contato em breve!
            </p>

            <button onClick={() => setModalAberto(false)}>
              Fechar
            </button>
          </div>
        </div>
      )}
    </div>
  );
}