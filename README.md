# VoxTune
VoxTune is a Voice Automated Music Player that is just like any other default music play in android phone's, but only here, all the operations could be performed manually as well as by vocal commands.

All files are uploaded together in here but while uploading this project to your project folder you need to organise everything as follows:
Your project structure should look something like this:

VoxTune

├── core

│   ├── audio_player.py

│   ├── favorites_manager.py

│   ├── library_manager.py

│   ├── playlist_manager.py

│   └── utils.py

├── data

│   └── app_data.json

├── ui

│   ├── albums_page.py

│   ├── components.py

│   ├── favorites_page.py

│   ├── main_window.py

│   ├── playlists_page.py

│   └── theme.py

├── voice

│   ├── commands.py

│   └── voice_assistant.py

├── main.py

└── requirements.txt

VoxTune is the main project folder, core,data,ui,voice are the respective packages for their respective code files as given.
The main.py file is the one you have to execute while the requirements.txt has the packages you might need for this project.
once the requirements file is copied in your directory, simply head towards your terminal and:

pip install -r requirements.txt

keep the app_data.json file empty as all your songa data will be automatically pasted there.
The project is still in progress so stay tuned for any more updates.( if any file isn't yet uploaded, it will be uploaded soon)
