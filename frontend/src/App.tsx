import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Home from "./pages/Home";
import Register from "./pages/Register";
import NotFound from "./pages/NotFound";
import Layout from "./Layout";
import EventDetailsPage from "./pages/EventDetails";
import CreateEvent from "./pages/CreateEvent";
import CreateTicketPage from "./pages/CreateTicket";


function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/event/:id" element={<EventDetailsPage />} />
          <Route path="/event/create" element={<CreateEvent />} />
          <Route path="/ticket/create" element={<CreateTicketPage />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
