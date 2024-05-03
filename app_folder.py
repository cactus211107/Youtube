import os
def get_docs_folder():return os.path.expanduser("~/Documents")
def getAppFolder():return os.path.join(get_docs_folder(),'YoutubeDownloader')
def getInsideAppFolder(folder):return os.path.join(getAppFolder(),folder)
def create_folder_in_documents(folder_name):
    # Get the user's documents folder
    documents_folder = get_docs_folder()

    # Construct the full path to the new folder
    new_folder_path = os.path.join(documents_folder, folder_name)

    # Create the folder if it doesn't exist
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        print(f"Folder '{folder_name}' created in {documents_folder}")
    else:
        print(f"Folder '{folder_name}' already exists in {documents_folder}")
def create_app_folder():
    create_folder_in_documents('YoutubeDownloader')
    create_folder_in_documents('YoutubeDownloader/temp')
def addFileToFolder(path_in_folder):
    with open(os.path.join(getAppFolder(),path_in_folder),'r+') as f:
        pass
def getPathInAppFolder(*paths,filename=''):
    return os.path.join(os.path.join(getAppFolder(),*paths),filename)
def pathJoin(path,*paths):
    return os.path.join(path,*paths)