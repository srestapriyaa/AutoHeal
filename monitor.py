
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime
import urllib.request
import urllib.error

HEALTH_URL = "http://127.0.0.1:8000/health"
APP_FILE = Path(__file__).with_name("app.py")
LOG_FILE = Path(__file__).with_name("recovery.log")

CHECK_INTERVAL = 5
STARTUP_TIMEOUT = 10
RESTART_DELAY = 2


def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}"
    print(entry, flush=True)

    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(entry + "\n")


def check_health():
    try:
        with urllib.request.urlopen(HEALTH_URL, timeout=2) as response:
            return response.status == 200
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def start_application():
    if not APP_FILE.exists():
        log_event("ERROR: app.py was not found.")
        return None

    try:
        process = subprocess.Popen(
            [sys.executable, str(APP_FILE)],
            cwd=str(APP_FILE.parent)
        )
        log_event(f"Application started. PID: {process.pid}")
        return process
    except OSError as error:
        log_event(f"ERROR: Could not start application: {error}")
        return None


def wait_for_health(process, timeout):
    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:
        if process.poll() is not None:
            log_event("Application process exited unexpectedly.")
            return False

        if check_health():
            return True

        time.sleep(1)

    return check_health()


def main():
    log_event("AutoHeal monitoring started.")
    app_process = None

    try:
        while True:
            # Restart only when our managed application process has exited.
            if app_process is None or app_process.poll() is not None:
                if app_process is not None:
                    log_event("UNHEALTHY: Application process has exited.")

                if check_health():
                    log_event(
                        "An application is already responding on port 8000."
                    )
                    time.sleep(CHECK_INTERVAL)
                    continue

                log_event("Starting application.")
                app_process = start_application()

                if app_process is None:
                    time.sleep(RESTART_DELAY)
                    continue

                if wait_for_health(app_process, STARTUP_TIMEOUT):
                    log_event("RECOVERY SUCCESS: Application is healthy.")
                else:
                    log_event("Application failed to become healthy.")

                    # Do not start another copy while this process is alive.
                    if app_process.poll() is None:
                        app_process.terminate()
                        try:
                            app_process.wait(timeout=3)
                        except subprocess.TimeoutExpired:
                            app_process.kill()
                            app_process.wait()

                    app_process = None
                    time.sleep(RESTART_DELAY)
                    continue

            if check_health():
                log_event("HEALTHY: Application is responding.")
            else:
                log_event(
                    "UNHEALTHY: Application process is alive, "
                    "but the health endpoint is not responding."
                )
                # Avoid spawning a duplicate process while the old one lives.

            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        log_event("AutoHeal monitoring stopped.")

    finally:
        if app_process is not None and app_process.poll() is None:
            app_process.terminate()
            try:
                app_process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                app_process.kill()
                app_process.wait()


if __name__ == "__main__":
    main()
