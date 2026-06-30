import React from "react";
import { Outlet } from "react-router-dom";
import Navbar from "../components/ProtectedLayout/Nav";

const ProtectedLayout = () => {
  return (
    <div className="w-screen h-screen">
      <Navbar />
      <Outlet />
    </div>
  );
};

export default ProtectedLayout;
