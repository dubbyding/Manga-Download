import os
class createDesktopShortcut:
    def __init__(self, givenFileName, executing_filename, logo_filename):
        '''
            givenFileName = Filename for the shortcut
            executing_filename = Filename with extension whose shortcut is being created
            logo_filename = Icon for the shortcut
        '''
        # Get Current Directory Location
        current_directory = os.path.abspath(os.getcwd())

        # Get Username
        username = current_directory.split('/')[2]

        # Desktop Location
        desktop_location = '/home/' + username + '/Desktop/'

        # FileName
        self.filename = givenFileName

        # Filename of desktop shortcut
        self.file = desktop_location + '/' + givenFileName + '.desktop'

        # Executing file
        self.executing_file = 'Exec= bash ' + current_directory + '/' + executing_filename + '\n'

        #Logo
        self.executing_filename_logo = 'Icon=' + current_directory + '/' + logo_filename +'\n'

    def create_desktop_shortcut(self):
        if not os.path.isfile(self.file):
            with open(self.file, "w") as f:
                f.writelines(["[Desktop Entry]\n",
                            "Name=" + self.filename + "\n", 
                            "Name[en_US]=" + self.filename + "\n",
                            "StartupNotify=true\n", 
                            "Terminal=true\n",
                            self.executing_file,
                            self.executing_filename_logo,
                            "Type=Application\n"])
            os.chmod(self.file, 0o777)

class createShFile:
    def __init__(self):
        # Get Current Directory Location
        current_directory = os.path.abspath(os.getcwd())

        #run.sh file
        file_name = os.path.join(current_directory, "run.sh")

        #env location

        with open(file_name,"w") as f:
            f.writelines(
                [
                    "#!/bin/sh\n",
                    'cd '+ current_directory +'\n',
                    'if [[ ! -d env ]] \n',
                    "then\n",
                    "\tpython3 -m venv env\n"
                    "fi\n",
                    'source env/bin/activate\n',
                    'pip3 install -r requirements.txt\n',
                    'clear\n',
                    'python3 animeDownload.py\n',

                ]
            )

if __name__=="__main__":
    createSh = createShFile()
    createShortcut = createDesktopShortcut("Manga Download","run.sh", "logo.png")
    createShortcut.create_desktop_shortcut()
            
