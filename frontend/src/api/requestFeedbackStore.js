const listeners = new Set();

let state = { mode: "idle" };

function emit() {
  listeners.forEach((listener) => listener(state));
}

export const requestFeedbackStore = {
  getState() {
    return state;
  },
  subscribe(listener) {
    listeners.add(listener);
    return () => {
      listeners.delete(listener);
    };
  },
  showLoading() {
    if (state.mode !== "loading") {
      state = { mode: "loading" };
      emit();
    }
  },
  showError() {
    if (state.mode !== "error") {
      state = { mode: "error" };
      emit();
    }
  },
  clear() {
    if (state.mode !== "idle") {
      state = { mode: "idle" };
      emit();
    }
  },
};

