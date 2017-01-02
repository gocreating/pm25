import sys
import logging
import glob
import os
import pandas as pd
import numpy as np

DEFAULT_SRC_DIR = '../../data/pm25/csvs'
DEFAULT_DEST_DIR = '../../data/pm25/reducedCsvs'
INPUT_CSV_COLUMNS = ['latitude', 'longitude', 'pm25', 'timestamp']
OUTPUT_CSV_COLUMNS = ['latitude', 'longitude', 'pm25', 'timestamp']

def main():
    srcDir = DEFAULT_SRC_DIR
    destDir = DEFAULT_DEST_DIR
    if len(sys.argv) <= 1:
        logging.warning('missing source dir')
    elif len(sys.argv) <= 2:
        srcDir = sys.argv[1]
        logging.warning('missing destination dir')
    else:
        destDir = sys.argv[2]
    logging.info(
        'using source dir: %s, destination dir: %s' % (srcDir, destDir)
    )

    filenames = glob.glob(os.path.join(srcDir, '*.csv'))
    for filename in filenames:
        logging.info('parsing ' + filename + '...')

        df = pd.read_csv(
            filename,
            dtype={
                'latitude': np.float64,
                'longitude': np.float64,
            },
            skiprows=1,
            names=INPUT_CSV_COLUMNS
        )
        df = df[
            (df['latitude'] > 21.543543) & (df['longitude'] > 119.382273) &
            (df['latitude'] < 25.711060) & (df['longitude'] < 122.567674)
        ]
        df.to_csv(
            os.path.join(destDir, os.path.basename(filename)),
            index=False,
            columns=OUTPUT_CSV_COLUMNS
        )
        df.to_csv(
            os.path.join(destDir, '../reducedCsvs.csv'),
            mode='a',
            index=False,
            columns=OUTPUT_CSV_COLUMNS
        )

main()
