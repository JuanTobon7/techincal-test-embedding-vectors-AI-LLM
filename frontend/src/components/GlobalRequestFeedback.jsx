import { useEffect, useState } from "react";
import { requestFeedbackStore } from "../api/requestFeedbackStore";

const COLD_START_MESSAGE =
  "The server is starting (cold start). This may take a few minutes. Please wait.";
const SERVER_DOWN_MESSAGE =
  "The server is not responding. Please try again later.";

export default function GlobalRequestFeedback() {
  const [mode, setMode] = useState(requestFeedbackStore.getState().mode);

  useEffect(() => {
    return requestFeedbackStore.subscribe((nextState) => {
      setMode(nextState.mode);
    });
  }, []);

  if (mode === "idle") {
    return null;
  }

  const isError = mode === "error";

  return (
    <div
      className="global-request-feedback"
      aria-live={isError ? "assertive" : "polite"}
      aria-atomic="true"
    >
      <section
        className={`global-request-feedback__card${isError ? " is-error" : ""}`}
        role={isError ? "alert" : "status"}
      >
        {!isError && (
          <div className="global-request-feedback__spinner" aria-hidden="true" />
        )}
        <p>{isError ? SERVER_DOWN_MESSAGE : COLD_START_MESSAGE}</p>
      </section>
    </div>
  );
}

