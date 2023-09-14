import re
from django.core.exceptions import ValidationError

class validate_youtube_link:
   def __init__(self, fields):
      self.fields = fields

   def __call__(self, value):
      youtube_pattern = r'https://www\.youtube\.com/'
      tmp_val = dict(value).get(self.fields)

      if not re.match(youtube_pattern, tmp_val):
         raise ValidationError("Ссылка должна вести на YouTube.")
