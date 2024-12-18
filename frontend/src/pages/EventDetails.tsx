import React, { useEffect } from "react";
import api from "../api";
import { Location, Event, Ticket } from "../types/Props";
import { useParams } from "react-router-dom";
import { AuthContext } from "../context/Auth";
import { loadStripe } from "@stripe/stripe-js";

const EventDetailsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [eventDetails, setEventDetails] = React.useState<Event | null>(null);
  const [tickets, setTickets] = React.useState<Ticket[]>([]);
  const [location, setLocation] = React.useState<Location | null>(null);
  const [loading, setLoading] = React.useState(false);
  const [reservedTickets, setReservedTickets] = React.useState<Ticket[]>([]);
  const { isAuthenticated } = React.useContext(AuthContext);

  useEffect(() => {
    getEventDetails();
    getTickets();
    getReservedTickets();
  }, []);

  async function getEventDetails() {
    try {
      const eventRes = await api.get(`api/event/${id}/`);
      setEventDetails(eventRes.data);
      const locationRes = await api.get(`api/location/${eventRes.data.location}/`);
      setLocation(locationRes.data);
    } catch (error) {
      alert("Failed to fetch event details. Please try again.");
      console.error(error);
    }
  }
  async function getTickets() {
    try {
      setLoading(true);
      const ticketRes = await api.get(`api/event/${id}/tickets/`);
      setTickets(ticketRes.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }
  async function getReservedTickets() {
    try {
      const ticketRes = await api.get(`api/event/${id}/reservation/`);
      setReservedTickets(ticketRes.data);
    } catch (error) {
      console.error(error);
    }
  }
  async function handleTicketAdd(ticket_id: number) {
    if (!isAuthenticated) {
      alert("Please login to buy tickets.");
      return;
    } else {
      const response = await api.post(`api/ticket/${ticket_id}/reserve/`);
      if (response.status === 200) {
        getReservedTickets();
        getTickets();
      } else {
        alert(response.data);
      }
    }
  }
  async function removeTicket(ticket_id: number) {
    const response = await api.delete(`api/ticket/${ticket_id}/reserve/`);
    if (response.status === 200) {
      getReservedTickets();
      getTickets();
    } else {
      alert(response.data);
    }
  }
  const stripePromise = loadStripe("pk_test_51QXTrFLfoKR0enAtd21ULGubuHawevmSymJmVELOZyz7zr8UhxEDRW9Mt5FcRrRwzCMqj82QhkmBzO2xBkjMrNCx00PjS8YqCm");

  const handleCheckout = async () => {
    try {
      const response = await api.post("api/payment/create/");
      const session = response.data;
      const stripe = await stripePromise;

      const result = await stripe?.redirectToCheckout({
        sessionId: session.id,
      });

      if (result?.error) {
        console.error(result.error.message);
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 flex gap-8">
      <div className="w-3/5">
        {eventDetails ? (
          <>
            <div className="bg-white p-6 rounded-lg shadow-md h-min">
              <h1 className="text-3xl font-bold mb-4">{eventDetails.name}</h1>
              <p className="text-gray-700 mb-2">{eventDetails.description}</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md h-min mt-4">
              <h2 className="text-2xl font-semibold mb-4">Date & Time</h2>
              <p className="text-gray-600">
                {new Date(eventDetails.start_datetime).toLocaleString()}
              </p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md h-min mt-4">
              <h2 className="text-2xl font-semibold mb-4">Location</h2>
              <p className="text-gray-600">
                {location?.name}, {location?.city}, {location?.country}
              </p>
            </div>

            {reservedTickets.length > 0 ? (
              <>
                <hr className="my-6 h-0.5 border-t-0 bg-purple-700 opacity-100 dark:opacity-50" />
                <div className="bg-white p-6 rounded-lg shadow-md h-min mt-4">
                  <h2 className="text-2xl font-semibold mb-4">Your Reserved Tickets</h2>
                  <ul>
                    {reservedTickets.map((ticket) => (
                      <li
                        key={ticket.id}
                        className="flex justify-between p-4 mb-2 border rounded-md shadow-sm"
                      >
                        <div>
                          <p className="text-gray-800">
                            Sector: {ticket.sector}, Row: {ticket.row}, Seat: {ticket.seat}
                          </p>
                          <p className="text-gray-600">Price: ${ticket.price}</p>
                        </div>
                        <p className="text-green-600 font-semibold">Reserved</p>
                        <button
                          onClick={() => removeTicket(ticket.id)}
                          className="px-2 my-auto h-10 border-2 border-red-500 rounded-lg hover:bg-red-500 transition"
                        >
                          Remove
                        </button>
                      </li>
                    ))}
                  </ul>
                  <div className="flex justify-end">
                    <button
                      onClick={() => handleCheckout()}
                      className="mt-4 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
                    >
                      Checkout
                    </button>
                  </div>
                </div>
              </>
            ) : null}
          </>
        ) : (
          <p>Loading event details...</p>
        )}
      </div>

      <div className="w-2/5 bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-semibold mb-4">Available Tickets</h2>
        {tickets.length > 0 ? (
          <ul>
            {tickets.map((ticket) => (
              <li
                key={ticket.id}
                className="flex justify-between p-4 mb-2 border rounded-md shadow-sm"
              >
                <div>
                  <p className="text-gray-800">
                    Sector: {ticket.sector}, Row: {ticket.row}, Seat: {ticket.seat}
                  </p>
                  <p className="text-gray-600">Price: ${ticket.price}</p>
                </div>
                <button
                  onClick={() => handleTicketAdd(ticket.id)}
                  className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"
                >
                  Buy Ticket
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <p>No tickets available yet.</p>
        )}
        {loading && <p>Loading more tickets...</p>}
      </div>
    </div>
  );
};

export default EventDetailsPage;
