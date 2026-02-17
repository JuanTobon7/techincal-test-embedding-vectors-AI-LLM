import api from "./httpClient";

export async function suggestRae(payload) {
  const response = await api.post("/sugerir-rae/", payload);
  return response.data;
}
