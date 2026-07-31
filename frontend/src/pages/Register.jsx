import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { registerUser } from "../services/authService";
import { FaEnvelope, FaLock } from "react-icons/fa";

function Register() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
  username: "",
  email: "",
  password: "",
  confirmPassword: "",
});
const handleChange = (e) => {
  setFormData({
    ...formData,
    [e.target.name]: e.target.value,
  });
};

const handleRegister = async () => {
     if (formData.password !== formData.confirmPassword) {
    alert("Passwords do not match!");
    return;
   }
  try {
      await registerUser({
      username: formData.username,
      email: formData.email,
      password: formData.password,
    });  
    
    alert("Account created successfully! Please login.");

    navigate("/");
  } catch (error) {
    console.error(error);
    alert("Registration Failed");
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

          <h2 className="text-5xl font-bold text-center">
         Create Account
         </h2>

          <p className="text-gray-500 text-center mb-8">
            Create your account to continue
          </p>

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
         <div className="mb-5">
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
            className="w-full border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
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

          <div className="mb-5">
          <input
            type="password"
            name="confirmPassword"
            placeholder="Confirm Password"
            value={formData.confirmPassword}
            onChange={handleChange}
            className="w-full border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
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
  onClick={handleRegister}
  className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-xl font-semibold transition"
>
            Register
          </button>
                  <p className="text-center mt-6 text-gray-600">
           Already have an account?{" "}
           <span
             onClick={() => navigate("/")}
             className="text-blue-600 font-semibold cursor-pointer hover:underline"
           >
             Login
           </span>
         </p> 
        </div>
      </div>
    </div>
  );
}

export default Register;