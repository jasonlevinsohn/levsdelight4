import os
from PIL import Image, ImageFile
from boto.s3.connection import S3Connection
from boto.s3.key import Key


class ImageConverter:

    
    def __init__(self, file_name='test-image.jpg', scale_img=30, img_quality=80):

        self.file_name = file_name
        self.this_path = os.path.dirname(os.path.abspath(__file__))
        self.full_file_path = self.this_path + '/' + self.file_name

        self.scale = scale_img
        self.quality = img_quality

        print 'File %s opened successfully' % self.full_file_path

    def create_thumbnail(self):

        thumbnail_size = 256, 256 

        # Create thumbnail version
        name_part_only = self.file_name.split('.')[0]
        thumbnail_file_name = name_part_only + '-thumbnail.jpg'

        if self.file_name != thumbnail_file_name:
            try:
                thumb = Image.open(self.full_file_path)
                thumb.thumbnail(thumbnail_size)
                thumb.save(self.this_path + '/' + thumbnail_file_name, 'JPEG')
                print 'Thumbnail created.  File saved as', thumbnail_file_name
            except IOError:
                print 'could not create thumbnail for', self.file_name

    def create_web_image(self):

        # Create Image ready for website
        name_part_only = self.file_name.split('.')[0]
        web_file_name = name_part_only + '-web.jpg'
        
        if self.file_name != web_file_name:
            try:
                image_file = Image.open(self.full_file_path)
                if self.scale == 100:
                    width, height = image_file.size
                else:
                    width = int((self.scale * image_file.size[0]) / 100)
                    height = int((self.scale * image_file.size[1]) / 100)
                    # width, height = (int(self.scale * image_file.size[0] / 100.0)),
                    # (int(self.scale * image_file.size[1] / 100.0))

                scaled_image_file = image_file.resize((width, height), Image.ANTIALIAS)

                scaled_image_file.save(self.this_path + '/' + web_file_name,
                        optimize=True,
                        quality=self.quality,
                        progressive=True)

                print 'Web File Created. File saved as ', web_file_name
                print 'Quality Level: ', self.quality
                print 'Scaled to %s percent' % self.scale
            except IOError as e:
                print 'File could not be saved for', self.file_name
                print e.strerror

    def getEnvir(self):
        this_var = os.environ.get('OFFLINE')
        print 'Environment Var is %s' % this_var

    def checkFolderExists(self, file_name='june2016'):

        # Create a connection
        key = os.environ.get('AWS_ACCESS_KEY_ID')
        secret = os.environ.get('AWS_SECRET_ACCESS_KEY')
        s3 = S3Connection(key, secret)

        # Get the bucket
        levsbucket = s3.get_bucket('levsdelight')


        # Check for the folder(key)
        s3_image_key = Key(levsbucket, 'img/%s' % (file_name))
        # s3_image_key = Key(levsbucket)
        # s3_image_key.key('img/%s' % (file_name))

        s3_image_key.set_contents_from_string('This is the content of the text file')
        
        # if folder_key.exists():
        #     print 'The folder img/%s/ exists' % (folder_name)
        # else:
        #     print 'The folder img/%s/ DOES NOT exist' % (folder_name)




# This is how we do it
# ic = ImageConverter('test-image.jpg', 30, 80)
# ic.create_web_image()
# ic.create_thumbnail()

