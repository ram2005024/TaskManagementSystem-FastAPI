import { createSlice } from "@reduxjs/toolkit";
import {
  getMeThunk,
  loginThunk,
  logoutThunk,
  refreshToken,
} from "../thunks/authThunk";

// Create the auth slice
const initialState = {
  loading: true,
  user: null,
  access_token: null,
};
const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      // For refresh-token
      .addCase(refreshToken.pending, (state) => {
        state.loading = true;
      })
      .addCase(refreshToken.fulfilled, (state, action) => {
        state.access_token = action.payload.access;
        state.loading = false;
      })
      .addCase(refreshToken.rejected, (state) => {
        state.loading = false;
        state.user = null;
        state.access_token = null;
      })
      // For logout
      .addCase(logoutThunk.fulfilled, (state) => {
        state.user = null;
        state.access_token = null;
      })
      // For login
      .addCase(loginThunk.fulfilled, (state, action) => {
        state.access_token = action.payload.access;
      })
      .addCase(loginThunk.rejected, (state, action) => {
        state.access_token = null;
        state.loading = false;
      })
      .addCase(getMeThunk.fulfilled, (state, action) => {
        state.user = action.payload;
      });
  },
});
export default authSlice.reducer;
