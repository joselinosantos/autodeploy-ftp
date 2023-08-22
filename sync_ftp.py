import os
import time
from ftplib import FTP
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configurações de FTP
FTP_HOST = 'ip do servidor'
FTP_USER = 'usuario'
FTP_PASS = 'senha'
REMOTE_FOLDER = '/pasta_projeto_remota'
LOCAL_FOLDER = '/home/pasta_projeto'

# Upload do arquivo
def upload_file(file_path):
    with FTP(FTP_HOST) as ftp:
        ftp.login(FTP_USER, FTP_PASS)
        with open(file_path, 'rb') as file:
            remote_path = os.path.join(REMOTE_FOLDER, os.path.relpath(file_path, LOCAL_FOLDER))
            ftp.storbinary('STOR ' + remote_path, file)

# Monitora as mudanças nos arquivos locais
class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f'Arquivo modificado: {event.src_path}')
            upload_file(event.src_path)

# Inicia o monitoramento de mudanças
if __name__ == "__main__":
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, LOCAL_FOLDER, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

