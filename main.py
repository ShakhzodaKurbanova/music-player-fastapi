from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, engine
from models import Base, Artist, Song, Playlist

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/artists", tags=['Исполнители'], summary='Добавить исполнителя')
def create_artist(name: str, db: Session = Depends(get_db)):
    artist = Artist(name=name)
    db.add(artist)
    db.commit()
    db.refresh(artist)
    return artist

@app.get("/artists", tags=['Исполнители'], summary='Все исполнители')
def list_artists(db: Session = Depends(get_db)):
    return db.query(Artist).all()

@app.get("/artists/{artist_id}", tags=['Исполнители'], summary='Искать исполнителя')
def find_artist(artist_id: int, db: Session = Depends(get_db)):
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(status_code=404, detail="Исполнитель не найден")
    return artist

@app.put("/artists/{artist_id}", tags=['Исполнители'], summary='Добавить исполнителя')
def modify_artist(artist_id: int, name: str, db: Session = Depends(get_db)):
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(status_code=404, detail="Исполнитель не найден")
    artist.name = name
    db.commit()
    return {"message": "Имя исполнителя обновлено"}

@app.delete("/artists/{artist_id}", tags=['Исполнители'], summary='Удалить исполнителя')
def remove_artist(artist_id: int, db: Session = Depends(get_db)):
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(status_code=404, detail="Исполнитель не найден")
    if artist.songs:
        raise HTTPException(status_code=405, detail="Нельзя удалить исполнителя, у которого есть песни")
    db.delete(artist)
    db.commit()
    return {"message": "Исполнитель удален"}

@app.post("/songs", tags=['Музыка'], summary='Добавить музыку')
def create_song(title: str, artist_name: str, db: Session = Depends(get_db)):
    artist = db.query(Artist).filter(Artist.name == artist_name).first()
    if not artist:
        raise HTTPException(status_code=404, detail="Исполнитель не найден")
    song = Song(title=title, artist=artist)
    db.add(song)
    db.commit()
    db.refresh(song)
    return song

@app.get("/songs", tags=['Музыка'], summary='Вся музыка')
def list_songs(db: Session = Depends(get_db)):
    return db.query(Song).all()

@app.get("/songs/{song_id}", tags=['Музыка'], summary='Найти музыку')
def find_song(song_id: int, db: Session = Depends(get_db)):
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Песня не найдена")
    return song

@app.put("/songs/{song_id}", tags=['Музыка'], summary='Изменить музыку')
def modify_song(song_id: int, title: str, db: Session = Depends(get_db)):
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Песня не найдена")
    song.title = title
    db.commit()
    return {"message": "Название песни обновлено"}

@app.delete("/songs/{song_id}", tags=['Музыка'], summary='Удалить музыку')
def remove_song(song_id: int, db: Session = Depends(get_db)):
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Песня не найдена")
    db.delete(song)
    db.commit()
    return {"message": "Песня удалена"}

@app.post("/playlists", tags=['Плейлисты'], summary='Создать плейлист')
def create_playlist(name: str, db: Session = Depends(get_db)):
    playlist = Playlist(name=name)
    db.add(playlist)
    db.commit()
    db.refresh(playlist)
    return playlist

@app.get("/playlists", tags=['Плейлисты'], summary='Все плейлисты')
def list_playlists(db: Session = Depends(get_db)):
    return db.query(Playlist).all()

@app.get("/playlists/{playlist_id}", tags=['Плейлисты'], summary='Найти плейлист')
def find_playlist(playlist_id: int, db: Session = Depends(get_db)):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Плейлист не найден")
    return playlist

@app.post("/playlists/{playlist_id}/songs", tags=['Плейлисты'], summary='Добавить песни плейлист')
def add_song_to_playlist(playlist_id: int, song_title: str, artist_name: str, db: Session = Depends(get_db)):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Плейлист не найден")

    song = db.query(Song).join(Artist).filter(Song.title == song_title, Artist.name == artist_name).first()
    if not song:
        raise HTTPException(status_code=404, detail="Песня не найдена")

    playlist.songs.append(song)
    db.commit()
    return {"message": "Песня добавлена в плейлист"}

@app.delete("/playlists/{playlist_id}/songs/{song_id}", tags=['Плейлисты'], summary='Удалить песню с плейлиста')
def remove_song_from_playlist(playlist_id: int, song_id: int, db: Session = Depends(get_db)):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Плейлист не найден")

    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Песня не найдена")

    playlist.songs.remove(song)
    db.commit()
    return {"message": "Песня удалена из плейлиста"}

@app.delete("/playlists/{playlist_id}", tags=['Плейлисты'], summary='Удалить плейлист')
def remove_playlist(playlist_id: int, db: Session = Depends(get_db)):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Плейлист не найден")
    if playlist.songs:
        raise HTTPException(status_code=405, detail="Нельзя удалить плейлист, если он не пустой")
    db.delete(playlist)
    db.commit()
    return {"message": "Плейлист удален"}
