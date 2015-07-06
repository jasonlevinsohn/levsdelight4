import os, logging
from PIL import Image, ImageFile
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.s3.acl import CannedACLStrings

logging_file = os.getcwd() + '/logs/uploader.log'
print 'Logging File: ', logging_file
logging.basicConfig(filename=logging_file, level=logging.INFO)

class ImageUploader:

    
    def __init__(self, file_name='test-image.jpg', month_to_save_to='june2015', scale_img=30, img_quality=80, temp_dir='tmp'):

        self.file_name = file_name
        self.this_path = os.path.dirname(os.path.abspath(__file__)) + '/' + temp_dir
        self.full_file_path = self.this_path + '/' + self.file_name
        self.temp_dir = temp_dir

        self.month_to_save_to = month_to_save_to
        self.scale = scale_img
        self.quality = img_quality

        logging.info('Image Uploader Initialized')


    def upload_original(self):
        bytes_uploaded = self.uploadImage(self.file_name)
        print str(bytes_uploaded) + ' bytes uploaded for original file'

        logging.info('Original File Uploaded')

        return 'Original file uploaded'

        
    def create_upload_thumbnail(self):

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
                logging.info('Thumbnail created.  File saved as', thumbnail_file_name)
            except IOError:
                print 'could not create thumbnail for', self.file_name
                logging.error('could not create thumbnail for', self.file_name)

        # Upload the thumbnail to S3
        bytes_uploaded = self.uploadImage(thumbnail_file_name)
        print str(bytes_uploaded) + ' bytes uploaded to S3 for thumbnail file.'

    def create_upload_web_image(self):

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

                scaled_image_file = image_file.resize((width, height), Image.ANTIALIAS)

                scaled_image_file.save(self.this_path + '/' + web_file_name,
                        optimize=True,
                        quality=self.quality,
                        progressive=True)

                print 'Web File Created. File saved as ', web_file_name
                logging.info('Web File Created. File saved as ', web_file_name)
                print 'Quality Level: ', self.quality

                print 'Scaled to %s percent' % self.scale

                # Upload web file to S3
                bytes_uploaded = self.uploadImage(web_file_name)
                print str(bytes_uploaded) + ' saved to S3 for web file.'

                return 'Web File Created Successfully'

            except IOError as e:
                print 'File could not be saved for', self.file_name
                logging.error('File could not be saved for', self.file_name)
                print e.strerror

                return 'Web File Error: %s' % e.strerror

    def connectToS3(self):
        # Create a connection
        key = os.environ.get('AWS_ACCESS_KEY_ID')
        secret = os.environ.get('AWS_SECRET_ACCESS_KEY')
        s3 = S3Connection(key, secret)

        # Get the bucket
        self.levsbucket = s3.get_bucket('levsdelight')
        logging.info('Connected to S3')

        return 'Connected to S3'

    def uploadImage(self, file_name):

        bytes_uploaded = None

        # Save image to bucket
        s3_image_key_name = 'img/%s/%s' % (self.month_to_save_to, file_name)
        s3_image_key = Key(self.levsbucket, s3_image_key_name)

        try:

            full_file_path = self.this_path + '/' + file_name
            number_of_times_to_call_callback = 5
            bytes_uploaded = s3_image_key.set_contents_from_filename(
                    full_file_path,
                    None,
                    True,
                    self.upload_callback,
                    number_of_times_to_call_callback,
                    CannedACLStrings[1],
                    None,
                    True)

            print 'File %s has been uploaded to key %s' % (file_name, s3_image_key_name)
            logging.info('File %s has been uploaded to key %s' % (file_name, s3_image_key_name))

            return bytes_uploaded
        
        except IOError:
            print 'There was an error finding the file'
            logging.error('There was an error finding the file')
            return 0

        except Exception as e:
            print 'Error uploading file: %s' % e.message
            logging.error('Error uploading file: %s' % e.message)

            return 0

    def upload_callback(self, amt_uploaded, full_size):
        print 'Uploading: %d/%d' % (amt_uploaded, full_size)
        logging.info('Uploading: %d/%d' % (amt_uploaded, full_size))


        

# This is how we do it

# ic = ImageConverter('test-image.jpg', 30, 80)
# ic.create_web_image()
# ic.create_thumbnail()

