import React from "react";
import Navbar from "./components/Navbar";

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      <Navbar />

      <main className="flex-grow container mx-auto px-4 py-6">{children}</main>
    </div>
  );
};

export default Layout;
