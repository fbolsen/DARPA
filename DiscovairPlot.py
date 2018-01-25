from glob import iglob
import os
import argparse
import pandas as pd



def get_csv_files(pth):

    # remove files with zero size and 'conflict' in filename
    # filenames with 'conflict' indicates sync problem with Tresorit
    # iglob returns iterator, glob.glob returns list
    file_list = [f for f in iglob(pth, recursive=True) if os.path.isfile(f) and
                 os.path.getsize(f) > 0 and 'conflict' not in f]

    return file_list

def decide_filetype(fname):
    with open(fname, encoding='utf-8') as f:
        firstNlines = f.readlines()[0:5]

        if firstNlines[0].find("Discovair") >= 0:  # file is detection log
            return 'detectionlog'
        elif firstNlines[0].find("Measurement") >= 0:  # file is gps track
            return 'gpstrack'
        else:
            return 'unknown'


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot Discovair Detections with GPS tracks")
    parser.add_argument("--folder", default="./Testfiles", help="Folder to parse for data files")
    args = parser.parse_args()

    rootdir = args.folder

    fileList = get_csv_files(rootdir + '/**/*.csv')
    df_files = pd.DataFrame()
    df_files['filename'] = fileList
    df_files['filetype'] = [decide_filetype(f) for f in fileList]


    print(fileList)