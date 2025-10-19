import os
import pathlib
import shutil


class Shorter:
    def __init__(self):
        pass
    
    def get_files(self) -> list:
        data = []

        files = os.listdir()
        for file in files:
            if os.path.isdir(file):
                continue
            
            ext = lambda name:(name.split('.')[-1] if len(name.split('.')) >= 2 else "None")
            data.append((file,ext(file)))
        
        return data
    
    def main(self) -> None:
        files = self.get_files()
        for file in files:
            name,ext = file
            dest_folder = ext.upper() + " Folder"
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
            
            moved = False
            n = 1
            while not moved:
                if os.path.exists(f'{dest_folder}/{name}'):
                    path = pathlib.Path(name)
                    _name = path.stem
                    _ext = path.suffix
                    new_name = path.rename(f'{_name}_{n}{_ext}')
                    name = new_name.name
                    n += 1
                    continue
                
                shutil.move(name,dest_folder)
                print(f'-> moving {name} to {dest_folder}')
                moved = True
                    

if __name__ == '__main__':
    s = Shorter()
    s.main()
    import os
import pathlib
import shutil


class Shorter:
    def __init__(self):
        pass
    
    def get_files(self) -> list:
        data = []

        files = os.listdir()
        for file in files:
            if os.path.isdir(file):
                continue
            
            ext = lambda name:(name.split('.')[-1] if len(name.split('.')) >= 2 else "None")
            data.append((file,ext(file)))
        
        return data
    
    def main(self) -> None:
        files = self.get_files()
        for file in files:
            name,ext = file
            dest_folder = ext.upper() + " Folder"
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
            
            moved = False
            n = 1
            while not moved:
                if os.path.exists(f'{dest_folder}/{name}'):
                    path = pathlib.Path(name)
                    _name = path.stem
                    _ext = path.suffix
                    new_name = path.rename(f'{_name}_{n}{_ext}')
                    name = new_name.name
                    n += 1
                    continue
                
                shutil.move(name,dest_folder)
                print(f'-> moving {name} to {dest_folder}')
                moved = True
                    

if __name__ == '__main__':
    s = Shorter()
    s.main()
    