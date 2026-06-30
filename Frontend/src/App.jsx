import React, { useEffect } from "react";
import store from "./redux/store";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Auth from "./pages/Auth";
import { Provider, useDispatch, useSelector } from "react-redux";
import PublicLayout from "./layout/PublicLayout";
import ProtectedLayout from "./layout/ProtectedLayout";
import Main from "./pages/Main";
import Home from "./pages/Home";
import ProtectedRoute from "./middleware/ProtectedRoute";
import PublicRoute from "./middleware/PublicRoute";
import {
  getMeThunk,
  logoutThunk,
  refreshToken,
} from "./redux/thunks/authThunk";
const routes = createBrowserRouter([
  {
    path: "/login",
    element: (
      <PublicRoute>
        <Auth />
      </PublicRoute>
    ),
  },
  {
    path: "/",
    element: <PublicLayout />,
    children: [
      {
        index: true,
        element: <Home />,
      },
    ],
  },
  {
    path: "/dashboard",
    element: (
      <ProtectedRoute>
        <ProtectedLayout />
      </ProtectedRoute>
    ),
    children: [
      {
        index: true,
        element: <Main />,
      },
    ],
  },
]);

const App = () => {
  const dispatch = useDispatch();
  const { access_token } = useSelector((state) => state.auth);
  // Get the access token when the app loads
  useEffect(() => {
    (async () => {
      try {
        const res = await dispatch(refreshToken()).unwrap();
        if (res.access) {
          await dispatch(getMeThunk()).unwrap();
        }
      } catch (error) {
        console.error(error);
        dispatch(logoutThunk());
      }
    })();
  }, [dispatch]);
  return (
    <div className="min-h-screen min-w-screen">
      <RouterProvider router={routes}></RouterProvider>
    </div>
  );
};

export default App;
