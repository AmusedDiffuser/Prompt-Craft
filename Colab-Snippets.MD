# Colab Snippets 

link gdrive and test link:


```
#Start by connecting gdrive into the google colab

from google.colab import drive

drive.mount('/content/gdrive')

#Specify the path of the folder where you want to save the file

folder_path = "/content/gdrive/MyDrive/test_folder"

#Create the folder if it does not exist

import os

if not os.path.exists(folder_path):

  os.makedirs(folder_path)

#Write a short text file and save it into the folder

file_path = os.path.join(folder_path, "test_file.txt")

with open(file_path, "w") as f:

  f.write("This is a test file.")

#Read the contents of the text file to confirm that everything is working

with open(file_path, "r") as f:

  print(f.read())

```

Here is another code block that has two user adjustable variables, one to specify the source folder, and the other to specify a destination folder in the connected google drive. When you run this code block, it will copy any contents from the source folder to the specified destination folder:

```
#Specify the source and destination folders

source_folder = "/content/gdrive/MyDrive/test_folder"

destination_folder = "/content/gdrive/MyDrive/copy_folder"

#Create the destination folder if it does not exist

import os

if not os.path.exists(destination_folder):

  os.makedirs(destination_folder)

#Copy any contents from the source folder to the destination folder

import shutil

for file_name in os.listdir(source_folder):

  source_file = os.path.join(source_folder, file_name)

  destination_file = os.path.join(destination_folder, file_name)

  shutil.copy(source_file, destination_file)

```


