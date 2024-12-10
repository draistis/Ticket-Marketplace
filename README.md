
# Web API and client for buying tickets

## API Reference

#### Register user
```http
  POST /api/user/create/
```
#### Login to get JWT token
```http
  POST /api/login/
```
---
#### Get all users (superuser)
```http
  GET /api/user/list/
```
#### Modify user (self, superuser)
```http
  GET PUT DELETE /api/user/<id>/
```
---
#### Modify organizer (self aka associated user, superuser)
```http
  GET PUT DELETE /api/organizer/<id>/
```
---
#### Add a location (organizer, superuser)
```http
  POST /api/location/
```
#### Get all locations
```http
  GET /api/location/list/
```
#### Get location (anyone), modify (superuser)
```http
  GET PUT DELETE /api/location/<id>/
```
---
#### Add an event (organizer, superuser)
```http
  POST /api/event/
```
#### Get all events
```http
  GET /api/event/list/
```
#### Get all events for category
```http
  GET /api/event/list/
```
#### Get event (anyone), modify (self aka associated user, superuser)
```http
  GET PUT DELETE /api/event/<id>/
```
---
#### Add a reservation
```http
  POST /api/reservation/
```
#### Get all reservations
```http
  GET /api/reservation/list/
```
#### Get reservation (anyone), modify (self aka associated user, superuser)
```http
  GET PUT DELETE /api/reservation/<id>/
```
---
#### Add a ticket (organizer, superuser)
```http
  POST /api/reservation/
```
#### Get all tickets 
```http
  GET /api/reservation/list/
```
#### Get reservation (anyone), modify (self aka associated user, superuser)
```http
  GET PUT DELETE /api/reservation/<id>/
```
## License

[MIT](https://choosealicense.com/licenses/mit/)

