import os
import sqlite3


def create_database(db_path: str | None = "../../data/01_raw/algorhythms.db") -> None:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")  # Foreign keys
    c = conn.cursor()

    # Create tables
    c.execute("""
    CREATE TABLE IF NOT EXISTS User (
        user_id TEXT PRIMARY KEY,
        age INTEGER,
        gender TEXT,
        location TEXT,
        music_profile TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS Artist (
        artist_id TEXT PRIMARY KEY,
        name TEXT,
        genres TEXT,
        popularity INTEGER
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS Album (
        album_id TEXT PRIMARY KEY,
        name TEXT,
        artist_id TEXT,
        release_date DATE,
        popularity INTEGER,
        genres TEXT,
        FOREIGN KEY (artist_id) REFERENCES Artist(artist_id)
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS Track (
        track_id TEXT PRIMARY KEY,
        name TEXT,
        artist_id TEXT,
        album_id TEXT,
        popularity INTEGER,
        genres TEXT,
        release_date DATE,
        FOREIGN KEY (artist_id) REFERENCES Artist(artist_id),
        FOREIGN KEY (album_id) REFERENCES Album(album_id)
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS UserTrackHistory (
        user_id TEXT,
        track_id TEXT,
        played_at DATETIME,
        is_top BOOLEAN,
        is_recent BOOLEAN,
        is_liked BOOLEAN,
        PRIMARY KEY (user_id, track_id, played_at),
        FOREIGN KEY (user_id) REFERENCES User(user_id),
        FOREIGN KEY (track_id) REFERENCES Track(track_id)
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS ChartTrack (
        chart_id TEXT,
        track_id TEXT,
        name TEXT,
        artist_id TEXT,
        album_id TEXT,
        popularity INTEGER,
        genres TEXT,
        release_date DATE,
        chart_name TEXT,
        position INTEGER,
        added_at DATE,
        PRIMARY KEY (chart_id, track_id),
        FOREIGN KEY (track_id) REFERENCES Track(track_id),
        FOREIGN KEY (artist_id) REFERENCES Artist(artist_id),
        FOREIGN KEY (album_id) REFERENCES Album(album_id)
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS Recommendation (
        user_id TEXT,
        track_id TEXT,
        album_id TEXT,
        score REAL,
        reason TEXT,
        created_at DATETIME,
        PRIMARY KEY (user_id, track_id, album_id),
        FOREIGN KEY (user_id) REFERENCES User(user_id),
        FOREIGN KEY (track_id) REFERENCES Track(track_id),
        FOREIGN KEY (album_id) REFERENCES Album(album_id)
    )
    """)

    conn.commit()
    conn.close()
    print(f"Database created at: {db_path}")


if __name__ == "__main__":
    create_database()
