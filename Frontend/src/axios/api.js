import axios from "axios";
import store from "../redux/store";
import { logoutThunk, refreshToken } from "../redux/thunks/authThunk";
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
});

api.interceptors.request.use((config) => {
  const access = store.getState().auth.access_token;
  if (access) {
    config.headers.Authorization = `Bearer ${access}`;
  }
  return config;
});

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config;
    if (original?.url?.includes("/auth/refresh")) {
      return Promise.reject(error);
    }
    if (error.response?.status == 401 && !original._retry) {
      original._retry = true;
      try {
        const result = await store.dispatch(refreshToken()).unwrap();
        if (result.payload) {
          original.headers.Authorization = `Bearer ${result.access}`;
          return api(original);
        } else {
          store.dispatch(logoutThunk());
          window.location.href = "/login";
        }
      } catch (error) {
        store.dispatch(logoutThunk());
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  },
);

export default api;
