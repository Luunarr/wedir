import os
import curses
import shutil
import socket

def drw(win, dir, fls, sel, off):
    win.clear()
    hgt, wth = win.getmaxyx()

    lg = os.getlogin()
    hn = socket.gethostname()

    dD = dir.replace(os.environ['USERPROFILE'], '~')
    dD = (dD[:wth - 20] + "...") if len(dD) > wth - 20 else dD
    uI = f"({hn}@{lg}) Directory: "
    win.addstr(0, 0, "([r]-[n]-[d]) ([c]-[v]) ([g])", curses.color_pair(5))
    win.addstr(1, 0, uI, curses.color_pair(100))
    s = len(uI)
    win.addstr(1, s, dD, curses.color_pair(101))
    win.addstr(3, 0, "") 
    
    if not fls:
        win.addstr(2, 2, "🚫 No files or folders available.", curses.color_pair(1))
        win.refresh()
        return

    nC = 3
    cW = wth // nC
    vF = fls[off:off + (hgt - 4) * nC]

    for idx, f in enumerate(vF):
        r = (idx // nC) + 2
        c = (idx % nC) * cW
        
        clr, emo = gFci(f, dir)

        n = f"{emo} {f[:cW - 3]}"
        if os.path.isdir(os.path.join(dir, f)):
            n += "/"

        if idx + off == sel:
            win.addstr(r, c, n.ljust(cW - 1), curses.A_REVERSE | clr)
        else:
            win.addstr(r, c, n.ljust(cW - 1), clr)

    win.refresh()

def gFci(f, dir):
    fP = os.path.join(dir, f)
    
    hdn = f.startswith('.') or (os.path.isfile(fP) and os.stat(fP).st_file_attributes & 0x02)

    if f == "..":
        return curses.color_pair(24), "🔙"
    
    if hdn:
        return curses.color_pair(1), "👻"

    extm = {
        ('.txt', '.md', '.json', '.rst'): (3, "📄"),  
        ('.py', '.pyw'): (5, "🐍"),                  
        ('.jpg', '.jpeg', '.png', '.gif', '.svg', '.bmp', '.tiff'): (6, "🌆"),
        ('.mp4', '.mkv', '.avi', '.mov', '.flv', '.gif', '.webm'): (7, "🎬"), 
        ('.pdf',): (8, "📕"),               
        ('.zip', '.rar', '.tar', '.gz', '.bz2', '.7z', '.xz'): (9, "📦"),
        ('.exe', '.sh', '.msi', '.app', '.apk', '.bin'): (10, "💻"),
        ('.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'): (11, "🎵"),  
        ('.doc', '.docx', '.odt', '.rtf', '.tex'): (12, "📝"),
        ('.csv', '.xls', '.xlsx', '.ods'): (13, "📊"), 
        ('.ppt', '.pptx', '.odp', '.key'): (14, "📊"),  
        ('.html', '.htm', '.xhtml', '.xml'): (15, "🐘"),  
        ('.php', '.php3', '.php4', '.php5'): (18, "🔧"),
        ('.js', '.ts', '.jsx', '.tsx'): (19, "📜"),
        ('.css', '.scss', '.less'): (20, "🎨"),
        ('.sh', '.bash', '.zsh'): (10, "💻"), 
        ('.log', '.out'): (25, "📋"),
        ('.ttf', '.otf', '.woff', '.woff2'): (30, "🔤"),  
        ('.sql', '.sqlite', '.db', '.accdb'): (31, "💾"),
        ('.iso', '.img', '.vhd', '.vdi'): (32, "💿"),
        ('.msi', '.cab'): (33, "🖥️"),  
        ('.deb', '.rpm', '.pkg'): (34, "🐧"),  
        ('.yml', '.yaml', '.ini', '.cfg'): (35, "🦑"),  
        ('.dockerfile', '.container', '.tar.gz'): (36, "🐋"),  
        ('.venv', '.env'): (37, "📦"),  
        ('.crt', '.key', '.pem'): (38, "🔑"),  
        ('.pyc', '.pyo'): (39, "🐍"),  
        ('.bat', '.cmd'): (24, "🫀"),  
        ('.pcap', '.cap'): (40, "🛜"),  
        ('.rb'): (41, "💎"),
        ('.go'): (42, "🐹"),  
        ('.java', '.jar'): (43, "☕"),  
        ('.c', '.cpp', '.h'): (44, "🖥️"),  
        ('.rs'): (45, "🦀"),  
        ('.pl', '.pm'): (46, "🐫"),  
        ('.xml',): (47, "📂"),  
        ('.yaml', '.yml'): (48, "📝"),  
        ('.lua'): (49, "🌑"),  
        ('.xz', '.bz2'): (50, "📦")
    }

    if os.path.isdir(fP):
        return curses.color_pair(4), "📁"

    for exts, (clr, ico) in extm.items():
        if f.endswith(exts):
            return curses.color_pair(clr), ico

    return curses.color_pair(1), "👀"

def renf(dir, sel, win):
    curses.echo()
    win.addstr(curses.LINES - 2, 0, "Enter new name: ")
    nN = win.getstr(curses.LINES - 2, 17, 80).decode("utf-8").strip()
    curses.noecho()
    if nN:
        new_path = os.path.join(dir, nN)
        if not os.path.exists(new_path):
            os.rename(os.path.join(dir, sel), new_path)
        else:
            win.addstr(curses.LINES - 2, 0, "Error: File already exists!       ")

def opn(sel):
    os.startfile(os.path.normpath(sel))

def mgr(win):
    curses.start_color()

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(10, curses.COLOR_YELLOW, curses.COLOR_BLACK)
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
    curses.init_pair(100, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(101, curses.COLOR_RED, curses.COLOR_WHITE)

    curses.curs_set(0)

    dir = os.environ['USERPROFILE']
    sel = 0
    off = 0
    clip = None 
    while True:
        try:
            fls = os.listdir(dir)
        except PermissionError:
            dir = os.path.dirname(dir)
            continue

        fls.insert(0, "..")
        tF = len(fls)
        sel = min(sel, tF - 1)

        drw(win, dir, fls, sel, off)

        k = win.getch()

        if k == curses.KEY_DOWN:
            sel += 3
            if sel >= tF:
                sel = tF - 1
            if sel >= off + (curses.LINES - 4) * 3:
                off += 1

        elif k == curses.KEY_UP:
            sel -= 3
            if sel < 0:
                sel = 0
            if sel < off:
                off = max(0, off - 1)

        elif k == curses.KEY_RIGHT:
            sel = min(sel + 1, tF - 1)

        elif k == curses.KEY_LEFT:
            sel = max(sel - 1, 0)

        elif k == ord('\n'):
            selF = fls[sel]
            selP = os.path.join(dir, selF)
            if selF == "..":
                dir = os.path.dirname(dir)
                sel, off = 0, 0
            elif os.path.isdir(selP):
                dir = selP
                sel, off = 0, 0
            elif os.path.isfile(selP):
                opn(selP)

        elif k == ord('r'):
            selF = fls[sel]
            renf(dir, selF, win)

        elif k == ord('d'):
            selF = fls[sel]
            selP = os.path.join(dir, selF)
            win.addstr(curses.LINES - 2, 0, "Delete? (y/n): ")
            cf = win.getch()
            if cf == ord('y'):
                if os.path.isfile(selP):
                    os.remove(selP)
                elif os.path.isdir(selP):
                    shutil.rmtree(selP)
                else:
                    win.addstr(curses.LINES - 2, 0, "Error: Item does not exist!       ")

        elif k == ord('n'):
            win.addstr(curses.LINES - 2, 0, "Folder name: ")
            curses.echo()
            nF = win.getstr(curses.LINES - 2, 12, 80).decode("utf-8").strip()
            curses.noecho()
            if nF:
                new_folder_path = os.path.join(dir, nF)
                if not os.path.exists(new_folder_path):
                    os.mkdir(new_folder_path)
                else:
                    win.addstr(curses.LINES - 2, 0, "Error: Folder already exists!      ")

        elif k == ord('c'):
            selF = fls[sel]
            clb = os.path.join(dir, selF)

        elif k == ord('v') and clb:  
            dest_path = os.path.join(dir, os.path.basename(clb))
            if os.path.isfile(clb):
                if not os.path.exists(dest_path):
                    shutil.copy(clb, dir)
                else:
                    win.addstr(curses.LINES - 2, 0, "Error: File already exists in destination!    ")
            else:
                if not os.path.exists(dest_path):
                    shutil.copytree(clb, dest_path)
                else:
                    win.addstr(curses.LINES - 2, 0, "Error: Directory already exists in destination!    ")

        elif k == ord('g'):
            win.addstr(curses.LINES - 2, 0, "Drive letter (C, D, etc.): ")
            curses.echo()
            drv = win.getstr(curses.LINES - 2, 28, 5).decode("utf-8").strip().upper()
            curses.noecho()
            if drv:
                new_dir = f"{drv}:\\"
                if os.path.exists(new_dir):
                    dir = new_dir
                    sel, off = 0, 0
                else:
                    win.addstr(curses.LINES - 2, 0, "Error: Drive does not exist!      ")

        elif k == ord('q'): 
            break
        
def run():
    curses.wrapper(mgr)

if __name__ == "__main__":
    run()
