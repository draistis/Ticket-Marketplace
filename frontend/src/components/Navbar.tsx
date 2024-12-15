import React from "react";

const Navbar: React.FC = () => {
  return (
    <nav className="bg-white shadow-md border-b">
      <div className="container mx-auto flex items-center justify-between px-4 py-3">
        {/* Left Side - Logo and Links */}
        <div className="flex items-center space-x-12">
          {/* Logo */}
          <a href="#" className="text-purple-600 font-bold text-xl">
            MyBrand
          </a>

          {/* Navigation Links */}
          <div className="flex space-x-8">
            <a
              href="#"
              className="text-gray-600 hover:text-purple-600 border-b-2 border-transparent hover:border-purple-600 transition"
            >
              Dashboard
            </a>
            <a
              href="#"
              className="text-gray-600 hover:text-purple-600 border-b-2 border-transparent hover:border-purple-600 transition"
            >
              Team
            </a>
            <a
              href="#"
              className="text-gray-600 hover:text-purple-600 border-b-2 border-transparent hover:border-purple-600 transition"
            >
              Projects
            </a>
            <a
              href="#"
              className="text-gray-600 hover:text-purple-600 border-b-2 border-transparent hover:border-purple-600 transition"
            >
              Calendar
            </a>
          </div>
        </div>

        {/* Right Side - Login Button */}
        <div>
          <a
            href="#login"
            className="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 transition"
          >
            Login
          </a>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
