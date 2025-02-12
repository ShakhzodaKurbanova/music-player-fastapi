from fastapi import FastAPI, HTTPException
import database as db
from schemas import ArtistCreate, SongCreate, ArtistUpdate, PlaylistCreate

app = FastAPI()


### ИСПОЛНИТЕЛИ ###

@app.post('/add_artists', tags=['Исполнители'], summary='Добавить исполнителя')
def create_artist(artist: ArtistCreate):
    result = db.add_artist(artist)
    if result is None:
        raise HTTPException(status_code=400, detail="Артист с таким именем уже существует")
    return result

@app.get('/get_artists', tags=['Исполнители'], summary='Все исполнители')
def get_artists():
    return db.get_all_artists()

@app.get('/get_artist/{artist_id}', tags=['Исполнители'], summary='Искать исполнителя')
def search_artist(artist_name: str):
    result = db.get_artist_by_name(artist_name)
    if result is None:
        raise HTTPException(status_code=404, detail="Артист не найден")
    return result

@app.put("/change artist/{artist_name}", tags=['Исполнители'], summary='Поменять имя исполнителя')
def change_artist_name(artist_update: ArtistUpdate):
    result = db.update_artist_name(artist_update.old_name, artist_update.new_name)
    if result is None:
        raise HTTPException(status_code=404, detail="Артист не найден")
    elif result == "name_exists":
        raise HTTPException(status_code=400, detail="Новое имя уже занято")
    return result

@app.delete('/delete_artist/{artist_id}', tags=['Исполнители'], summary='Удалить исполнителя')
def remove_artist(artist_name: str):
    result = db.delete_artist(artist_name)
    if result is None:
        raise HTTPException(status_code=404, detail="Артист не найден")
    elif result == "has_songs":
        raise HTTPException(status_code=405, detail="Нельзя удалить артиста, у которого есть песни")
    return result

### Музыка ###

@app.post('/add_songs', tags=['Музыка'], summary='Добавить музыку')
def create_song(song: SongCreate):
    result = db.add_song(song)
    if result is None:
        raise HTTPException(status_code=404, detail="Артист не найден")
    return result

@app.get('/get_song', tags=['Музыка'], summary='Вся музыка')
def get_songs():
    return db.get_all_songs()

@app.get('/get_song/{song_id}', tags=['Музыка'], summary='Искать музыку')
def search_song(song_id: int):
    result = db.get_song_by_id(song_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Песня не найдена")
    return result

@app.delete('/songs/{song_id}', tags=['Музыка'], summary='Удалить музыку')
def remove_song(song_id: int):
    result = db.delete_song(song_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Песня не найдена")
    return result

### ПЛЕЙЛИСТЫ ###

@app.post("/playlists/", tags=['Плейлисты'], summary='Создать плейлист')
def new_playlist(playlist: PlaylistCreate):
    result = db.create_playlist(playlist)
    if result is None:
        raise HTTPException(status_code=400, detail="Плейлист с таким именем уже существует")
    return result

@app.post("/playlists/{playlist_id}/songs/", tags=['Плейлисты'], summary='Добавить музыку в плейлист')
def add_to_playlist_by_name(playlist_id: int, song_title: str, artist_name: str):
    result = db.add_song_to_playlist(playlist_id, song_title, artist_name)
    if result == "playlist_not_found":
        raise HTTPException(status_code=404, detail="Плейлист не найден")
    elif result == "artist_not_found":
        raise HTTPException(status_code=404, detail="Исполнитель не найден")
    elif result == "song_not_found":
        raise HTTPException(status_code=404, detail="Песня не найдена у этого исполнителя")
    elif result == "already_exists":
        raise HTTPException(status_code=400, detail="Песня уже есть в плейлисте")
    return result

@app.delete("/playlists/{playlist_id}/songs/{song_id}/", tags=['Плейлисты'], summary='Удалить музыку с плейлиста')
def remove_from_playlist(playlist_id: int, song_id: int):
    result = db.remove_song_from_playlist(playlist_id, song_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Песня в плейлисте не найдена")
    return result

@app.delete("/playlists/{playlist_id}/", tags=['Плейлисты'], summary='Удалить плейлист')
def remove_playlist(playlist_id: int):
    result = db.delete_playlist(playlist_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Плейлист не найден")
    elif result == "not_empty":
        raise HTTPException(status_code=405, detail="Нельзя удалить непустой плейлист")
    return result