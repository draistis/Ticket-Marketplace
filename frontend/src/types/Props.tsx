interface Event {
  id: number;
  name: string;
  description: string;
  end_datetime: string;
  category: string;
  start_datetime: string;
  location: number;
  organizer: number;
  created_at: string;
}
interface Location {
  id: number;
  city: string;
  country: string;
  name: string;
  address: string;
  capacity: number;
  description: string;
}

interface EventWithLocation extends Event {
  city: string;
  country: string;
  venue: string;
}

interface Ticket {
  id: number;
  sector: string;
  row: string;
  seat: number;
  price: number;
  event: number;
  owner: number;
  is_reserved: boolean;
  reserved_until: string;
}

export type { Event, Location, EventWithLocation, Ticket };
