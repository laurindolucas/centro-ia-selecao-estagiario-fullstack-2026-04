import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Cadastro.css";
import logo from "../assets/uniCaronaLogo.png";
import { BiCar } from "react-icons/bi";
import { BiUser } from "react-icons/bi";
export default function Cadastro() {
  const navigate = useNavigate();

  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [descricao, setDescricao] = useState("");
  const [senha, setSenha] = useState("");
  const [tipo, setTipo] = useState("");

const handleSubmit = async () => {
  if (!nome || !email || !senha || !tipo) {
    alert("Preencha todos os campos obrigatórios");
    return;
  }

  try {
    const res = await fetch("http://127.0.0.1:8000/users", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        nome,
        email,
        descricao,
        senha,
        tipo
      })
    });

    const data = await res.json();

    console.log("Resposta API:", data);

    if (!res.ok) {
      alert("Erro ao cadastrar usuário");
      return;
    }

    localStorage.setItem("user_id", data.id);

    navigate("/Story");

  } catch (error) {
    console.error(error);
    alert("Erro ao conectar com o servidor");
  }
};

  return (
    <div className="container">
      <img src={logo} alt="Logo UniCarona" className="splash-logo-cadastro" />
    
      <p className="subtitulo">
        Conectando universitários na mesma rota
      </p>

      <div className="card">
        <label>Seu nome</label>
        <input
          type="text"
          placeholder="Digite seu nome"
          value={nome}
          onChange={(e) => setNome(e.target.value)}
        />

        <label>Email</label>
        <input
          type="email"
          placeholder="Digite seu email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <label>Descrição (bio)</label>
        <input
          type="text"
          placeholder="Fale um pouco sobre você"
          value={descricao}
          onChange={(e) => setDescricao(e.target.value)}
        />

        <label>Senha</label>
        <input
          type="password"
          placeholder="Digite sua senha"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
        />

        <label>Você é</label>

        <div className="tipo-container">
          <div
            className={`tipo-card ${tipo === "motorista" ? "ativo" : ""}`}
            onClick={() => setTipo("motorista")}
          >
            <BiCar />
            <p>Motorista</p>
          </div>

          <div
            className={`tipo-card ${tipo === "passageiro" ? "ativo" : ""}`}
            onClick={() => setTipo("passageiro")}
          >
            <BiUser />
            <p>Passageiro</p>
          </div>
        </div>

        <button onClick={handleSubmit}>
          Continuar
        </button>
      </div>
    </div>
  );
}