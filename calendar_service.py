import json
import os
import zmq


EVENTS_FILE = "events.json"


def load_events():
    """
    Load events from JSON file.
    """
    if not os.path.exists(EVENTS_FILE):
        return []

    with open(EVENTS_FILE, "r") as file:
        return json.load(file)


def save_events(events):
    """
    Save events to JSON file.
    """
    with open(EVENTS_FILE, "w") as file:
        json.dump(events, file, indent=4)


def generate_event_id(events):
    """
    Generate a unique event ID.
    """
    if not events:
        return 1

    return max(event["event_id"] for event in events) + 1


def create_event(data):
    app_name = data.get("app_name")
    user_id = data.get("user_id")
    title = data.get("title")
    date = data.get("date")
    time = data.get("time")

    if not app_name:
        return {"message": "Missing app_name"}
    if not user_id:
        return {"message": "Missing user_id"}
    if not title:
        return {"message": "Missing title"}
    if not date:
        return {"message": "Missing date"}
    if not time:
        return {"message": "Missing time"}

    events = load_events()

    event = {
        "event_id": generate_event_id(events),
        "app_name": app_name,
        "user_id": user_id,
        "title": title,
        "date": date,
        "time": time
    }

    events.append(event)
    save_events(events)

    return {
        "message": "Event created",
        "event": event
    }


def get_events(data):
    user_id = data.get("user_id")

    if not user_id:
        return {"message": "Missing user_id"}

    events = load_events()

    return {
        "events": [e for e in events if e["user_id"] == user_id]
    }


def get_events_by_date(data):
    user_id = data.get("user_id")
    date = data.get("date")

    if not user_id:
        return {"message": "Missing user_id"}
    if not date:
        return {"message": "Missing date"}

    events = load_events()

    return {
        "events": [
            e for e in events
            if e["user_id"] == user_id and e["date"] == date
        ]
    }


def update_event(data):
    event_id = data.get("event_id")

    if event_id is None:
        return {"message": "Missing event_id"}

    events = load_events()

    for event in events:
        if event["event_id"] == event_id:

            if "title" in data:
                event["title"] = data["title"]
            if "date" in data:
                event["date"] = data["date"]
            if "time" in data:
                event["time"] = data["time"]

            save_events(events)

            return {
                "message": "Event updated",
                "event": event
            }

    return {"message": "Event not found"}


def delete_event(data):
    event_id = data.get("event_id")

    if event_id is None:
        return {"message": "Missing event_id"}

    events = load_events()

    for event in events:
        if event["event_id"] == event_id:
            events.remove(event)
            save_events(events)
            return {"message": "Event deleted"}

    return {"message": "Event not found"}


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5556")

    print("Calendar microservice running on port 5556")

    while True:
        request = socket.recv_string()
        data = json.loads(request)

        action = data.get("action")

        if action == "create_event":
            response = create_event(data)

        elif action == "get_events":
            response = get_events(data)

        elif action == "get_events_by_date":
            response = get_events_by_date(data)

        elif action == "update_event":
            response = update_event(data)

        elif action == "delete_event":
            response = delete_event(data)

        else:
            response = {"message": "Unknown action"}

        socket.send_string(json.dumps(response))


if __name__ == "__main__":
    main()