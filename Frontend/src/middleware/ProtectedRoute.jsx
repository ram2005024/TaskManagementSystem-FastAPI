import React from "react";
import { useSelector } from "react-redux";
import LoaderFull from "../components/Loader/LoaderFull";
import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ children }) => {
  const { access_token, loading, user } = useSelector((state) => state.auth);
  if (loading) {
    return <LoaderFull />;
  } else if (!access_token) {
    return <Navigate to="/login" replace />;
  } else {
    return children;
  }
};

export default ProtectedRoute;
