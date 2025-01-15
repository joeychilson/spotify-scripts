import os
import time

import spotipy
from spotipy.oauth2 import SpotifyOAuth


def unlike_all_songs(confirm=True):
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
            scope="user-library-modify user-library-read",
        )
    )

    if confirm:
        total_tracks = sp.current_user_saved_tracks(limit=1)["total"]
        confirm_input = input(
            f"This will unlike {total_tracks} songs. Type 'CONFIRM' to proceed: "
        )
        if confirm_input != "CONFIRM":
            print("Operation cancelled.")
            return

    while True:
        results = sp.current_user_saved_tracks(limit=50)

        if not results["items"]:
            print("No more liked songs found.")
            break

        track_ids = [item["track"]["id"] for item in results["items"]]

        try:
            sp.current_user_saved_tracks_delete(tracks=track_ids)
            print(f"Unliked {len(track_ids)} songs...")

            time.sleep(1)
        except Exception as e:
            print(f"Error unliking tracks: {e}")
            break


def main():
    unlike_all_songs()
    print("Operation completed.")


if __name__ == "__main__":
    main()
