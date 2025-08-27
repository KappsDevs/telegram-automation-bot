import connection


def create_messages_table():
    try:
        with connection.get_connection() as con:
            with con.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS messages (
                        message_id BIGINT PRIMARY KEY,
                        date TIMESTAMP,
                        sender TEXT,
                        content TEXT,
                        ocr_text TEXT,
                        chat_id TEXT,
                        sent BOOL
                    )
                """)
            con.commit()
    except Exception as e:
        print(f"Error creating messages table: {e}")


def mark_messages_as_sent(message_ids):
    if isinstance(message_ids, int):
        message_ids = [message_ids]

    try:
        with connection.get_connection() as con:
            with con.cursor() as cur:
                cur.execute("""
                    UPDATE messages
                    SET sent = TRUE
                    WHERE message_id = ANY(%s)
                """, (message_ids,))
            con.commit()
    except Exception as e:
        print(f"Error marking messages as sent: {e}")


def truncate_table():
    try:
        with connection.get_connection() as con:
            with con.cursor() as cur:
                cur.execute("TRUNCATE TABLE messages")
            con.commit()
    except Exception as e:
        print(f"Error truncating table: {e}")


def insert_into_db(message, img_text):
    try:
        with connection.get_connection() as con:
            with con.cursor() as cur:
                cur.execute("""
                    INSERT INTO messages (message_id, date, sender, content, ocr_text, chat_id, sent)
                    VALUES (%s, %s, %s, %s, %s,  %s,FALSE)
                """, (
                    message.id,
                    message.date,
                    getattr(message.sender, 'username', None),
                    message.text,
                    img_text,
                    message.chat_id ,
                ))
            con.commit()
    except Exception as e:
        print(f"Error inserting message {message.id}: {e}")



def get_unsent_messages():
    try:
        with connection.get_connection() as con:
            with con.cursor() as cur:
                cur.execute("""
                    SELECT message_id,
                           date,
                           sender,
                           content,
                           ocr_text
                    FROM messages
                    WHERE sent = FALSE
                    ORDER BY date DESC
                """)
                rows = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
                return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        print(f"Error: {e}")
        return []
