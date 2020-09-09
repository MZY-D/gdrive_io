##!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import fnmatch
import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class DriveIO:
    def __init__(self, env="local", credential_path=None):
        """
        Get credentials to activate pydrive.

        Input :
            env : str
                "local" or "colab" are available. If you are in Google Colaboratory, then choose "colab", else choose "local".
            credential_path : str
                The directory of 'settinngs.yaml'('client_secrets.json') for GoogleDriveAPI.
        """
        if env == "local":
            current_dir = os.getcwd()
            os.chdir(credential_path)
            gauth = GoogleAuth()
            gauth.LocalWebserverAuth()
            self.drive = GoogleDrive(gauth)
            os.chdir(current_dir)
        elif env == "colab":
            from google.colab import auth
            from oauth2client.client import GoogleCredentials
            auth.authenticate_user()
            gauth = GoogleAuth()
            gauth.credentials = GoogleCredentials.get_application_default()
            self.drive = GoogleDrive(gauth)

    def driveCsv2df(self, folder_id, target_file, add_file_name=False):
        """
        Read CSV in GoogleDrive and return pandas DataFrame.

        Input :
            folder_id : str
                Folder id of GoogleDrive where target file is stored.
            target_file : str
                Target CSV file name. Wild card is available
            add_file_name : boolean
                If True, then out_df has "file_name" column to identify rows from which file.

        Return :
            out_df : pandas DataFrame
        """
        file_dict = self.driveDict(folder_id)
        out_df = pd.DataFrame()
        for f in fnmatch.filter(file_dict.keys(), target_file):
            print(f)
            exist_file = self.drive.CreateFile({'id': file_dict[f]})
            try:
                exist_file.GetContentFile("_tempDiriveIO_" + f, mimetype='text/csv')
                temp_df = pd.read_csv("_tempDiriveIO_" + f, header=0)
            except UnicodeEncodeError:
                exist_file.GetContentFile("_tempDiriveIO_" + f, mimetype='text/csv')
                temp_df = pd.read_csv("_tempDiriveIO_" + f, header=0, encoding="shift-jis")
            if add_file_name:
                temp_df["file_name"] = f
            else:
                pass
            out_df = out_df.append(temp_df)
            os.remove("_tempDiriveIO_" + f)
        return out_df

    def driveExcel2df(self, folder_id, target_file, sheet=0, skip_rows=0, add_file_name=False):
        """
        Read Excel in GoogleDrive and return pandas DataFrame.

        Input :
            folder_id : str
                Folder id of GoogleDrive where target file is stored.
            target_file : str
                Target Excel file name. Wild card is available
            sheet : str, int, list, or None, default 0
                Strings are used for sheet names. Integers are used in zero-indexed sheet positions.
                * https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html
            skip_rows : list-like
                Rows to skip at the beginning (0-indexed).
                * https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html
            add_file_name : boolean
                If True, then out_df has "file_name" column to identify rows from which file.

        Return :
            out_df : pandas DataFrame
        """
        file_dict = self.driveDict(folder_id)
        out_df = pd.DataFrame()
        for f in fnmatch.filter(file_dict.keys(), target_file):
            print(f)
            exist_file = self.drive.CreateFile({'id': file_dict[f]})
            exist_file.GetContentFile("_tempDiriveIO_" + f)
            temp_df = pd.read_excel("_tempDiriveIO_" + f, sheet, header=0, skiprows=skip_rows)
            if add_file_name:
                temp_df["file_name"] = f
            else:
                pass
            out_df = out_df.append(temp_df)
            os.remove("_tempDiriveIO_" + f)
        return out_df

    def driveSS2df(self, folder_id, target_file, index_col=None, header=0, skip_rows=0, add_file_name=False):
        """
        Read Spreadsheet in GoogleDrive via CSV format and return pandas DataFrame.

        Input :
            folder_id : str
                Folder id of GoogleDrive where target file is stored.
            target_file : str
                Target Spreadsheet file name. Wild card is available
            index_col : int, str, sequence of int / str, or False, default None
                Column(s) to use as the row labels of the DataFrame, either given as string name or column index.
                * https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
            header : int, list of int, default 0
                Row number(s) to use as the column names, and the start of the data.
                * https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
            skip_rows : list-like
                Rows to skip at the beginning (0-indexed).
                * https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
            add_file_name : boolean
                If True, then out_df has "file_name" column to identify rows from which file.

        Return :
            out_df : pandas DataFrame
        """
        file_dict = self.driveDict(folder_id)
        out_df = pd.DataFrame()
        for f in fnmatch.filter(file_dict.keys(), target_file):
            print(f)
            exist_file = self.drive.CreateFile({'id': file_dict[f]})
            exist_file.GetContentFile("_tempDiriveIO_" + f, mimetype='text/csv')
            temp_df = pd.read_csv("_tempDiriveIO_" + f, header=0, skiprows=skip_rows)
            if add_file_name:
                temp_df["file_name"] = f
            else:
                pass
            out_df = out_df.append(temp_df)
            os.remove("_tempDiriveIO_" + f)
        return out_df

    def driveSS2Excel2df(self, folder_id, target_file, sheet, index_col=None, skip_rows=0, add_file_name=False):
        """
        Read Spreadsheet in GoogleDrive via Excel format and return pandas DataFrame.

        Input :
            folder_id : str
                Folder id of GoogleDrive where target file is stored.
            target_file : str
                Target Spreadsheet file name. Wild card is available
            sheet : str, int, list, or None, default 0
                Strings are used for sheet names. Integers are used in zero-indexed sheet positions.
                * https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html
            index_col : int, str, sequence of int / str, or False, default None
                Column(s) to use as the row labels of the DataFrame, either given as string name or column index.
                * https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html
            skip_rows : list-like
                Rows to skip at the beginning (0-indexed).
                * https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html
            add_file_name : boolean
                If True, then out_df has "file_name" column to identify rows from which file.

        Return :
            out_df : pandas DataFrame
        """
        file_dict = self.driveDict(folder_id)
        out_df = pd.DataFrame()
        for f in fnmatch.filter(file_dict.keys(), target_file):
            print(f, " > ", sheet)
            exist_file = self.drive.CreateFile({'id': file_dict[f]})
            exist_file.GetContentFile("_tempDiriveIO_" + f + ".xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            input_book = pd.ExcelFile("_tempDiriveIO_" + f + ".xlsx")
            temp_df = input_book.parse(sheet, skiprows=skip_rows)
            if add_file_name:
                temp_df["file_name"] = f + ".xlsx"
            else:
                pass
            out_df = out_df.append(temp_df)
            os.remove("_tempDiriveIO_" + f + ".xlsx")
        return out_df

    def df2driveCsv(self, folder_id, file_name, df, index_bool=True, encode="utf-8"):
        """
        Upload CSV in GoogleDrive from pandas DataFrame.

        Input :
            folder_id : str
                Folder id of GoogleDrive where target file is stored.
            file_name : str
                Upload CSV file name.
            index_bool : boolean
                If False, then index of the dataframe will be skipped.
            encode : str
                Encoding option for the CSV file.

        Return :
            None
        """
        file_dict = self.driveDict(folder_id)
        if file_name in file_dict.keys():
            exist_file = self.drive.CreateFile({'id': file_dict[file_name]})
        else:
            exist_file = self.drive.CreateFile({'title': file_name, 'mimeType': 'text/csv', "parents": [{"kind": "drive#fileLink", "id": folder_id}]})
        exist_file.SetContentString(df.to_csv(index=index_bool, encoding=encode))
        exist_file.Upload()
        return None

    def excel2drive(self, folder_id, file_name, df=None, index_bool=True):
        """
        Upload Excel in GoogleDrive from local directory.

        Input :
            folder_id : str
                Folder id of GoogleDrive where target file is stored.
            file_name : str
                Upload Excel file name.
            df : pandas.dataframe
                If input , upload pandas dataframe as a Excel file.
            index_bool : boolean
                If False, then index of the dataframe will be skipped.
            encode : str
                Encoding option for the CSV file.

        Return :
            None
        """
        if df is not None:
            df.to_excel("_tempDiriveIO_" + file_name, index=index_bool)
        else:
            pass
        file_dict = self.driveDict(folder_id)
        if file_name in file_dict.keys():
            exist_file = self.drive.CreateFile({'id': file_dict[file_name]})
        else:
            exist_file = self.drive.CreateFile({'title': file_name, "parents": [{"kind": "drive#fileLink", "id": folder_id}]})
        if df is not None:
            exist_file.SetContentFile("_tempDiriveIO_" + file_name)
        else:
            exist_file.SetContentFile(file_name)
        exist_file.Upload()
        if df is not None:
            os.remove("_tempDiriveIO_" + file_name)
        else:
            pass
        return None

    def driveDict(self, folder_id):
        """
        File name and the ids in specific directory in GoogleDrive can be gotten.

        Input:
            folder_id : str
                Folder id of GoogleDrive where target file is stored.

        Output:
            file_dict : dict
                Dict of the file name and the ids in the directory.
        """
        file_list = self.drive.ListFile({'q': "'%s' in parents and trashed=false" % (folder_id)}).GetList()
        file_dict = {}
        for file in file_list:
            file_dict[file['title']] = file['id']
        return file_dict

    def driveText2Text(self, folder_id, target_file):
        """
        Test file in specific directory in GoogleDrive can be gotten.

        Input:
            folder_id : str
                Folder id of GoogleDrive where target file is stored.
            target_file : str
                Target text file name.

        Output:
            text : str
                The text string.
        """
        file_dict = self.driveDict(folder_id)
        exist_file = self.drive.CreateFile({'id': file_dict[target_file]})
        text = exist_file.GetContentString()
        return text
