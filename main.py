from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents

def main():
    print("==== Week 8 Database Demo ====")

    conn = connect_database()
    create_all_tables(conn)
    conn.close()

    migrate_users_from_file()

    success, msg = register_user("alice", "Pass123!", "analyst")
    print(msg)

    success, msg = login_user("alice", "Pass123!")
    print(msg)

    incident_id = insert_incident(
        "2024-11-05",
        "Phishing",
        "High",
        "Open",
        "Suspicious email detected",
        "alice"
    )
    print(f"Created incident #{incident_id}")

    df = get_all_incidents()
    print(df.head())

if __name__ == "__main__":
    main()
