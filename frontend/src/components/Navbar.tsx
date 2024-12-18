import React from "react";
import { AuthContext } from "../context/Auth";

const Navbar: React.FC = () => {
  const { isAuthenticated, user, logout } = React.useContext(AuthContext);

  return (
    <nav className="bg-white shadow-md border-b">
      <div className="container mx-auto flex items-center justify-between px-4 py-3">
        <div className="flex items-center space-x-12">
          <a href="/" className="text-purple-600 font-bold text-xl">
            Tickets
          </a>

          <div className="flex space-x-8">
            <a
              href="#"
              className="text-gray-600 hover:text-purple-600 border-b-2 border-transparent hover:border-purple-600 transition"
            >
              Concerts
            </a>
            <a
              href="#"
              className="text-gray-600 hover:text-purple-600 border-b-2 border-transparent hover:border-purple-600 transition"
            >
              Sports
            </a>
            <a
              href="#"
              className="text-gray-600 hover:text-purple-600 border-b-2 border-transparent hover:border-purple-600 transition"
            >
              Tech
            </a>
            {user?.is_organizer && (
              <>
                <a
                  href="/event/create"
                  className="text-gray-600 hover:text-purple-600 border-b-2 border-transparent hover:border-purple-600 transition"
                >
                  Create Event
                </a>
                <a
                  href="/ticket/create"
                  className="text-gray-600 hover:text-purple-600 border-b-2 border-transparent hover:border-purple-600 transition"
                >
                  Create Ticket
                </a>
              </>
            )}
          </div>
        </div>

        <div>
          {isAuthenticated ? (
            <button
              onClick={logout}
              className="px-4 py-2 border-purple-600 border-solid border-2 rounded hover:bg-purple-700 hover:text-white transition"
            >
              Logout
            </button>
          ) : (
            <a
              href="/login"
              className="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 transition"
            >
              Login
            </a>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
