import RegistrationForm from './components/forms/registration/registration'
import LoginForm from './components/forms/login/login'
import Home from './components/pages/Home'
import Workspace from './components/pages/workspace/Workspace'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import React, { useState } from "react";
import axios from "axios";
import './App.css'

export default function App() {
  axios.defaults.withCredentials = true;
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/workspace" element={<Workspace />} />
      </Routes>
    </BrowserRouter>
  )
}

