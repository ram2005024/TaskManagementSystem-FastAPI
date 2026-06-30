import React from "react";
import { useSelector } from "react-redux";

const Main = () => {
  const { user } = useSelector((state) => state.auth);
  console.log(user);
  return <div>Hi {user?.username}</div>;
};

export default Main;
