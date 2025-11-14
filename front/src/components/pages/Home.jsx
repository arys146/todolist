import { useNavigate } from 'react-router-dom';
import React, { useState } from "react";
import Modal from "./Modal";                 // <-- добавить
import LoginForm from "../forms/login/login";         // <-- добавить
import RegisterForm from "../forms/registration/registration";   // <-- добавить
import api from "../../api";
import axios from "axios";

import { CheckSquare, GitBranch, Package, Play, Target, Calendar, X } from 'lucide-react';

export default function Home() {
    const navigate = useNavigate();
    const [activeModal, setActiveModal] = useState(null); // 'login' | 'register' | null
    const [successRegister, setSuccessRegister] = useState(false);
    
    async function check_auth() {
        try {
            const response = await api.post("/check-auth");
            navigate('/workspace');
        } catch (error) {
            console.error("Error:", error);
        }
    }
    check_auth()

    const openLogin = (data = false) => {
        setSuccessRegister(data)
        setActiveModal("login")
    };
    const openRegister = () => setActiveModal("register");
    const closeModal = () => setActiveModal(null);

    return (
        <div className="min-h-screen bg-gradient-to-br from-purple-950 via-gray-900 to-purple-900">
            <nav className="p-6 flex justify-between items-center max-w-6xl mx-auto">
                <div className="flex items-center gap-2">
                <CheckSquare className="text-green-400" size={32} />
                <h1 className="text-2xl font-bold text-white">TodoList</h1>
                </div>
                <div className="flex gap-3">
                <button onClick={openLogin} className="px-6 py-2 rounded-lg bg-purple-600 hover:bg-purple-700 text-white transition-colors">
                    Login
                </button>
                <button onClick={openRegister} className="px-6 py-2 rounded-lg bg-green-500 hover:bg-green-600 text-white transition-colors">
                    Sign Up
                </button>
                </div>
            </nav>

        {/* Hero Section */}
            <div className="max-w-6xl mx-auto px-6 py-16">
                <div className="text-center mb-16">
                <h2 className="text-5xl font-bold text-white mb-4">
                    Organize Your Life
                </h2>
                <p className="text-xl text-gray-300 max-w-2xl mx-auto">
                    A powerful task and habit tracker to help you stay productive and build better routines
                </p>
                </div>

                {/* Features */}
                <div className="grid md:grid-cols-2 gap-6 mb-16">
                <div className="bg-purple-900/30 backdrop-blur-sm border border-purple-700/30 rounded-xl p-6">
                    <Target className="text-green-400 mb-4" size={40} />
                    <h3 className="text-2xl font-semibold text-white mb-3">Create Tasks</h3>
                    <p className="text-gray-300">
                    Organize your day with customizable tasks. Set priorities, due dates, and track your progress with ease.
                    </p>
                </div>
                
                <div className="bg-purple-900/30 backdrop-blur-sm border border-purple-700/30 rounded-xl p-6">
                    <Calendar className="text-green-400 mb-4" size={40} />
                    <h3 className="text-2xl font-semibold text-white mb-3">Build Habits</h3>
                    <p className="text-gray-300">
                    Track daily habits and build consistency. Visualize your streaks and watch your routines strengthen over time.
                    </p>
                </div>
                </div>

                {/* Setup Guide */}
                <div className="bg-gradient-to-br from-purple-900/40 to-purple-950/40 backdrop-blur-sm border border-purple-700/30 rounded-xl p-8">
                <h3 className="text-3xl font-bold text-white mb-6 text-center">Quick Setup Guide</h3>
                
                <div className="space-y-6">
                    <div className="flex gap-4">
                    <div className="flex-shrink-0 w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center">
                        <GitBranch className="text-white" size={24} />
                    </div>
                    <div>
                        <h4 className="text-xl font-semibold text-white mb-2">1. Clone Repository</h4>
                        <code className="block bg-gray-900/80 text-green-400 p-3 rounded-lg text-sm">
                        git clone https://github.com/arys146/todolist.git
                        </code>
                    </div>
                    </div>

                    <div className="flex gap-4">
                    <div className="flex-shrink-0 w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center">
                        <Package className="text-white" size={24} />
                    </div>
                    <div>
                        <h4 className="text-xl font-semibold text-white mb-2">2. Install Docker Desktop</h4>
                        <p className="text-gray-300">
                        Download and install Docker Desktop from{' '}
                        <a href="javascript:alert(1)" className="text-green-400 hover:text-green-300 underline">
                            docker.com
                        </a>
                        </p>
                    </div>
                    </div>

                    <div className="flex gap-4">
                    <div className="flex-shrink-0 w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center">
                        <Play className="text-white" size={24} />
                    </div>
                    <div>
                        <h4 className="text-xl font-semibold text-white mb-2">3. Start the Project</h4>
                        <code className="block bg-gray-900/80 text-green-400 p-3 rounded-lg text-sm">
                        cd todolist<br />
                        docker compose up -d --build
                        </code>
                        <p className="text-gray-300 mt-2">
                        Access the app at <span className="text-green-400">http://localhost:5173</span>
                        </p>
                    </div>
                    </div>
                </div>
                </div>

                <Modal open={activeModal} onClose={closeModal}>
                    <button onClick={closeModal} className="absolute right-4 top-4 text-gray-400 hover:text-white">
                        <X size={36} />
                    </button>

                    {activeModal === "login" && <LoginForm Redirect={openRegister} successReg={successRegister} />}
                    {activeModal === "register" && <RegisterForm Redirect={openLogin} />}
                </Modal>
            </div>
        </div>
    );
}