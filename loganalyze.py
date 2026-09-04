from datetime import datetime
from collections import Counter, defaultdict


def analyze_user_activity(log_file_path: str) -> dict:
  
    action_counts = Counter()
    user_action_counts = Counter()
    open_sessions = {}
    session_durations = []

    with open(log_file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = [p.strip() for p in line.split(",")]
            if len(parts) != 3:
                continue
            timestamp_str, user_id, action = parts

            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

            action_counts[action] += 1
            user_action_counts[user_id] += 1

            if action == "login":
                open_sessions[user_id] = timestamp
            elif action == "logout" and user_id in open_sessions:
                login_time = open_sessions.pop(user_id)
                duration = (timestamp - login_time).total_seconds()
                session_durations.append(duration)

    average_session_time = (
        sum(session_durations) / len(session_durations)
        if session_durations else 0.0
    )

    most_active_user = (
        max(user_action_counts, key=user_action_counts.get)
        if user_action_counts else None
    )

    total_users = len(user_action_counts)

    return {
        "action_counts": dict(action_counts),
        "average_session_time": average_session_time,
        "most_active_user": most_active_user,
        "total_users": total_users,
    }


if __name__ == "__main__":
    result = analyze_user_activity("activity.log")
    from pprint import pprint
    pprint(result)

    # {'action_counts': {'login': 2, 'logout': 2, 'submit': 1, 'view': 2},
    #  'average_session_time': 160.0,
    #  'most_active_user': 'u002',
    #  'total_users': 2}

