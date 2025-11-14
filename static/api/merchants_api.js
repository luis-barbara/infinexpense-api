// src/static/js/merchants_api.js

const API_URL = "http://localhost:8000/merchants";


// Função para obter todos os merchants
async function getMerchants() {
  try {
    const response = await fetch(API_URL);
    if (!response.ok) throw new Error("Erro ao carregar merchants");
    const merchants = await response.json();
    console.log(merchants);
    return merchants;
  } catch (err) {
    console.error(err);
  }
}

// Função create
async function createMerchant(name, location) {
  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, location })
    });
    if (!response.ok) throw new Error("Erro ao criar merchant");
    const merchant = await response.json();
    console.log("Criado:", merchant);
    return merchant;
  } catch (err) {
    console.error(err);
  }
}

// Função update
async function updateMerchant(id, name, location) {
  try {
    const response = await fetch(`${API_URL}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, location })
    });
    if (!response.ok) throw new Error("Erro ao atualizar merchant");
    const merchant = await response.json();
    console.log("Atualizado:", merchant);
    return merchant;
  } catch (err) {
    console.error(err);
  }
}

// Função delete
async function deleteMerchant(id) {
  try {
    const response = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
    if (!response.ok) throw new Error("Erro ao deletar merchant");
    console.log("Merchant deletado:", id);
  } catch (err) {
    console.error(err);
  }
}


getMerchants();
