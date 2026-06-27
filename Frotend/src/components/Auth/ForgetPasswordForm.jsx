const ForgotPasswordForm = ({ data, setData, onSwitch }) => {
  const handleChange = (e) =>
    setData({ ...data, [e.target.name]: e.target.value });

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Forgot password email:", data.email);
    // later: send to FastAPI
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <h2 className="text-2xl font-semibold text-center text-gray-800">
        Reset Password
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

      {/* Submit */}
      <button
        type="submit"
        className="w-full bg-indigo-600 text-white rounded-full py-2.5 hover:bg-indigo-700 transition"
      >
        Send Reset Link
      </button>

      {/* Back to Login */}
      <p className="text-sm text-center text-gray-600">
        Back to{" "}
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

export default ForgotPasswordForm;
