import json
import zmq


def send_request(socket, payload):
    """
    Helper function to send request and print response.
    """
    socket.send_string(json.dumps(payload))
    response = socket.recv_string()
    print(json.dumps(json.loads(response), indent=4))
    print("-" * 40)


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    # Connect to calendar 
    socket.connect("tcp://localhost:5556")

    # 1. Create event
    print("Creating event...")
    send_request(socket, {
        "action": "create_event",
        "app_name": "TaskApp",
        "user_id": "123",
        "title": "Study for Test",
        "date": "2026-06-10",
        "time": "18:00"
    })

    # Get  events
    print("Getting all events...")
    send_request(socket, {
        "action": "get_events",
        "user_id": "123"
    })

    # Update event 
    print("Updating event...")
    send_request(socket, {
        "action": "update_event",
        "event_id": 1,
        "time": "19:00"
    })

    # Get events by date
    print("Getting events by date...")
    send_request(socket, {
        "action": "get_events_by_date",
        "user_id": "123",
        "date": "2026-06-10"
    })

    # Delete event
    print("Deleting event...")
    send_request(socket, {
        "action": "delete_event",
        "event_id": 1
    })

    # Confirm deletion
    print("Final check...")
    send_request(socket, {
        "action": "get_events",
        "user_id": "123"
    })


if __name__ == "__main__":
    main()