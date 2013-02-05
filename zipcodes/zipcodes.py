import math

class ZipCodeRecord:
    """
    zip code record
    """
    def __init__(self, zipcode, lat, lon, perform_transformation=True,
                 **kwargs):
        self.zipcode = zipcode
        if perform_transformation:
            self.lat = math.radians(float(lat))
            self.lon = math.radians(float(lon))
        else:
            self.lat = lat
            self.lon = lon
        
        # position tuple for fater lookup
        self.pos = (self.lat, self.lon)
        
        # contribute additional attributes
        for k,v in kwargs.items():
            setattr(self, k, v)

class ZipCodes:
    """
    zip code manager
    """
    def __init__(self):
        self.zips = {}
        
    def set_zipcode(self, zipcode, lat, lon, perform_transformation=True,
                    **kwargs):
        """
        Set the record for a zipcode
        """
        self.zips[zipcode] = \
            ZipCodeRecord(zipcode, lat, lon, perform_transformation, **kwargs)
        
    def get_zipcode(self, zipcode):
        """
        Gets the zipcode record
        """
        return self.zips[zipcode]
        
    def distance_between_zipcodes(self, zip1, zip2):
        """
        Get the distance in miles between two zipcodes
        """
        return self.distance_between_positions(self.zips[zip1].pos,
            self.zips[zip2].pos)
    
    def distance_between_zipcode_and_position(self, zipcode, pos):
        return self.distance_between_positions(self.zips[zipcode].pos, pos)
    
    def distance_between_positions(self, pos1, pos2):
        """
        Get the distance in miles between two (lat,lon) positions
        """
        lat1, lon1 = pos1
        lat2, lon2 = pos2
        dlon = lon2 - lon1
        dlat = lat2 - lat1        
        
        a = (math.sin(dlat / 2))**2 + math.cos(lat1) * math.cos(lat2) * \
            (math.sin(dlon / 2))**2
        c = 2 * math.asin(min(1, math.sqrt(a)))
        dist = 3956 * c
        return dist

    def within_radius(self, starting_zip, radius):
        """
        Get a list of zipcode,distance tuples for zipcodes within a mile radius
        of the starting zip
        """
        radius_zips = [
            (z, distance) for z, distance in \
                ((z,self.distance_between_zipcodes(z, starting_zip)) \
                for z in self.zips) if distance <= radius
        ]
        
        return radius_zips
    
    def within_radius_sorted(self, starting_zip, radius):
        """
        Get a list of zipcode,distance tuples for zipcodes within a mile radius
        of the starting zip, sorted by distance
        """
        radius_zips = self.within_radius(starting_zip, radius)        
        
        return sorted(radius_zips, key=lambda z: z[1])
        
