import React, { useState } from "react";
import { LogIn, User, Lock } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import api from "../../../api";  
import { tokenStore } from "../../../tokenStore";
import axios from "axios";

export default function LoginForm({Redirect, successReg}) {

    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        username: '',
        password: ''
    });

  const data = [
    { title: "Логин",
      name:"login",
      placeholder:"Уникальный логин",
      onChange: (e) => setUsername(e.target.value),
      field_error: "Введите уникальный логин"
    },
    { title: "Пароль",
      name:"password",
      placeholder:"Введите пароль",
      type: "password",
      onChange: (e) => setPassword(e.target.value)
    },
  ]

  async function loginUser(payload) {
    try {
      const { data } = await api.post("/login", payload);
      tokenStore.set(data.access_token);       
      navigate("/workspace");
    } catch (error) {
      console.error("Error:", error);
    }
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    loginUser(formData);
  };

  return (
    
      <div className="rounded-2xl p-12 w-full max-w-md ">
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="w-12 h-12 bg-green-500 rounded-xl flex items-center justify-center">
              <LogIn className="text-white" size={24} />
            </div>
          </div>
          <h2 className="text-3xl font-bold text-white mb-2">Welcome</h2>
          {successReg === true && <p className="text-green-400 text-sm">You registered successfully, login to continue</p>}
        </div>

        <form className="space-y-5" onSubmit={handleSubmit}>
          <div className="space-y-2">
            <label className="text-white text-sm font-medium">Username</label>
            <div className="relative">
              <User className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
              <input
                type="text"
                name="username"
                placeholder="Enter your username"
                value={formData.username}
                onChange={handleChange}
                className="w-full pl-11 pr-4 py-3 bg-gray-900/80 border border-purple-700/30 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-green-500 transition-colors"
                required
              />
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-white text-sm font-medium">Password</label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
              <input
                type="password"
                name="password"
                placeholder="Enter your password"
                value={formData.password}
                onChange={handleChange}
                className="w-full pl-11 pr-4 py-3 bg-gray-900/80 border border-purple-700/30 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-green-500 transition-colors"
                required
              />
            </div>
          </div>

          <button 
            type="submit"
            className="w-full py-3 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-semibold rounded-lg shadow-lg transform hover:scale-105 transition-all mt-2"
          >
            Login
          </button>
        </form>

        <div className="text-center mt-6 text-gray-300 text-sm">
          Don't have an account?{' '}
          <a onClick={Redirect} className="cursor-pointer text-green-400 hover:text-green-300 font-medium">
            Sign Up
          </a>
        </div>
      </div>
    

  );
}