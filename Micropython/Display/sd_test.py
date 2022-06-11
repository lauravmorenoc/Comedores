# More details can be found in TechToTinker.blogspot.com 
# George Bantique | tech.to.tinker@gmail.com

import os
from machine import Pin, SoftSPI
from sdcard import SDCard

# Pin assignment:
# MISO -> GPIO 21
# MOSI -> GPIO 22
# SCK  -> GPIO 19
# CS   -> GPIO 23
spisd = SoftSPI(-1, miso=Pin(21), mosi=Pin(22), sck=Pin(19))
sd = SDCard(spisd, Pin(23))


print('Root directory:{}'.format(os.listdir()))
vfs = os.VfsFat(sd)
os.mount(vfs, '/sd')
print('Root directory:{}'.format(os.listdir()))
os.chdir('sd')
print('SD Card contains:{}'.format(os.listdir()))


# 1. To read file from the root directory:
# f = open('sample.txt', 'r')
# print(f.read())
# f.close()

# 2. To create a new file for writing:
# f = open('sample2.txt', 'w')
# f.write('Some text for sample 2')
# f.close()

# 3. To append some text in existing file:
# f = open('sample3.txt', 'a')
# f.write('Some text for sample 3')
# f.close()

# 4. To delete a file:
# os.remove('file to delete')

# 5. To list all directories and files:
# os.listdir()

# 6. To create a new folder:
# os.mkdir('sample folder')

# 7. To change directory:
# os.chdir('directory you want to open')

# 8. To delete a folder:
# os.rmdir('folder to delete')

# 9.  To rename a file or a folder:
# os.rename('current name', 'desired name')