from django.db import models
from zipcodes import ZipCodes

class ZipcodeManager(models.Manager):
    """
    Zipcode Manager
    """
    # use for related fields
    use_for_related_fields = True
    
    def get_zc(self):
        """
        Get the lower level zipcode manager
        """
        zc = getattr(self, '__zc', None)
        if not zc:
            self.initialize_zipcode_manager()
        return getattr(self, '__zc')
    
    def reset_zipcode_manager(self):
        """
        Reset the zipcode manager
        """
        setattr(self, '__zc', None)
        
    def initialize_zipcode_manager(self):
        """
        Initialize the zipcode manager
        """
        zc = ZipCodes()
        from models import Zipcode
        for z in Zipcode.objects.all():
            if z.lat and z.lon:
                zc.set_zipcode(z.zipcode, z.lat, z.lon, True,
                           city=z.city, state=z.state, county=z.county,
                           location_text=z.location_text)
        setattr(self, '__zc', zc)
                
