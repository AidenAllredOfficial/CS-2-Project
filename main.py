#! ./venv/bin/python3
# This is the main file for the project.

### Imports

import tsapp


def main():
    window = tsapp.GraphicsWindow()

    while window.is_running:
        window.finish_frame()


if __name__ == "__main__":
    main()
