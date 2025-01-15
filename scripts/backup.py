import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from datetime import datetime
import os


def backup_liked_songs():
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
            scope="user-library-read",
        )
    )

    all_tracks = []
    offset = 0
    limit = 50

    print("Starting backup of liked songs...")
    while True:
        response = sp.current_user_saved_tracks(limit=limit, offset=offset)
        if not response["items"]:
            break

        for item in response["items"]:
            track = item["track"]
            track_data = {
                "name": track["name"],
                "id": track["id"],
                "artists": [
                    {"name": artist["name"], "id": artist["id"]}
                    for artist in track["artists"]
                ],
                "album": {
                    "name": track["album"]["name"],
                    "id": track["album"]["id"],
                    "release_date": track["album"]["release_date"],
                },
                "duration_ms": track["duration_ms"],
                "popularity": track["popularity"],
                "explicit": track["explicit"],
                "spotify_url": track["external_urls"]["spotify"],
                "preview_url": track["preview_url"],
                "added_at": item["added_at"],
            }
            all_tracks.append(track_data)

        offset += limit
        print(f"Processed {len(all_tracks)} songs...")

    if not os.path.exists("spotify_backups"):
        os.makedirs("spotify_backups")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"spotify_backups/liked_songs_backup_{timestamp}.json"

    backup_data = {
        "backup_date": datetime.now().isoformat(),
        "total_tracks": len(all_tracks),
        "tracks": all_tracks,
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(backup_data, f, indent=2, ensure_ascii=False)

    print("\nBackup completed!")
    print(f"Total tracks backed up: {len(all_tracks)}")
    print(f"Backup saved to: {filename}")

    return filename


def verify_backup(filename):
    """Verify the backup file can be read and contains data"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        print("\nBackup verification:")
        print("✓ Backup file is valid JSON")
        print(f"✓ Contains {data['total_tracks']} tracks")
        print(f"✓ Backup date: {data['backup_date']}")
        return True
    except Exception as e:
        print(f"\nError verifying backup: {e}")
        return False


def main():
    backup_file = backup_liked_songs()
    verify_backup(backup_file)


if __name__ == "__main__":
    main()
