# reduce the file size of these jpgs
from PIL import Image
import os



base_dir = "converted_face_data/"
converted_dir = "small_converted_face_data/"

subdirs = os.listdir(base_dir)
print ("SUBDIRS:", subdirs)
for i in range(0, len(subdirs)):
    raw_path = base_dir + subdirs[i] + "/"
    converted_path = converted_dir + subdirs[i] + "/"
    print ("Beginning ", raw_path)
    if os.path.isdir(raw_path):
        if not os.path.exists(converted_path):
            os.mkdir(converted_path)
        curr_files = os.listdir(raw_path)
        for  j in range(0, len(curr_files)):
            if curr_files[j] != ".DS_Store":
                conv_file_path = converted_path + curr_files[j]
                if not os.path.exists(conv_file_path):
                    im = Image.open(raw_path + curr_files[j])
                    new_im = im.resize((480, 770))
                    new_im.save(converted_path + curr_files[j])
                else:
                    print ("file:", conv_file_path, " already exists")
    else:
        print ("Not a directory:", raw_path)
