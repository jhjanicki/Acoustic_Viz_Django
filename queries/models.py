from django.db import models

# Create your models here.

class Sites(models.Model):
    site_id = models.TextField(primary_key=True)
    site_name = models.TextField(max_length=255)
    int_id = models.TextField(max_length=255)
    
    class Meta:
        managed = False # this means Django should never alter this table
        db_table = 'site'
    
    def __str__(self):
    	return self.site_id
        

class Data(models.Model):
    data_entry_id = models.IntegerField(primary_key=True)
    site_id = models.TextField(max_length=255)
    # site_id = models.ForeignKey(Sites, db_column='site_id', to_field='site_id')
    date_recorded = models.DateField('%Y-%m-%d')
    time_recorded = models.TimeField('%H:%M:%S')
    average = models.FloatField(null=True, blank=True, default=None)
    original_file = models.TextField(max_length=255)

    class Meta:
        managed = False # this means Django should never alter this table
        db_table = 'acoustic_data'
        #ordering = ['date_recorded', 'time_recorded']
    
    def __str__(self):
    	return str(self.data_entry_id)