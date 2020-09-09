# Gdrive_IO
## Introduction

Easy to input files on GoogleDrive as pandas DataFrame fortmat and output(upload) DataFrames onto GoogleDrive powered by Pandas and Pydrive. If you use Google Colaboratory, it's easier to set up auth than your local Jupyter notebook.

- You can get pandas dataframe from files on the Google drive as below.
  - CSV
  - Excel
  - Spreadsheet
- You can upload your pandas dataframe onto the Google drive as format you like as below.
  - CSV
  - Excel
- You can get file id dict in the specific google drive directory. This is useful to read multiple files.

## How to use

### Local Jupyter notebook

```
pip install git+https://github.com/mi-ta-d/gdrive_io
```

```python
import gdrive_io

drive = gdrive_io.DriveIO(env="local", "xxx")  # Your credentials path for GoogleDrive (https://pythonhosted.org/PyDrive/quickstart.html)
drive_dir_id = "aaaaa"  # Id of the Google Drive directory where your CSV is.
df = drive.driveCsv2df(drive_dir_id,"file_name.csv")
```

### Google Colaboratory

```python
!pip install git+https://github.com/mi-ta-d/gdrive_io
import gdrive_io

drive = gdrive_io.DriveIO(env="colab")
drive_dir_id = "aaaaa"  # Id of the Google Drive directory where your CSV is.
df = drive.driveCsv2df(drive_dir_id,"file_name.csv")
```



