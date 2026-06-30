import React from "react";
import { useSelector } from "react-redux";
import { Navigate } from "react-router-dom";

const PublicRoute = ({ children }) => {
  const { access_token } = useSelector((state) => state.auth);
  console.log("Access Token yaha xa hai");
  if (access_token) {
    return <Navigate to="/dashboard" replace />;
  } else return children;
};

export default PublicRoute;
