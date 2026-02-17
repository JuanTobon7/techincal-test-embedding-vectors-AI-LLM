import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "https://juanchodev.pythonanywhere.com/",
  timeout: 15000,
});

export async function suggestRae(payload) {
  const response = await api.post("/sugerir-rae/", payload);
  return response.data;
}

