const API_URL = "http://127.0.0.1:8000";

export async function criarUsuario(data) {
  const res = await fetch(`${API_URL}/users`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });

  return res.json();
}

export async function buscarUsuario(id) {
  const res = await fetch(`${API_URL}/users/${id}`);
  return res.json();
}




export async function criarRota(data) {
  const res = await fetch(`${API_URL}/rotas`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });

  return res.json();
}

export async function buscarRotas() {
  const res = await fetch(`${API_URL}/rotas`);
  return res.json();
}


export async function buscarMatches(rotaId) {
  const res = await fetch(`${API_URL}/matches/${rotaId}`);
  return res.json();
}