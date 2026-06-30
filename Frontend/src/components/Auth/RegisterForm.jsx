const RegisterForm = ({ data, setData, onSwitch }) => {
  const handleChange = (e) =>
    setData({ ...data, [e.target.name]: e.target.value });

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Register values:", data);
    // later: send to FastAPI
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <h2 className="text-2xl font-semibold text-center text-gray-800">
        Create Account
      </h2>

      {/* Name */}
      <input
        name="name"
        type="text"
        value={data.name}
        onChange={handleChange}
        placeholder="Enter your name"
        className="w-full border border-gray-300 rounded-full px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        required
      />

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

      {/* Submit */}
      <button
        type="submit"
        className="w-full bg-indigo-600 text-white rounded-full py-2.5 hover:bg-indigo-700 transition"
      >
        Register
      </button>

      {/* Switch to Login */}
      <p className="text-sm text-center text-gray-600">
        Already have an account?{" "}
        <button
          type="button"
          onClick={() => onSwitch("login")}
          className="text-blue-600 hover:underline"
        >
          Login
        </button>
      </p>
    </form>
  );
};

export default RegisterForm;
