interface Event {
  id: number;
  name: string;
  description: string;
  end_datetime: string;
  category: string;
  start_datetime: string;
  location: number;
  organizer: number;
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

export type { Event, Location, EventWithLocation };
