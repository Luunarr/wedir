import os
import curses
import shutil

def draw(win, directory, files, selection, offset):
    win.clear()
    height, width = win.getmaxyx()

    dirDisplay = directory.replace(os.environ['USERPROFILE'], '~')
    dirDisplay = (dirDisplay[:width - 20] + "...") if len(dirDisplay) > width - 20 else dirDisplay
    win.addstr(0, 0, f"Dir: {dirDisplay}", curses.color_pair(5))

    if not files:
        win.addstr(2, 2, "🚫 No files or folders available.", curses.color_pair(1))
        win.refresh()
        return

    Ncols = 3
    colW = width // Ncols
    Vfiles = files[offset:offset + (height - 4) * Ncols]

    for idx, file in enumerate(Vfiles):
        row = (idx // Ncols) + 2
        col = (idx % Ncols) * colW
        
        color, emoji = getFileColorIcon(file, directory)

        name = f"{emoji} {file[:colW - 3]}"
        if os.path.isdir(os.path.join(directory, file)):
            name += "/"

        if idx + offset == selection:
            win.addstr(row, col, name.ljust(colW - 1), curses.A_REVERSE | color)
        else:
            win.addstr(row, col, name.ljust(colW - 1), color)

    win.refresh()

def getFileColorIcon(file, directory):
    file_path = os.path.join(directory, file)
    if file == "..":
        return curses.color_pair(2), "🔙"
    if os.path.isdir(file_path):
        return curses.color_pair(4), "📁"
    if file.endswith('.txt'):
        return curses.color_pair(3), "📄"  
    if file.endswith('.py'):
        return curses.color_pair(5), "🐍"  
    if file.endswith('.jpg') or file.endswith('.png'):
        return curses.color_pair(6), "🌆"  
    if file.endswith('.mp4') or file.endswith('.mkv'):
        return curses.color_pair(7), "🎬"  
    if file.endswith('.pdf'):
        return curses.color_pair(8), "📕" 
    if file.endswith('.zip') or file.endswith('.rar'):
        return curses.color_pair(9), "📦"  
    if file.endswith('.exe'):
        return curses.color_pair(10), "💻"  
    if file.endswith('.mp3') or file.endswith('.wav'):
        return curses.color_pair(11), "🎵"  
    if file.endswith('.doc') or file.endswith('.docx'):
        return curses.color_pair(12), "📝" 
    if file.endswith('.csv'):
        return curses.color_pair(13), "📊"  
    if file.endswith('.ppt') or file.endswith('.pptx'):
        return curses.color_pair(14), "📊"  
    if file.endswith('.html') or file.endswith('.htm'):
        return curses.color_pair(15), "🌐"  
    if file.endswith('.json'):
        return curses.color_pair(16), "📄"  
    if file.endswith('.gif'):
        return curses.color_pair(17), "🎥" 
    if file.endswith('.php'):
        return curses.color_pair(18), "🔧"  
    if file.endswith('.js'):
        return curses.color_pair(19), "📜"  
    if file.endswith('.css'):
        return curses.color_pair(20), "🎨" 
    if file.endswith('.sh'):
        return curses.color_pair(21), "💻" 
    if file.endswith('.svg'):
        return curses.color_pair(22), "🖼️" 
    if file.endswith('.md'):
        return curses.color_pair(23), "📜"  
    if file.endswith('.bat'):
        return curses.color_pair(24), "⚙️"
    if file.endswith('.log'):
        return curses.color_pair(25), "📋"
    if file.endswith('.apk'):
        return curses.color_pair(26), "📱"
    return curses.color_pair(1), "👀"

def renamef(directory, selected, win):
    curses.echo()
    win.addstr(curses.LINES - 2, 0, "Enter new name: ")
    new_name = win.getstr(curses.LINES - 2, 17, 80).decode("utf-8").strip()
    curses.noecho()
    if new_name:
        os.rename(os.path.join(directory, selected), os.path.join(directory, new_name))

def opene(selected):
    os.startfile(os.path.normpath(selected))

def manager(win):
    curses.start_color()

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(10, curses.COLOR_YELLOW, curses.COLOR_BLUE)
    curses.init_pair(11, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(12, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(13, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(14, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(15, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(16, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(17, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(18, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(19, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(20, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(21, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(22, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(23, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(24, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(25, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(26, curses.COLOR_CYAN, curses.COLOR_BLACK)

    curses.curs_set(0)

    directory = os.environ['USERPROFILE']
    selection = 0
    offset = 0

    while True:
        try:
            files = os.listdir(directory)
        except PermissionError:
            directory = os.path.dirname(directory)
            continue

        files.insert(0, "..")
        totalFiles = len(files)
        selection = min(selection, totalFiles - 1)

        draw(win, directory, files, selection, offset)

        key = win.getch()

        if key == curses.KEY_DOWN:
            selection += 3
            if selection >= totalFiles:
                selection = totalFiles - 1
            if selection >= offset + (curses.LINES - 4) * 3:
                offset += 1

        elif key == curses.KEY_UP:
            selection -= 3
            if selection < 0:
                selection = 0
            if selection < offset:
                offset = max(0, offset - 1)

        elif key == curses.KEY_RIGHT:
            selection = min(selection + 1, totalFiles - 1)

        elif key == curses.KEY_LEFT:
            selection = max(selection - 1, 0)

        elif key == ord('\n'):
            selected = files[selection]
            selectedPath = os.path.join(directory, selected)

            if selected == "..":
                directory = os.path.dirname(directory)
                selection = 0
                offset = 0
            elif os.path.isdir(selectedPath):
                directory = selectedPath
                selection = 0
                offset = 0
            elif os.path.isfile(selectedPath):
                os.startfile(selectedPath)

        elif key == ord('r'):
            selected = files[selection]
            renamef(directory, selected, win)

        elif key == ord('d'):
            selected = files[selection]
            selectedPath = os.path.join(directory, selected)
            confirm = win.getch()
            if confirm == ord('y'):
                os.remove(selectedPath) if os.path.isfile(selectedPath) else shutil.rmtree(selectedPath)

        elif key == ord('n'):
            win.addstr(curses.LINES - 2, 0, "Enter folder name: ")
            curses.echo()
            NFname = win.getstr(curses.LINES - 2, 20, 80).decode("utf-8").strip()
            curses.noecho()
            if NFname:
                os.mkdir(os.path.join(directory, NFname))

        elif key == ord('q'):
            break

def run():
    curses.wrapper(manager)

if __name__ == "__main__":
    run()
