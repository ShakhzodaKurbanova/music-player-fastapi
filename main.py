from fastapi import FastAPI, HTTPException
import schemas

app = FastAPI()

songs = [
    {
        "id": 1,
        "title": "Батареи",
        "artist": "Нервы"
    }
]

artists = [
    {
        "id": 2,
        "name": "Сергей",
        "surname": "Лазарев"
    }
]

@app.get('/get_song', tags=['Музыка'], summary='Вся музыка')
def get_song():
    return songs

@app.get('/get_song/{song_id}', tags=['Музыка'], summary='Искать музыку')
def get_exact_song(song_id: int):
    for song in songs:
        if song['id'] == song_id:
            return song
    raise HTTPException(status_code=404, detail="Песня не найдена")

@app.get('/get_artist', tags=['Исполнители'], summary='Все исполнители')
def get_artist():
    return artists

@app.get('/get_artist/{artist_id}', tags=['Исполнители'], summary='Искать исполнителя')
def get_exact_artist(artist_id: int):
    for artist in artists:
        if artist['id'] == artist_id:
            return artist
    raise HTTPException(status_code=404, detail="Исполнитель не найден")

@app.post('/add_songs', tags=['Музыка'], summary='Добавить музыку')
def add_song():
    return songs

