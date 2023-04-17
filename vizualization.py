import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table


def open_generation_dir(path):
    data = []
    with open(path, 'r') as csvfile:
        #csvreader = csv.DictReader(csvfile)
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            data.append(row[1:])
    #data = pd.read_csv(path)
    #data = data.iloc[: , 1:]
    return data[1:]

def prepare_table(path, generation, data, color):

    f = plt.figure(figsize=(10,10))
    f.suptitle(generation, fontsize=30)

    ax1 = plt.subplot(121, frame_on=False) # no visible frame
    hard_hand = table(ax1, data['hard_hand'], loc='center', cellColours=color['hard_hand'], cellLoc='center', colWidths=[.05]*10)
    ax2 = f.add_subplot(222, frame_on=False) # no visible frame
    soft_hand = table(ax2, data['soft_hand'], loc='center', cellColours=color['soft_hand'], cellLoc='center', colWidths=[.05]*10)
    ax3 = f.add_subplot(224, frame_on=False, ) # no visible frame
    pair = table(ax3, data['pair'], loc='center', cellColours=color['pair'], cellLoc='center', colWidths=[.05]*10)

    ax1.set_title('Hard hand',fontsize = 25)
    ax2.set_title('Soft hand', fontsize = 25)
    ax3.set_title('Pair', fontsize = 25, pad=30)

    ax1.get_xaxis().set_visible(False)
    ax1.get_yaxis().set_visible(False)
    ax2.get_xaxis().set_visible(False)
    ax2.get_yaxis().set_visible(False)
    ax3.get_xaxis().set_visible(False)
    ax3.get_yaxis().set_visible(False)

    hard_hand.set_fontsize(16)
    hard_hand.scale(2,2.5)
    soft_hand.set_fontsize(16)
    soft_hand.scale(2,2)
    pair.set_fontsize(16)
    pair.scale(2,2)

    plt.savefig(path)
    plt.savefig('Tables/'+dir+'.png')
    plt.close('all')

def to_dataframe(data, column_name, row_name):
    data_df = []
    data_color = []
    for i in range(0, len(data)):
        data_df.append([])
        data_color.append([])
        for j in range(0, len(data[i])):
            if data[i][j] == 'Move.STAND':
                data_df[i].append('S')
                data_color[i].append('#ff6666')
            elif data[i][j] == 'Move.HIT':
                data_df[i].append('H')
                data_color[i].append('#66ff33')
            elif data[i][j] == 'Move.DOUBLE':
                data_df[i].append('D')
                data_color[i].append('#33ccff')
            elif data[i][j] == 'Move.SPLIT':
                data_df[i].append('P')
                data_color[i].append('#ffff00')
    df = pd.DataFrame(data_df)
    df.columns = column_name
    df.index = row_name
    return df, data_color



if __name__ == '__main__':
    dir_path = 'Data'
    data = {}
    df = {}
    data_color = {}
    column_name = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
    row_name = {'hard_hand': ['20', '19', '18', '17', '16', '15', '14', '13', '12', '11', '10', '9', '8', '7', '6', '5'],
                'soft_hand': ['9', '8', '7', '6', '5', '4', '3', '2'],
                'pair': ['11', '10', '9', '8', '7', '6', '5', '4', '3', '2']}

    for dir in os.listdir(dir_path):
        
        data['hard_hand'] = open_generation_dir(path = dir_path + '/' + dir + '/hard_hand.csv')
        data['soft_hand'] = open_generation_dir(path = dir_path + '/' + dir + '/soft_hand.csv')
        data['pair'] = open_generation_dir(path = dir_path + '/' + dir + '/pairs.csv')

        df['hard_hand'], data_color['hard_hand'] = to_dataframe(data=data['hard_hand'], column_name=column_name, row_name=row_name['hard_hand'])
        df['soft_hand'], data_color['soft_hand'] = to_dataframe(data=data['soft_hand'], column_name=column_name, row_name=row_name['soft_hand'])
        df['pair'], data_color['pair'] = to_dataframe(data=data['pair'], column_name=column_name, row_name=row_name['pair'])

        prepare_table(path=dir_path+'/'+dir+'/'+dir+'.png', generation=dir, data=df, color=data_color)
    