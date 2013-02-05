from django.db import models
from managers import ZipcodeManager
import csv

class Zipcode(models.Model):
    """
    Zipcode
    """
    zipcode = models.CharField(db_index=True, max_length=5, unique=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    county = models.CharField(max_length=255, blank=True)
    location_text = models.CharField(max_length=255, blank=True)
    
    objects = ZipcodeManager()

    def __unicode__(self):
        return '%s %s' % (self.zipcode,self.location_text,)        
    
class ZipcodeUpload(models.Model):
    """
    Zipcode Upload
    """
    csv_file = models.FileField(upload_to='apps/zipcodes/csv')    
    complete_update = models.BooleanField(default=False,
        help_text='a complete update will wipe all existing zipcodes')

    def save(self, *args, **kwargs):
        super(ZipcodeUpload, self).save(*args, **kwargs)
        zipcode_update = self.process_upload()
        super(ZipcodeUpload, self).delete()
        return zipcode_update
    
    def process_upload(self):
        # create the zipcode update with the initial status
        zu = ZipcodeUpdate(status='Processing')
        zu.save()

        if self.complete_update:
            zu.details += 'Performing complete update\n'
        else:
            zu.details += 'Performing incremental update\n'
            
        # if this is a complete update, delete the zipcodes
        if self.complete_update:
            zu.details += 'Deleting %s existing zipcodes\n' % (Zipcode.objects.count(),)
            Zipcode.objects.all().delete()
            
        try:
            # get a csv reader
            rdr = csv.reader(open(self.csv_file.path))
            add_counter = 0
            update_counter = 0
            skip_counter = 0
            zu.details += 'Iterating csv\n'
            for (zipcode, lat, lon, city, state, county, location_text) in rdr:
                try:
                    is_new = False
                    zc = Zipcode.objects.get(zipcode=zipcode)
                except Zipcode.DoesNotExist:
                    is_new = True
                    zc = Zipcode(zipcode=zipcode)
                    
                try:
                    if lat:
                        lat = float(lat)
                    else:
                        lat = None
                    if lon:
                        lon = float(lon)
                    else:
                        lon = None
                    
                    zc.lat = lat
                    zc.lon = lon
                    zc.city = city
                    zc.state = state
                    zc.county = county
                    zc.location_text = location_text
                    zc.save()
                    if is_new:
                        add_counter += 1
                    else:
                        update_counter += 1
                except Exception as e:
                    skip_counter += 1
                    zu.details+= 'Error (skipping row): %s\n' % (e,)
            zu.status = '%s zipcodes added, %s updated, %s skipped' % (add_counter, update_counter, skip_counter)
            zu.details+= 'complete'
            zu.save()
            
        except Exception as e:
            zu.status = 'Error'
            zu.details+= '%s\n' % (e,)
            zu.save()

        return zu
    
class ZipcodeUpdate(models.Model):
    """
    Zipcode Update
    """
    date_added = models.DateTimeField(auto_now_add=True)    
    status = models.CharField(blank=True, max_length=255)
    details = models.TextField(blank=True)
    
    def __unicode__(self):
        return '%s' % (self.date_added,)        
    