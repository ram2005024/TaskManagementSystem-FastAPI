import { useState } from "react";
import LoginForm from "../components/Auth/LoginForm";
import RegisterForm from "../components/Auth/RegisterForm";
import SocialLogin from "../components/Auth/SocialLogin";
import ForgotPasswordForm from "../components/Auth/ForgetPasswordForm";

const AuthContainer = () => {
  const [page, setPage] = useState("login");

  // lifted state
  const [loginData, setLoginData] = useState({ email: "", password: "" });
  const [registerData, setRegisterData] = useState({
    name: "",
    email: "",
    password: "",
  });
  const [forgotData, setForgotData] = useState({ email: "" });

  return (
    <div className="flex items-center justify-center w-screen h-screen">
      <div className="p-4 mx-4 text-gray-500 bg-white shadow max-w-96 md:p-6 rounded-xl">
        {page === "login" && (
          <>
            <LoginForm
              data={loginData}
              setData={setLoginData}
              onSwitch={setPage}
            />
            <SocialLogin />
          </>
        )}
        {page === "register" && (
          <RegisterForm
            data={registerData}
            setData={setRegisterData}
            onSwitch={setPage}
          />
        )}
        {page === "forgot" && (
          <ForgotPasswordForm
            data={forgotData}
            setData={setForgotData}
            onSwitch={setPage}
          />
        )}
      </div>
    </div>
  );
};

export default AuthContainer;
