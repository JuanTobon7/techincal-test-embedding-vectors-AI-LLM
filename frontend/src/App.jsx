import { useState } from "react";
import { suggestRae } from "./api/raeApi";

export default function App() {
  const [finalidad, setFinalidad] = useState("");
  const [concepto, setConcepto] = useState("");
  const [resultado, setResultado] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    setResultado("");

    try {
      const data = await suggestRae({
        finalidad_curso: finalidad,
        concepto_principal: concepto,
      });
      setResultado(data.rae_sugerido || "No se recibio sugerencia de RAE.");
    } catch (err) {
      const message =
        err?.response?.data?.detail ||
        "No fue posible obtener la sugerencia. Verifica que el backend este activo.";
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="page">
      <section className="panel">
        <h1>Asistente de RAE</h1>
        <p>Genera una propuesta de resultado de aprendizaje esperado.</p>

        <form onSubmit={handleSubmit} className="form">
          <label>
            Finalidad del curso
            <textarea
              value={finalidad}
              onChange={(event) => setFinalidad(event.target.value)}
              rows={4}
              required
            />
          </label>

          <label>
            Concepto principal
            <textarea
              value={concepto}
              onChange={(event) => setConcepto(event.target.value)}
              rows={3}
              required
            />
          </label>

          <button type="submit" disabled={loading}>
            {loading ? "Generando..." : "Sugerir RAE"}
          </button>
        </form>

        {error && <div className="error">{error}</div>}

        {resultado && (
          <article className="result-card">
            <h2>RAE sugerido</h2>
            <p>{resultado}</p>
          </article>
        )}
      </section>
    </main>
  );
}

