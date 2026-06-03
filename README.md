A. Calendar-Microservice

The Calendar Microservice manages scheduled events for applications such as fitness apps and task managers. It allows applications to create, retrieve, update, and delete calendar events. The microservice communicates using JSON messages and returns either event data or error messages.

B. To programmatically REQUEST data from the microservice:

A program connects to it using ZeroMQ. It sends a message in JSON format that includes the required information:

- app_name: Name of the application making the request
- user_id: Unique identifier for the user
- action: The operation to perform on the calendar service

Supported actions:
- create_event
- get_events
- get_events_by_date
- update_event
- delete_event

Depending on the action, additional fields may be required:

create_event requires:
- title: Name of the event
- date: Event date (YYYY-MM-DD)
- time: Event time

get_events requires:
- user_id

get_events_by_date requires:
- user_id
- date

update_event requires:
- event_id
- (optional) title
- (optional) date
- (optional) time

delete_event requires:
- event_id

The microservice uses this information to perform the requested operation and returns either a success response or an error message.

The service returns an error message if:

- app_name is missing
- user_id is missing (when required)
- action is missing or invalid
- required fields for an action are missing
- event_id does not exist (for update/delete operations)

Example Request:

```

{
    "action": "create_event",
    "app_name": "Fitness App",
    "user_id": "user123",
    "title": "Leg Day Workout",
    "date": "2026-06-10",
    "time": "18:00"
}

```


Explanation:
1. ZeroMQ context and REQ socket are created
2. The client connects to the microservice at tcp://localhost:5556
3. JSON request is constructed with the required fields
4. The request is converted to a JSON string and sent to the microservice


C. To programmatically RECEIVE data from the microservice:

After sending a request, the program waits for a response from the microservice. The response comes back as a JSON string. The program then converts it into a Python dictionary so it can be used or printed.

Example Response Code:

```
response = socket.recv_string()
data = json.loads(response)

print(data)
```

Example Successful Response (Create Event):

```

{
    "message": "Event created",
    "event": {
        "event_id": 1,
        "app_name": "Fitness App",
        "user_id": "user123",
        "title": "Leg Day Workout",
        "date": "2026-06-10",
        "time": "18:00"
    }
}
```

Example Successful Response (Get Events):

```

{
    "events": [
        {
            "event_id": 1,
            "app_name": "Fitness App",
            "user_id": "user123",
            "title": "Leg Day Workout",
            "date": "2026-06-10",
            "time": "18:00"
        }
    ]
}

```
Example Error Response:

```
{
    "message": "Event not found"
}
```

```
{
    "message": "Missing required field: title"
}
```


Explanation:
1. recv_string() waits for a response from the microservice
2. json.loads() converts the JSON string into a Python dictionary
3. The application can access returned values using dictionary keys such as events, event, or message