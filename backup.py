import os
import zmail
from contextlib import suppress

USERNAME = ""  # Your mail address.(required)
PASSWORD = ""  # Your mail password.(required)

backup_dir = '{}_backup/'.format(USERNAME)
persist_walk = True
walk_steps = 10
backup_walk_path = backup_dir + '_mail_walk.txt'

srv = zmail.server(USERNAME, PASSWORD)

mail_count, mail_size = srv.stat()

# Make directory if not exist.
with suppress(FileExistsError):
    os.mkdir(backup_dir)


# walk functions.
def get_walk():
    if os.path.exists(backup_walk_path):
        with open(backup_walk_path, mode='r') as f:
            _walk = int(f.read())
        return _walk
    return 1


def save_walk(_walk):
    with open(backup_walk_path, mode='w') as f:
        f.write(str(_walk))


def safe_str(o):
    if o is None:
        return ''
    s = str(o).replace('/', ':')
    return s


walk = get_walk() if persist_walk else 1
while walk <= mail_count:
    mails = srv.get_mails(start_index=walk, end_index=walk + walk_steps)
    for mail in mails:
        zmail.save(mail,
                   name=safe_str(mail['subject']) + ' ' + safe_str(mail['date']) + '.eml',  # Your mail name.
                   target_path=backup_dir,
                   overwrite=True)
        print('{} {} {}/{}'.format(mail['subject'], mail['date'], walk, mail_count))
        walk += 1
        if persist_walk:
            save_walk(walk)
