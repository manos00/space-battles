import os
import git
import platform

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
