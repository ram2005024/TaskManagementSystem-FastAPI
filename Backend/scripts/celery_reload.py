import subprocess

from watchfiles import run_process


def start_worker():
    subprocess.run(
        [
            "uv",
            "run",
            "celery",
            "-A",
            "app.core.celery.celery_app",
            "worker",
            "-l",
            "info",
        ]
    )


if __name__ == "__main__":
    run_process(
        "/code",
        target=start_worker,
        watch_filter=None,
    )
