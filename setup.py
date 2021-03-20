import os
import git
import platform
import winshell
import win32com.client

desktop = winshell.desktop()

if platform.system() == 'Windows':
    appdata = os.environ.get('appdata')
    spacebattles = appdata+'/space-battles'
    try:
        git.Git(appdata).clone('https://github.com/manos00/space-battles')
    except git.exc.GitCommandError as g:
        if g:
            pass
    img = spacebattles+'/img'
    db = spacebattles+'/highscores'
    if os.path.exists(db):
        pass
    else:
        os.mkdir(db)
    path = os.path.join(desktop, 'SpaceBattles.lnk')
    target = f"{spacebattles}/informatik.exe"
    icon = f"{spacebattles}/img/spaceship.ico"
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.IconLocation = icon
    shortcut.save()
else:
    try:
        git.Git().clone('https://github.com/manos00/space-battles')
    except git.exc.GitCommandError as g:
        if g:
            pass
    img = '/img'
    db = '/highscores'
    if os.path.exists(db):
        pass
    else:
        os.mkdir(db)
