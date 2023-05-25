# SHORTCUTS 

You can access all the shortcuts selecting “Tools” → “Keyboard Shortcuts”.

But here is a selection of my top 5:

Undo last action (inside a cell): ctrl + m + z

Find and replace: ctrl + m + h

Insert code cell above: ctrl + m + a

Insert code cell below: ctrl + m + b

Delete cell: ctrl + m + d

Be sure to check out other shortcuts and customize your favourite ones!

MOUNT YOUR GOOGLE DRIVE TO COLAB

from google.colab import drive

drive.mount('/content/gdrive')

The cell will return the following:

Click on the link, give Google Colab access to your Drive, and retrieve the authorization code. Paste it, and you’re done!

You are now able to access your Google Drive files under:

/content/gdrive/My Drive/

Use the batch comand !cd or the “Files” panel on the left.

RUN BASH COMMANDS

Bash commands can be run by prefixing the command with ‘!’.

Download dataset from the web with:

!wget <ENTER URL>

Install libraries with:

!pip install <LIBRARY>or !apt-get install <LIBRARY>

Run an existing .py script with:

!python script.py

Clone a git repository with:

!git clone <REPOSITORY URL>

UPLOAD / DOWNLOAD FILES

To upload a file (or several) from your computer, run:

from google.colab import files

files.upload()

To download a file, run:

from google.colab import files

files.download('path/to/your/file')

Another way to do this is to use the file explorer on the left panel, with drags & drops.

⚠️ Be aware the files will disapear as soon as you leave Google Colab.

ACTIVATE GPU AND TPU

The default hardware of Google Colab is CPU. However you can enable GPU (and even TPU) support for more computationally demanding tasks like Deep Learning.

Click on: “Runtime” → “Change runtime type” → “Hardware accelerator”. Then select the desired hardware.

You can easily check if the GPU is enabled by executing the following code:

import tensorflow as tf

tf.test.gpu_device_name()

LINK COLAB TO GITHUB

Open a GitHub file under Colab:

To open a notebook hosted on GitHub, there are 3 options:

Go to https://colab.research.google.com switch to the GitHub tab and enter the URL of the notebook

The notebook carries an “Open in Colab” badge, which allows you to open it directly on Google Colab.

The markdown code to insert into the README.md file is:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/googlecolab/colabtools/blob/master/notebooks/colab-github-demo.ipynb)

Use “Open in Colab” Chrome extension. After installation, whenever you find a Jupyter notebook in GitHub, click the icon of the plugin and it will open in Colab.

Save a Colab notebook in a GitHub repository:

Follow: “File” → “Save a copy in GitHub”. Once that is clicked it will ask for the authorization of your git account. Finally, you will be able to save the collaboratory notebook into the repository of your choice.

STOP COLAB FROM DISCONNECTING

Disconnection due to idleness:

This is a big drawback of Google Colab, and I’m sure a lot of you encountered this issue at least once. You decide to take a break, but when you’re back your notebook is disconnected!

Actually, Google Colab automatically disconnects the notebook if we leave it idle for more than 30 minutes. 🕑

Open your Chrome DevTools by pressing F12 or ctrl+shift+i on Linux and enter the following JavaScript snippet in your console:

function KeepClicking(){

console.log("Clicking");

document.querySelector("colab-connect-button").click()

}

setInterval(KeepClicking,60000)

This function makes a click on the connect-button every 60 seconds. Thus, Colab thinks that the notebook is not idle and you don’t have to worry about being disconnected!

Disconnection while a task is running:

First, be aware that when you connect to a GPU, you are given a maximum of 12 hours at a time on the Cloud Machine.

Sometimes it happens that you’re being disconnected, even within this 12-hour time lapse. As explained in Colab’s FAQ: “Colaboratory is intended for interactive use. Long-running background computations, particularly on GPUs, may be stopped.” 😕

DISPLAY DATAFRAMES AS INTERACTIVE TABLES

Colab includes an extension that renders pandas dataframes into interactive tables that can be filtered, sorted, and explored dynamically.

Enable this extension with %load_ext google.colab.data_table and disable it with:

 %unload_ext google.colab.data_table

USE TENSORBOARD WITH COLAB

TensorBoard is a tool for providing the measurements and visualizations needed during a Deep Learning workflow. It can be used directly within Colab. 📉 📈

Start by loading the TensorBoard notebook extension:

%load_ext tensorboard

Once your model is created, start TensorBoard within the notebook using:

%tensorboard --logdir logs

For more details, please check the Tensorflow tutorial on that topic.

CHANGE DISPLAY MODE

Dark mode: a lot of people prefer this mode because is more relaxing for their eyes. You can activate it following “Tools” → “Settings” → “Theme”
