import axios from "axios";
import { requestFeedbackStore } from "./requestFeedbackStore";

const SLOW_REQUEST_THRESHOLD_MS = 8000;

const api = axios.create({
  baseURL: "https://techincal-test-embedding-vectors-ai-llm.onrender.com/api",
  timeout: 15000,
});

const requestTimeouts = new Map();
const slowRequests = new Set();
let requestIdCounter = 0;

function isNetworkOrServerError(error) {
  if (error?.code === "ERR_CANCELED") {
    return false;
  }

  if (!error || !error.response) {
    return true;
  }
  return error.response.status >= 500;
}

function clearRequestTimer(requestId) {
  const timeoutId = requestTimeouts.get(requestId);
  if (timeoutId) {
    clearTimeout(timeoutId);
    requestTimeouts.delete(requestId);
  }
}

function finalizeRequest(config, error = null) {
  const requestId = config?.metadata?.requestId;
  if (!requestId) {
    return;
  }

  clearRequestTimer(requestId);
  const wasSlow = slowRequests.delete(requestId);

  if (error && wasSlow && isNetworkOrServerError(error)) {
    requestFeedbackStore.showError();
    return;
  }

  if (slowRequests.size === 0) {
    requestFeedbackStore.clear();
  }
}

api.interceptors.request.use((config) => {
  if (requestFeedbackStore.getState().mode === "error") {
    requestFeedbackStore.clear();
  }

  const requestId = ++requestIdCounter;
  config.metadata = { ...(config.metadata || {}), requestId };

  const timeoutId = setTimeout(() => {
    requestTimeouts.delete(requestId);
    slowRequests.add(requestId);
    requestFeedbackStore.showLoading();
  }, SLOW_REQUEST_THRESHOLD_MS);

  requestTimeouts.set(requestId, timeoutId);
  return config;
});

api.interceptors.response.use(
  (response) => {
    finalizeRequest(response.config);
    return response;
  },
  (error) => {
    finalizeRequest(error.config, error);
    return Promise.reject(error);
  }
);

export default api;
