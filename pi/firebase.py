from firebase_admin import credentials, db, initialize_app, delete_app
import threading

class FirebaseHelper:
    def __init__(self, key_path, db_url):
        """Initializes Firebase with the given service account key and DB URL."""
        self.cred = credentials.Certificate(key_path)
        self.app = initialize_app(
            self.cred,
            {'databaseURL': db_url},
            name="smart_lab_app"
        )
        self.root_ref = db.reference('/', app=self.app)
        self._listener = None
        self._listener_thread = None
        print("[INFO] FirebaseHelper initialized.")

    def set_value(self, path, value):
        self.root_ref.child(path).set(value)
        print(f"[INFO] Set {path} = {value}")

    def update_value(self, path, value):
        self.root_ref.child(path).update(value)
        print(f"[INFO] Updated {path} with {value}")

    def get_value(self, path):
        return self.root_ref.child(path).get()

    def delete_value(self, path):
        self.root_ref.child(path).delete()
        print(f"[INFO] Deleted {path}")

    def listen(self, path, callback):
        """Attach a Firebase real-time database listener to a specific path."""
        ref = self.root_ref.child(path)

        def _wrapped_callback(event):
            # event has properties: event.event_type, event.path, event.data
            print(f"[EVENT] Type: {event.event_type}, Path: {event.path}")
            callback(event)

        self._listener = ref.listen(_wrapped_callback)
        print(f"[INFO] Listening to changes on '{path}' using built-in Firebase listener.")

    def stop_listener(self):
        """Stops the Firebase real-time listener."""
        if self._listener:
            self._listener.close()
            self._listener = None
            print("[INFO] Firebase listener stopped.")

    def __del__(self):
        """Clean up and close Firebase app and listener."""
        self.stop_listener()
        try:
            delete_app(self.app)
            print("[INFO] Firebase app deleted.")
        except Exception as e:
            print(f"[ERROR] Failed to delete Firebase app: {e}")


# Example usage
if __name__ == "__main__":
    def handle_update(event):
        print("[CALLBACK] New update received:", event.data)

    fb = FirebaseHelper(
        key_path="key.json",
        db_url="https://your-project-id.firebaseio.com"
    )

    fb.set_value('lab1/test', {'voltage': 230})
    fb.listen('lab1/test', handle_update)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n[EXIT] KeyboardInterrupt received")

    del fb
