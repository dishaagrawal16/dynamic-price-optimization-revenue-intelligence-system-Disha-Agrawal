import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../services/authService";
import { FaEnvelope, FaLock } from "react-icons/fa";

function Login() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
  username: "",
  password: "",
  role:"business_analyst"
});
const handleChange = (e) => {
  setFormData({
    ...formData,
    [e.target.name]: e.target.value,
  });
};

const handleLogin = async () => {
  try {
    console.log(formData);
    const data = await loginUser(formData);

    localStorage.setItem("token", data.access_token);
    localStorage.setItem("role", data.role);
    alert("Login Successful!");

    navigate("/dashboard");
  } catch (error) {
    console.error(error);
    alert("Invalid Username or Password");
  }
};
  return (
    <div className="min-h-screen flex">
      {/* Left Section */}
      <div className="hidden lg:flex w-1/2 bg-gradient-to-br from-blue-600 to-indigo-700 text-white flex-col justify-center items-center p-10">
        <h1 className="text-5xl font-bold mb-6">PricePilot AI</h1>

        <p className="text-xl text-center max-w-md">
          Dynamic Pricing Optimization & Revenue Intelligence System
        </p>
      </div>

      {/* Right Section */}
      <div className="w-full lg:w-1/2 flex justify-center items-center bg-gray-100">
        <div className="bg-white shadow-2xl rounded-2xl p-10 w-[420px]">

          <h2 className="text-3xl font-bold text-center mb-2">
            Welcome Back
          </h2>

          <p className="text-gray-500 text-center mb-8">
            Login to continue
          </p>
          <div className="mb-5">
  <label className="block font-semibold mb-2">
    Login As
  </label>

  <select
    name="role"
    value={formData.role}
    onChange={handleChange}
    className="w-full border rounded-lg py-3 px-4"
  >
    <option value="admin">👑 Admin</option>
    <option value="business_analyst">📊 Business Analyst</option>
  </select>
</div>
          {/* Email */}
          <div className="relative mb-5">
            <FaEnvelope className="absolute left-4 top-4 text-gray-400" />

            <input
              type="text"
              name="username"
              placeholder="Username"
              value={formData.username}
              onChange={handleChange}
              className="w-full border rounded-lg py-3 pl-12 pr-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
/>
          </div>

          {/* Password */}
          <div className="relative mb-5">
            <FaLock className="absolute left-4 top-4 text-gray-400" />

           <input
             type="password"
             name="password"
             placeholder="Password"
             value={formData.password}
             onChange={handleChange}
             className="w-full border rounded-lg py-3 pl-12 pr-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
           />
          </div>

          <div className="flex justify-between text-sm mb-6">
            <label>
              <input type="checkbox" className="mr-2" />
              Remember Me
            </label>

            <a href="#" className="text-blue-600">
              Forgot Password?
            </a>
          </div>

          <button
  onClick={handleLogin}
  className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-xl font-semibold transition"
>
            Login
          </button>
          <p className="text-center mt-6 text-gray-600">
  Don't have an account?{" "}
  <span
    onClick={() => navigate("/register")}
    className="text-blue-600 font-semibold cursor-pointer hover:underline"
  >
    Register
  </span>
</p>
        </div>
      </div>
    </div>
  );
}

export default Login;