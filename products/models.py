from django.db import models
from django.urls import reverse

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Transpose
from imagekit.models import ProcessedImageField
from PIL import Image, ImageDraw, ImageFont, ImageFilter

class Watermark(object):
    def process(self, image):
        watermark = Image.open('/home/silvanog31560/projects/art_gallery/art_root/art/static/art/images/watermark.png')
        image = image.convert("RGBA")
        watermark = watermark.convert("RGBA")
        width = (image.width - watermark.width) // 2
        height = (image.height - watermark.height) // 2
        image.paste(watermark, (width, height), watermark)
        return image

# Create your models here.
class Product(models.Model):
    ACRYLIC_PAINTINGS = 'AP'
    DIGITAL_ART = 'DA'
    OIL_PAINTINGS = 'OP'
    WATERCOLOR_PAINTINGS = 'WP'
    CRAFTS = 'CR'
    CATEGORY_CHOICES = [
        (ACRYLIC_PAINTINGS, 'Acrylic Paintings'),
        (DIGITAL_ART, 'Digital Art'),
        (OIL_PAINTINGS, 'Oil Paintings'),
        (WATERCOLOR_PAINTINGS, 'Watercolor Paintings'),
        (CRAFTS, 'Crafts'),
    ]

    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default=ACRYLIC_PAINTINGS)
    stock = models.IntegerField()
    price = models.IntegerField(default=0) #price in cents for stripe
    added = models.DateTimeField(auto_now_add=True)
    landscape = models.ImageField(blank=True)
    portrait = models.ImageField(blank=True)
    wm_landscape = models.ImageField("watermark landscape", blank=True)
    wm_portrait = models.ImageField("watermark portrait", blank=True)
    try:
        landscape_regular = ImageSpecField(source='landscape',
                                       processors=[
                                        ResizeToFill(800, 600),
                                        ],
                                       format='JPEG',
                                       options={'quality': 60})
        landscape_medium = ImageSpecField(source='landscape',
                                          processors=[
                                          ResizeToFill(700 , 525),
                                          ],
                                          format='JPEG',
                                          options={'quality': 60})
        landscape_thumbnail = ImageSpecField(source='landscape',
                                              processors=[
                                              ResizeToFill(300, 225),
                                              ],
                                              format='JPEG',
                                              options={'quality': 60})
    except:
        pass

    try:
        portrait_regular = ImageSpecField(source='portrait',
                                     processors=[
                                      Transpose(),
                                      ResizeToFill(600, 800),
                                      ],
                                     format='JPEG',
                                     options={'quality': 60})
        portrait_medium = ImageSpecField(source='portrait',
                                        processors=[
                                        Transpose(),
                                        ResizeToFill(525 , 700),
                                        ],
                                        format='JPEG',
                                        options={'quality': 60})
        portrait_thumbnail = ImageSpecField(source='portrait',
                                            processors=[
                                            Transpose(),
                                            ResizeToFill(225, 300),
                                            ],
                                            format='JPEG',
                                            options={'quality': 60})

    except:
        pass

    try:
        wm_landscape_regular = ImageSpecField(source='wm_landscape',
                                       processors=[
                                        ResizeToFill(800, 600),
                                        Watermark(),
                                        ],
                                       format='JPEG',
                                       options={'quality': 60})
        wm_landscape_medium = ImageSpecField(source='wm_landscape',
                                          processors=[
                                          ResizeToFill(700 , 525),
                                          Watermark(),
                                          ],
                                          format='JPEG',
                                          options={'quality': 60})
        wm_landscape_thumbnail = ImageSpecField(source='wm_landscape',
                                              processors=[
                                              ResizeToFill(300, 225),
                                              Watermark(),
                                              ],
                                              format='JPEG',
                                              options={'quality': 60})
    except:
        pass

    try:
        wm_portrait_regular = ImageSpecField(source='wm_portrait',
                                     processors=[
                                      Transpose(),
                                      ResizeToFill(600, 800),
                                      Watermark(),
                                      ],
                                     format='JPEG',
                                     options={'quality': 60})
        wm_portrait_medium = ImageSpecField(source='wm_portrait',
                                        processors=[
                                        Transpose(),
                                        ResizeToFill(525 , 700),
                                        Watermark(),
                                        ],
                                        format='JPEG',
                                        options={'quality': 60})
        wm_portrait_thumbnail = ImageSpecField(source='wm_portrait',
                                            processors=[
                                            Transpose(),
                                            ResizeToFill(225, 300),
                                            Watermark(),
                                            ],
                                            format='JPEG',
                                            options={'quality': 60})

    except:
        pass

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("products:product-detail", args=[str(self.id)])

    def get_display_price(self):
        return "{0:.2f}".format(self.price/100)
