import { createAsyncThunk } from "@reduxjs/toolkit";
import api from "../../axios/api";

// Thunk-Refresh token
export const refreshToken = createAsyncThunk(
  "auth/refreshToken",
  async (_, thunkAPI) => {
    try {
      const res = await api.post(`/auth/refresh`);
      if (res.data) {
        return res.data;
      }
    } catch (error) {
      console.log(error);
      return thunkAPI.rejectWithValue(
        error.response?.data?.detail || error.message || "Something went wrong",
      );
    }
  },
);
// Logout
export const logoutThunk = createAsyncThunk(
  "auth/logoutThunk",
  async (_, thunkAPI) => {
    try {
      const res = await api.post(`/auth/logout`);
      return res.data;
    } catch (error) {
      console.log(error);
      return thunkAPI.rejectWithValue(`Error :${error || error.message}`);
    }
  },
);
// Login
export const loginThunk = createAsyncThunk(
  "auth/loginThunk",
  async ({ email, password }, thunkAPI) => {
    try {
      const res = await api.post("/auth/login", { email, password });
      if (res.data) return res.data;
    } catch (error) {
      return thunkAPI.rejectWithValue(
        error.response?.data?.detail || error.message || "Something went wrong",
      );
    }
  },
);
// Get the user info
export const getMeThunk = createAsyncThunk(
  "auth/getMeThunk",
  async (_, thunkAPI) => {
    try {
      const res = await api.get("/auth/me");
      return res.data;
    } catch (error) {
      console.log(error);
      return thunkAPI.rejectWithValue(
        error.response?.data?.detail || error.message || "Something went wrong",
      );
    }
  },
);
