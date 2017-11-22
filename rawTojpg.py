#converts images form raw(.nef) to jpg
import rawpy
import imageio
# import os.path, os.listdir
import os



base_dir = "face_data/"
converted_dir = "converted_face_data/"

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
            conv_file_path = converted_path + curr_files[j][:-4] + ".jpg"
            if not os.path.exists(conv_file_path):
                raw_img = rawpy.imread(raw_path + curr_files[j])
                converted_img = raw_img.postprocess()
                imageio.imwrite(converted_path + curr_files[j][:-4] + ".jpg", converted_img)
            else:
                print ("file:", conv_file_path, " already exists")
    else:
        print ("Not a directory:", raw_path)
