import { useDispatch, useSelector } from "react-redux";
import toast from "react-hot-toast";
import { loginThunk } from "../../redux/thunks/authThunk";
import { Navigate, useNavigate } from "react-router-dom";
const LoginForm = ({ data, setData, onSwitch }) => {
  const handleChange = (e) =>
    setData({ ...data, [e.target.name]: e.target.value });
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await dispatch(loginThunk(data)).unwrap();
      if (res.message) {
        navigate("/dashboard");
        toast.success(res.message);
      }
    } catch (error) {
      console.log(error);
      toast.error(error);
    }
  };
  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <h2 className="text-2xl font-semibold text-center text-gray-800">
        Welcome Back
      </h2>

      {/* Email */}
      <input
        name="email"
        type="email"
        value={data.email}
        onChange={handleChange}
        placeholder="Enter your email"
        className="w-full border border-gray-300 rounded-full px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        required
      />

      {/* Password */}
      <input
        name="password"
        type="password"
        value={data.password}
        onChange={handleChange}
        placeholder="Enter your password"
        className="w-full border border-gray-300 rounded-full px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        required
      />

      {/* Forgot Password */}
      <div className="text-right">
        <button
          type="button"
          onClick={() => onSwitch("forgot")}
          className="text-sm text-blue-600 hover:underline"
        >
          Forgot Password?
        </button>
      </div>

      {/* Submit */}
      <button
        type="submit"
        className="w-full bg-indigo-600 text-white rounded-full py-2.5 hover:bg-indigo-700 transition"
      >
        Log In
      </button>

      {/* Switch to Register */}
      <p className="text-sm text-center text-gray-600">
        Don’t have an account?{" "}
        <button
          type="button"
          onClick={() => onSwitch("register")}
          className="text-blue-600 hover:underline"
        >
          Signup
        </button>
      </p>
    </form>
  );
};

export default LoginForm;
