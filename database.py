import sqlite3
from schemas import ArtistCreate, SongCreate, PlaylistCreate


def get_db_connection():
    return sqlite3.connect("music.db")


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        artist_id INTEGER NOT NULL,
        FOREIGN KEY (artist_id) REFERENCES artists(id) ON DELETE CASCADE
    );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS playlists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS playlist_songs (
            playlist_id INTEGER NOT NULL,
            song_id INTEGER NOT NULL,
            FOREIGN KEY (playlist_id) REFERENCES playlists(id) ON DELETE CASCADE,
            FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE,
            UNIQUE (playlist_id, song_id)  -- Запрещаем дублирование песен в одном плейлисте
        );
        """)

    conn.commit()
    conn.close()


def add_artist(artist: ArtistCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO artists (name) VALUES (?);", (artist.name,))
        conn.commit()
        artist_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        return None

    conn.close()
    return {"id": artist_id, "name": artist.name}


def add_song(song: SongCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM artists WHERE id = ?;", (song.artist_id,))
    artist = cursor.fetchone()

    if not artist:
        conn.close()
        return None

    cursor.execute("INSERT INTO songs (title, artist_id) VALUES (?, ?);", (song.title, song.artist_id))
    conn.commit()
    song_id = cursor.lastrowid
    conn.close()

    return {"id": song_id, "title": song.title, "artist_id": song.artist_id}


def get_all_artists():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM artists;")
    artists = cursor.fetchall()

    result = []
    for artist in artists:
        artist_id, name = artist

        cursor.execute("SELECT id, title FROM songs WHERE artist_id = ?;", (artist_id,))
        songs = [{"id": song[0], "title": song[1]} for song in cursor.fetchall()]

        result.append({"id": artist_id, "name": name, "songs": songs})

    conn.close()
    return result



def get_all_songs():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT songs.id, songs.title, artists.name 
    FROM songs 
    JOIN artists ON songs.artist_id = artists.id;
    """)

    songs = [{"id": song[0], "title": song[1], "artist": song[2]} for song in cursor.fetchall()]

    conn.close()
    return songs


def delete_song(song_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM songs WHERE id = ?;", (song_id,))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return None

    conn.close()
    return {"message": "Песня удалена"}



def delete_artist(artist_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM artists WHERE name = ?;", (artist_name,))
    artist = cursor.fetchone()

    if not artist:
        conn.close()
        return None

    artist_id = artist[0]

    cursor.execute("SELECT COUNT(*) FROM songs WHERE artist_id = ?;", (artist_id,))
    song_count = cursor.fetchone()[0]

    if song_count > 0:
        conn.close()
        return "has_songs"

    cursor.execute("DELETE FROM artists WHERE id = ?;", (artist_id,))
    conn.commit()
    conn.close()
    return {"message": "Артист удален"}


def update_artist_name(old_name: str, new_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM artists WHERE name = ?;", (old_name,))
    artist = cursor.fetchone()

    if not artist:
        conn.close()
        return None

    try:
        cursor.execute("UPDATE artists SET name = ? WHERE name = ?;", (new_name, old_name))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return "name_exists"

    conn.close()
    return {"message": "Имя артиста обновлено"}


def get_artist_by_name(artist_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM artists WHERE name = ?;", (artist_name,))
    artist = cursor.fetchone()

    if not artist:
        conn.close()
        return None

    artist_id = artist[0]

    cursor.execute("SELECT id, title FROM songs WHERE artist_id = ?;", (artist_id,))
    songs = [{"id": song[0], "title": song[1]} for song in cursor.fetchall()]

    conn.close()
    return {"id": artist_id, "name": artist_name, "songs": songs}

def get_song_by_id(song_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT songs.id, songs.title, artists.name 
    FROM songs 
    JOIN artists ON songs.artist_id = artists.id
    WHERE songs.id = ?;
    """, (song_id,))

    song = cursor.fetchone()

    if not song:
        conn.close()
        return None

    conn.close()
    return {"id": song[0], "title": song[1], "artist": song[2]}


def create_playlist(playlist: PlaylistCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO playlists (name) VALUES (?);", (playlist.name,))
        conn.commit()
        playlist_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        return None

    conn.close()
    return {"id": playlist_id, "name": playlist.name}


def add_song_to_playlist(playlist_id: int, song_title: str, artist_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM playlists WHERE id = ?;", (playlist_id,))
    playlist = cursor.fetchone()
    if not playlist:
        conn.close()
        return "playlist_not_found"

    cursor.execute("SELECT id FROM artists WHERE name = ?;", (artist_name,))
    artist = cursor.fetchone()
    if not artist:
        conn.close()
        return "artist_not_found"

    artist_id = artist[0]

    cursor.execute("SELECT id FROM songs WHERE title = ? AND artist_id = ?;", (song_title, artist_id))
    song = cursor.fetchone()
    if not song:
        conn.close()
        return "song_not_found"

    song_id = song[0]

    try:
        cursor.execute("INSERT INTO playlist_songs (playlist_id, song_id) VALUES (?, ?);", (playlist_id, song_id))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return "already_exists"

    conn.close()
    return {"message": f"Песня '{song_title}' добавлена в плейлист"}


def remove_song_from_playlist(playlist_id: int, song_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM playlist_songs WHERE playlist_id = ? AND song_id = ?;", (playlist_id, song_id))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return None

    conn.close()
    return {"message": "Песня удалена из плейлиста"}


def delete_playlist(playlist_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM playlist_songs WHERE playlist_id = ?;", (playlist_id,))
    song_count = cursor.fetchone()[0]

    if song_count > 0:
        conn.close()
        return "not_empty"

    cursor.execute("DELETE FROM playlists WHERE id = ?;", (playlist_id,))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return None

    conn.close()
    return {"message": "Плейлист удален"}
