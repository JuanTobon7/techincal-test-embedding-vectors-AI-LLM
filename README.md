# AI-Assisted RAE Generator Prototype

This repository contains a production-oriented prototype to support university professors in generating **Resultados de Aprendizaje Esperado (RAE)** using an extensible AI architecture.

## 1) System Architecture

The solution is split into two decoupled applications:

- `backend/` Django + DRF API with clear service layers
- `frontend/` React (Vite) client for interaction

Backend module design (`learning_outcomes`):

- `views.py`: HTTP orchestration only
- `serializers.py`: request validation
- `services/prompt_builder.py`: prompt construction
- `services/institutional_context.py`: institutional context injection (RAG-ready)
- `services/llm_service.py`: provider abstraction and implementation
- `services/rae_service.py`: business use case orchestration
- `models.py`: persistence model for institutional embeddings

This separation keeps transport logic, domain logic, and provider logic independent.

## 2) Why Django + DRF

Django + DRF were selected for:

- Fast delivery of robust, testable API endpoints
- Mature ORM and migration system for PostgreSQL
- Clean request/response lifecycle and serializer-based validation
- Strong maintainability for enterprise teams

## 3) Why a Decoupled React Frontend

Frontend is intentionally separated from backend to enable:

- Independent deployment and scaling
- Team autonomy (frontend/backend can evolve separately)
- Future integration with additional channels (LMS plugin, mobile app)
- Clean API-first architecture from day one

## 4) Why pgvector From Day One

`pgvector` is included immediately to avoid re-architecture later.

Model `InstitutionalEmbedding` already stores:

- `content`: institutional guideline fragments
- `embedding`: vector representation for semantic retrieval

Even with static context now, schema and dependency are already prepared for real retrieval.

## 5) Why an LLM Abstraction Layer

`BaseLLMService` isolates business logic from provider SDK details.

Benefits:

- Swap providers (OpenAI, Azure OpenAI, Anthropic, local models) without changing `RAEService`
- Easier testing with deterministic mocks
- Lower coupling and safer future vendor changes

## 6) Path to Real RAG (Iteration 2)

Current flow uses static institutional rules through `get_institutional_context()`.

Iteration 2 can extend this function to:

1. Embed user query (`finalidad_curso + concepto_principal`)
2. Run similarity search in PostgreSQL (`InstitutionalEmbedding` + pgvector)
3. Retrieve top-k closest guideline chunks
4. Inject retrieved context into prompt builder
5. Preserve unchanged API contract and business flow

Because the context retrieval is already encapsulated, migration to real RAG is incremental.

## 7) Run Backend

Prerequisites:

- Python 3.12+
- PostgreSQL 15+ with `vector` extension enabled

Steps:

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

pip install -r ../requirements.txt
# Windows
copy .env.example .env
# Linux/Mac
cp .env.example .env

python manage.py migrate
python manage.py runserver
```

API endpoint:

- `POST http://localhost:8000/api/sugerir-rae/`

Request body:

```json
{
  "finalidad_curso": "Formar al estudiante en la resolucion de problemas reales de manufactura",
  "concepto_principal": "modelado de procesos"
}
```

## 8) Run Frontend

Prerequisites:

- Node.js 20+

Steps:

```bash
cd frontend
npm install
# Windows
copy .env.example .env
# Linux/Mac
cp .env.example .env

npm run dev
```

App URL:

- `http://localhost:5173`

## Prompt Used in `prompt_builder.py`

```text
Eres un experto en diseno curricular universitario.

Tu tarea es proponer un unico Resultado de Aprendizaje Esperado (RAE) en espanol para una asignatura.

Debes seguir estrictamente el contexto institucional y redactar una salida evaluable y medible.

Contexto institucional:
{institutional_context}

Insumos del profesor:
Finalidad del curso: {finalidad_curso}
Concepto principal: {concepto_principal}

Reglas de salida:
- Entregar solo un RAE, en una sola oracion.
- Empezar con un verbo de accion alineado con Bloom.
- Debe ser observable y evaluable.
- Mantener tono academico formal.
- No incluir explicaciones adicionales ni listas.
```


