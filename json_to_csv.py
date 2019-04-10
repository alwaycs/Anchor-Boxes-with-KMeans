import os
import glob
import pandas as pd
import json
from PIL import Image


def json_to_csv(name_list, img_dir, gt_dir):
    json_list = []
    for name in name_list:
        image_path = os.path.join(img_dir, name.strip('\n'))
        im = Image.open(image_path)
        width, height = im.size
        gt_name = name.replace('.jpg', '.json')
        gt_path = os.path.join(gt_dir, gt_name.strip('\n'))
        with open (gt_path) as f:
            anno = json.load(f)
            lines = anno['lines']
            for line in lines:
                poly = line['points']
                x1, y1, x2, y2, x3, y3, x4, y4 = poly
                xmin = min(x1,x2,x3,x4)
                ymin = min(y1,y2,y3,y4)
                xmax = max(x1,x2,x3,x4)
                ymax = max(y1,y2,y3,y4)
                value = (name, width, height, xmin, ymin, xmax, ymax)
                json_list.append(value)
    column_name = ['filename', 'width', 'height', 'xmin', 'ymin', 'xmax', 'ymax']
    json_df = pd.DataFrame(json_list, columns=column_name)
    return json_df


def main():
    img_dir = "/workspace/meijinpeng/dataset/ReCTS/img/"
    gt_dir = "/workspace/meijinpeng/dataset/ReCTS/gt/"
    train_txt = "/workspace/meijinpeng/dataset/ReCTS/train.txt"
    test_txt = "/workspace/meijinpeng/dataset/ReCTS/test.txt"
    work_dir = os.getcwd()
    with open(train_txt) as f_train:
        train_name=f_train.readlines()
        all_name = train_name
        print(len(train_name), type(train_name))
    with open(test_txt) as f_test:
        test_name=f_test.readlines()
        print(len(test_name))
    all_name.extend(test_name)
    print("all_name", len(all_name))
    print("train_name", len(train_name))


    for flag, path_list in zip(['train', 'test', 'all'], [train_name, test_name, all_name]):
        print('start aonvert:', flag)
        json_df = json_to_csv(path_list, img_dir, gt_dir)
        csv_path = os.path.join(work_dir, flag + '_labels.csv')
        json_df.to_csv(csv_path, index=None)
        print('Successfully converted ', flag, 'json to csv.')


main()
