import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def get_liked_songs():
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
            scope="user-library-read",
        )
    )

    results = []
    offset = 0
    limit = 50

    while True:
        response = sp.current_user_saved_tracks(limit=limit, offset=offset)
        if not response["items"]:
            break
        for item in response["items"]:
            track = item["track"]
            results.append(
                {
                    "name": track["name"],
                    "artist": track["artists"][0]["name"],
                    "album": track["album"]["name"],
                    "added_at": item["added_at"],
                    "spotify_url": track["external_urls"]["spotify"],
                }
            )

        offset += limit

    return results


def main():
    liked_songs = get_liked_songs()

    print(f"Found {len(liked_songs)} liked songs:")
    for song in liked_songs:
        print(f"- {song['name']} by {song['artist']} ({song['album']})")


if __name__ == "__main__":
    main()
