import os
import inspect

def main():
    fileName = ""

    for frame in inspect.stack()[1:]:
        if frame.filename[0] != '<':
            fileName = os.path.split(frame.filename)[1][:-3]
            break

    twitURL = "https://twitter.com/DragMine149"
    youURL = "https://youtube.com/channel/UCOnORrEI4GhYtivLQJpOoJQ"

    # Prints off my watermark

    print("\x1b[2J\x1b[H", end='')
    print("""{}
{} made by dragmine149 ('\u001b]8;;{}\u001b\\Twitter\u001b]8;;\u001b\\', '\u001b]8;;{}\u001b\\Youtube\u001b]8;;\u001b\\')
{}""".format('-' * os.get_terminal_size().columns,
            fileName,
            twitURL,
            youURL,
            '-' * os.get_terminal_size().columns))
    
main()