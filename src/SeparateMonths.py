import os

import imageio
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.basemap import Basemap

from src.utils import mkdir_folder, get_month_digit_formatted

"""
This Class is used to generate a separate report for all months in the time frame given. For example if the given range
in the csv file is from Jan 2018 to Jun 2020 then it will create a separate image for Jan '18, Jan '19 and Jan '20,
and similarly for all other months.
"""


class SeparateMonths(object):

    def __init__(self, csv_path, shapefile_name, shapefile_path):
        try:
            self.bird_df = pd.read_csv(csv_path)
        except IOError:
            print("Error while reading your csv file. Make sure you have given the correct path for the file.")
        self.shapefile_path = shapefile_name
        self.shapefile_name = shapefile_path
        self.current_month = None
        self.current_month_name = None
        self.current_year = None
        self.bird_name = None
        self.column_length = None
        self.base_map = None
        self.image_paths = []
        os.chdir('..')
        self.current_dir = os.getcwd()

    def process_data(self):
        self.data_cleanup()
        self.data_visualization()

    def data_cleanup(self):
        self.bird_df.drop(
            ['TRIP COMMENTS', 'GLOBAL UNIQUE IDENTIFIER', 'LAST EDITED DATE', 'TAXONOMIC ORDER', 'CATEGORY',
             'SUBSPECIES COMMON NAME', 'SUBSPECIES SCIENTIFIC NAME', 'BREEDING BIRD ATLAS CODE',
             'BREEDING BIRD ATLAS CATEGORY', 'AGE/SEX', 'IBA CODE', 'BCR CODE', 'USFWS CODE', 'ATLAS BLOCK',
             'EFFORT DISTANCE KM', 'EFFORT AREA HA', 'NUMBER OBSERVERS', 'ALL SPECIES REPORTED',
             'GROUP IDENTIFIER', 'HAS MEDIA', 'APPROVED', 'REVIEWED', 'REASON', 'SPECIES COMMENTS', 'Unnamed: 46',
             'OBSERVER ID', 'SAMPLING EVENT IDENTIFIER', 'PROTOCOL TYPE', 'PROTOCOL CODE', 'PROJECT CODE',
             'DURATION MINUTES'], axis=1, inplace=True)
        self.bird_df.columns = self.bird_df.columns.str.replace(' ', '_')
        self.bird_df.sort_values(by=['OBSERVATION_DATE'], inplace=True)
        self.bird_df['OBSERVATION_DATETIME'] = pd.to_datetime(self.bird_df['OBSERVATION_DATE'])
        self.column_length = self.bird_df['OBSERVATION_DATETIME'].shape[0]
        self.current_year = self.bird_df['OBSERVATION_DATETIME'].iloc[0].year
        self.current_month = self.bird_df['OBSERVATION_DATETIME'].iloc[0].month
        self.current_month_name = self.bird_df['OBSERVATION_DATETIME'].iloc[0].month_name()
        self.bird_name = self.bird_df['COMMON_NAME'].iloc[0]

    def data_visualization(self):
        self.create_new_basemap()
        for i in range(self.column_length):
            year = self.bird_df['OBSERVATION_DATETIME'].iloc[i].year
            month = self.bird_df['OBSERVATION_DATETIME'].iloc[i].month
            month_name = self.bird_df['OBSERVATION_DATETIME'].iloc[i].month_name()
            if year == self.current_year and month == self.current_month:
                df_lon = self.bird_df['LONGITUDE'].iloc[i]
                df_lat = self.bird_df['LATITUDE'].iloc[i]
                lon, lat = self.base_map(df_lon, df_lat)
                self.base_map.plot(lon, lat, marker='o', markeredgewidth=0.001, markeredgecolor='k', ms="3.0",
                                   color='b')
            else:
                self.save_figure()
                self.current_year = year
                self.current_month = month
                self.current_month_name = month_name
                self.create_new_basemap()
        self.save_figure()
        self.generate_gif()

    def create_new_basemap(self):
        plt.figure(figsize=(8, 8))
        plt.annotate(str(self.bird_name) + " : " + str(self.current_month_name) + " " + str(self.current_year),
                     xy=(0, 1.05), xycoords='axes fraction')
        plt.annotate('Made with Github/BirdAnalytics', xy=(1, 0), xycoords='axes fraction', xytext=(-20, 0.5),
                     textcoords='offset pixels', horizontalalignment='right', verticalalignment='bottom',
                     fontsize=5)
        self.base_map = Basemap(lat_0=14.5, lon_0=76, llcrnrlon=73.5, llcrnrlat=11.5, urcrnrlon=79, urcrnrlat=18.7,
                                projection='lcc')
        self.base_map.fillcontinents(color='#D5D6D8')
        self.base_map.readshapefile(self.shapefile_path, self.shapefile_name)

    def save_figure(self):
        folder_name = self.current_dir + '/images/' + 'SeparateMonths- ' + str(self.bird_name)
        figure_name = folder_name + '/' + str(self.bird_name) + '-' + get_month_digit_formatted(
            str(self.current_month)) + str(self.current_year) + '.png'
        mkdir_folder(folder_name)
        plt.savefig(figure_name, bbox_inches='tight')
        self.image_paths.append(figure_name)
        plt.close('all')

    def generate_gif(self):
        folder_name = self.current_dir + '/gifs/' + 'SeparateMonths- ' + str(self.bird_name)
        gif_name = folder_name + '/' + str(self.bird_name) + '.gif'
        mkdir_folder(folder_name)
        images = []
        for image in self.image_paths:
            images.append(imageio.imread(image))
        imageio.mimsave(gif_name, images, fps=0.6)
