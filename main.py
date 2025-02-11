from fastapi import FastAPI, HTTPException
import schemas as sch
import database as db

app = FastAPI()

## Исполнители ##

@app.get('/get_artist', tags=['Исполнители'], summary='Все исполнители')
def get_artist():
    return db.artists

@app.get('/get_artist/{artist_id}', tags=['Исполнители'], summary='Искать исполнителя')
def get_exact_artist(artist_id: int):
    for artist in db.artists:
        if artist['id'] == artist_id:
            return artist
    raise HTTPException(status_code=404, detail="Исполнитель не найден")

@app.post('/add_artists', tags=['Исполнители'], summary='Добавить исполнителя')
def add_artist(new_artist: sch.NewArtist):
    db.artists.append({
        'id': len(db.artists) + 1,
        'name': new_artist.artist_name,
    })
    return {'message': 'Исполнитель успешно добавлен'}

## Музыка ##

@app.get('/get_song', tags=['Музыка'], summary='Вся музыка')
def get_song():
    return db.songs

@app.get('/get_song/{song_id}', tags=['Музыка'], summary='Искать музыку')
def get_exact_song(song_id: int):
    for song in db.songs:
        if song['id'] == song_id:
            return song
    raise HTTPException(status_code=404, detail="Песня не найдена")

@app.post('/add_songs', tags=['Музыка'], summary='Добавить музыку')
def add_song(new_song: sch.NewSong):
    if new_song.artist in db.artists[0].values():
        db.songs.append({
            'id': len(db.songs) + 1,
            'name': new_song.title,
            'artist': new_song.artist
        })
        return {'message':'Песня успешно добавлена'}
    raise HTTPException(status_code=404, detail="Исполнитель не найден")

@app.delete('/songs/{song_id}', tags=['Музыка'], summary='Удалить музыку')
def delete_song(song_id: int):
    if song_id not in db.songs[0].values():
        raise HTTPException(status_code=404, detail="Песня не найдена")

    deleted_song = db.songs[0].pop(song_id)
    return {'message': 'Песня удалена', 'song': deleted_song}