""" Python script to download and visualize MODIS sensor data
processed with the MODVOLC algorithm using Normalized Thermal
Index (NTI) develooped by Wright et al. (2002). RSE, 82: 135-155
See also Wright et al. (2004). JVGR, 135: 29-49

This code was written by Jose Armando Saballos, PhD
"""
#===================================================================#
#                          INPUT PARAMETERS                         #
#===================================================================#

# Name of site to detect the MODVOLC thermal anomalies #
name = "Masaya volcano" # name in double-quotes #

# Initial date to look for the thermal anomalies: ti (YYYY-MM-DD) #
ti = "2000-02-01" # Start date to look for MODVOLC thermal anomalies in double-quotes #

# Final date to look for the thermal anomalies: tf (YYYY-MM-DD) #
tf = "2024-08-11" # Final date to look for MODVOLC thermal anomalies in double-quotes #

# Geographic WGS84 coordinates of the site of interest: lon E (ddg), lat N (ddg) #
lon = -86.163783 # e.g. lon = -90.88063 # East longitude in decimal degrees
lat = 11.994702 # e.g. lat = 14.47409 # North latitude in decimal degrees

# Search Radius for thermal anomalies around the site of interest in (km) #
rad = 2.5 # Radius of search in km

#======================================================================#
#                        END of INPUT PARAMETERS                       #
#======================================================================#

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>#
#======================================================================#
#        DON'T CHANGE ANYTHING ELSE, THE SCRIPT WILL DO THE REST       #
#======================================================================#
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>#

#===================================================================#
#                              IMPORTs                              #
#===================================================================#
import pandas as pd # 2.2.2
import numpy as np # 1.26.4
import seaborn as sns # 0.13.2
import matplotlib.pyplot as plt # 3.8.4
import matplotlib.dates as mdates # 3.8.4
import folium # 0.16.0
import requests # 2.31
from datetime import datetime
from pathlib import Path
import os

#========================================================================#

ti = datetime.strptime(ti, "%Y-%m-%d")
tf = datetime.strptime(tf, "%Y-%m-%d")
dt = tf-ti # time interval #
dj = ti.strftime("%j") # day of the year of final input date
yr = ti.strftime("%Y") # year of final input date

url = 'http://modis.higp.hawaii.edu/cgi-bin/mergeimage?maptype=alerts&jyear=' + tf.strftime("%Y") + '&jday=' + tf.strftime("%j") + '&jperiod=' + str(dt.days) + '&lonmin=' + str(lon-0.2) + '&latmin=' + str(lat-0.2)+'&lonmax=' + str(lon+0.2)+'+&latmax='+str(lat+0.2)
modvolc_file = requests.get(url)
with open("modvolc_data.dat", "w") as f:
    f.write(modvolc_file.text)
#
in_f1 = 'modvolc_data.dat' # reading MODVOLC extracted data #
#======================================================================#

def modvolc_points(vname,vlat,vlon,rad,dat_f,dyr):
    """ Función escrita por J A Saballos <j.a.saballos@gmail.com>
        Parámetros de entrada de la función (Input parameters):
        vname: nombre del volcán (e.g. Santa María)
        vlat: Latitud geográfica del sitio (e.g. 14.85694)
        vlon: Longitud geográfica del sitio (e.g. -89.65425)
        rad: radio de búsqueda alrededor del volcán en km (e.g. 4.8)
        dat_f: nombre y ruta del archivo de datos
        dyr: cantidad de tiempo en años que será utilizado para extaer los datos
             modvolc a partir del día de hoy
        Para mayor información leer los siguientes artículos:
        1) Wright et al. (2002). Automated volcanic eruption detection using MODIS.
           Remote sensing of environment, 82(1), 135-155.
        2) Wright et al. (2004) "MODVOLC: near-real-time thermal monitoring of global volcanism."
           Journal of Volcanology and Geothermal Research 135.1-2 : 29-49.
        3) Wright (2016). MODVOLC: 14 years of autonomous observations of effusive
           volcanism from space. Geological Society, London, Special Publications, 426(1), 23-53.
    """   
    # Definiendo el radio de búsqueda de anomalías alrededor del sitio de interés # 
    dlatp = vlat + (rad/106.8)
    dlatn = vlat - (rad/106.8)
    dlonp = vlon + (rad/106.8)
    dlonn = vlon - (rad/106.8)
    # Extraer los datos MODVOLC #=======================================================#
    df = pd.read_csv(in_f1, header=None, usecols=[2,3,4,5,6,7,8,9,20], delimiter=r"\s+",
         names=['yr', 'mm', 'dd', 'hr', 'mn', 'lon', 'lat', 'b21','nti'] )
    # Filtrar los datos con respecto al volcán o sitio de interés #=====================#
    df_filt = df.query('lon <= @dlonp & lon >= @dlonn & lat <= @dlatp & lat >= @dlatn')
    if len(df_filt) > 0:
       fecha = pd.to_datetime(dict(year=df_filt.yr, month=df_filt.mm, day=df_filt.dd, hour=df_filt.hr,
               minute=df_filt.mn)) # Crear fecha en formato pandas #
       #
       df_fecha = df_filt.assign(fecha=fecha)
       df_fecha.reset_index(drop=True, inplace=True)
       #=========================================================================================#
       # PIXELES CALIENTES y RADIANCIA ESPECTRAL (4 um) #========================================#
       #=========================================================================================#
       # Datos diario #
       c_dia = df_fecha.resample('D', on='fecha').count() # Conteo píxeles Diario
       c_dia.rename(columns = {'yr':'Daily_pixels'}, inplace = True)
       c_dia.drop(['mm', 'dd', 'hr', 'mn', 'lon', 'lat', 'b21', 'nti'], axis=1, inplace=True)
       r_dia = df_fecha.resample('D', on='fecha').sum() # Radiancia Diaria
       df_dia = c_dia.assign(radiancia_diaria=r_dia.b21)
       # Datos semanal #
       c_week = df_fecha.resample('W', on='fecha').count() # Semanal
       c_week.rename(columns = {'yr':'Weekly_pixels'}, inplace = True)
       c_week.drop(['mm', 'dd', 'hr', 'mn', 'lon', 'lat', 'b21', 'nti'], axis=1, inplace=True)
       r_week = df_fecha.resample('W', on='fecha').sum() # Radiancia semanal
       df_week = c_week.assign(radiancia_semanal=r_week.b21)
       # Datos mensual #
       c_mes = df_fecha.resample('ME', on='fecha').count() # Mensual
       c_mes.rename(columns = {'yr':'Monthly_pixels'}, inplace = True)
       c_mes.drop(['mm', 'dd', 'hr', 'mn', 'lon', 'lat', 'b21', 'nti'], axis=1, inplace=True)
       r_mes = df_fecha.resample('ME', on='fecha').sum() # Radiancia mensual
       df_mes = c_mes.assign(radiancia_mensual=r_mes.b21)
       # Datos anual #
       c_yr = df_fecha.resample('YE', on='fecha').count() # Anual
       c_yr.rename(columns = {'yr':'Pixeles_anual'}, inplace = True)
       c_yr.drop(['mm', 'dd', 'hr', 'mn', 'lon', 'lat', 'b21', 'nti'], axis=1, inplace=True)
       r_yr = df_fecha.resample('YE', on='fecha').sum() # Radiancia anual
       df_yr = c_yr.assign(radiancia_anual=r_yr.b21)
       #
       #==========================================================================================#
       # Fig 1, PIXELES CALIENTES #===============================================================#
       #==========================================================================================#
       # Time-series Pixeles calientes: diaria, semanal, mensual y anual #
       fig, axs = plt.subplots(ncols=1, nrows=3, figsize=(13,8))
       titulo1 = 'Hot pixels for the site ' + vname + '. Modvolc Algorithm. Search radius = '+str(rad)+' km'
       fig.suptitle(titulo1)
       # Panel superior. Plot conteo de anomalías anual #
       sns.lineplot(data=c_yr, x='fecha', y='Pixeles_anual', marker='o', label='Hot pixels per year', color='g', ax=axs[0])
       axs[0].set_ylabel('Number of Hot Pixels')
       axs[0].tick_params(right=True, top=True, labelright=True, labeltop=False, bottom=True, labelsize=8)
       axs[0].tick_params(colors='g', axis='y')
       axs[0].grid(alpha=0.5)
       #
       # Panel intermedio. Conteo mensual #
       sns.lineplot(data=c_mes, x='fecha', y='Monthly_pixels', marker='o', label='Hot pixels per month', color='r', ax=axs[1])
       plt.subplots_adjust(wspace=0, hspace=0)
       axs[1].set_ylabel('Number of Hot Pixels')
       axs[1].set_xticklabels([])
       axs[1].tick_params(right=True, top=False, labelright=True, labeltop=False, labelbottom=False, labelsize=8)
       axs[1].tick_params(colors='red', axis='y')
       #
       # Panel inferior. Plot conteo de anomalías diarias y semanales #
       sns.lineplot(data=c_dia, x='fecha', y='Daily_pixels', label='Hot pixels per day', alpha=0.6, ax=axs[2])
       sns.lineplot(data=c_week, x='fecha', y='Weekly_pixels', label='Hot pixels per week', alpha=0.6, ax=axs[2])
       plt.subplots_adjust(wspace=0, hspace=0)
       axs[2].set_ylabel('Number of Hot Pixels')
       axs[2].set_xlabel('Date', multialignment='center')
       axs[2].tick_params(right=True, labelright=True, top=True)
       axs[2].xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
       axs[2].grid(alpha=0.5)
       plt.xticks(fontsize=8)
       #
       # Guardar Fig 1 como PNG con el nombre del volcán en folder #
       vname = vname.replace(" ","_")
       if (Path(vname).is_dir()) == False:
          print('Creating directory:',vname, '\n')
          os.mkdir(vname)
       #
       fig1png = 'plot_site_'+ vname + '_hot_pixels_MODVOLC.png'
       f1path = os.path.join(vname,fig1png)
       plt.savefig(f1path, dpi=300, bbox_inches = 'tight')
       fig1pdf = 'plot_site_'+ vname + '_hot_pixels_MODVOLC.pdf'
       f1path = os.path.join(vname,fig1pdf)
       plt.savefig(f1path, dpi=300, bbox_inches = 'tight')
       #
       #==========================================================================================#
       # Fig 2, RADIANCIAS ESPECTRALES #==========================================================#
       #==========================================================================================#
       # Time-series Radiancia espectral (4 um): diaria, semanal, mensual y anual #
       fig, axs = plt.subplots(ncols=1, nrows=3, figsize=(13,8))
       titulo2 = 'Spectral radiance (4 μm) for site ' + vname + '. Modvolc algorithm. Search radius = '+str(rad)+' km'
       fig.suptitle(titulo2)
       # Panel superior. Radiancia anual #
       sns.lineplot(data=r_yr, x='fecha', y='b21', marker='o', label='Radiance per year', color='g', ax=axs[0])
       axs[0].set_ylabel('Spectral radiance\n(W/(m$^{-2}$ sr$^{-1}$ μm$^{-1}$)', multialignment='center')
       axs[0].tick_params(right=True, top=True, labelright=True, labeltop=False, bottom=True, labelsize=8)
       axs[0].tick_params(colors='g', axis='y')
       axs[0].grid(alpha=0.5)
       #
       # Panel intermedio. Radiancia mensual #
       sns.lineplot(data=r_mes, x='fecha', y='b21', marker='o', label='Radiance per month', color='r', ax=axs[1])
       plt.subplots_adjust(wspace=0, hspace=0)
       axs[1].set_ylabel('Spectral radiance\n(W/(m$^{-2}$ sr$^{-1}$ μm$^{-1}$)', multialignment='center')
       axs[1].set_xticklabels([])
       axs[1].tick_params(right=True, top=False, labelright=True, labeltop=False, labelbottom=False, labelsize=8)
       axs[1].tick_params(colors='red', axis='y')
       #
       # Panel inferior. Plot radiancia diarias y semanales #
       sns.lineplot(data=r_dia, x='fecha', y='b21', label='Radiance per day', alpha=0.6, ax=axs[2])
       sns.lineplot(data=r_week, x='fecha', y='b21', label='Radiance per week', alpha=0.6, ax=axs[2])
       plt.subplots_adjust(wspace=0, hspace=0)
       axs[2].set_ylabel('Spectral radiance\n(W/(m$^{-2}$ sr$^{-1}$ μm$^{-1}$)', multialignment='center')
       axs[2].set_xlabel('Date', multialignment='center')
       axs[2].tick_params(right=True, labelright=True, top=True)
       axs[2].xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
       axs[2].grid(alpha=0.5)
       plt.xticks(fontsize=8)       
       #
       # Guardar Fig 2 como PNG con el nombre del volcán en folder #
       fig2png = 'plot_site_'+ vname + '_spectral_radiance_MODVOLC.png'
       f1path = os.path.join(vname,fig2png)
       plt.savefig(f1path, dpi=300, bbox_inches = 'tight')
       fig2pdf = 'plot_site_'+ vname + '_spectral_radiance_MODVOLC.pdf'
       f1path = os.path.join(vname,fig2pdf)
       plt.savefig(f1path, dpi=300, bbox_inches = 'tight')
       #
       #==========================================================================================#
       # Fig 3, HISTOGRAMAS DEL NTI #=============================================================#
       #==========================================================================================#
       # Histograma que muestra la frecuecia de ocurrencia del índice NTI #
       fig = plt.subplots(figsize=(10, 5))
       plt.grid(True, alpha=0.25)
       sns.histplot(data=df_filt, x='nti',binwidth=0.02)
       plt.xlabel('Less strong thermal anomaly <----  NTI  ----> More strong thermal anomaly')
       plt.ylabel('Frequency')
       titulo3 = 'Histogram for site ' + vname + '. Normalized thermal index (NTI), n = ' + str(len(df_filt.nti))
       plt.title(titulo3)
       fig3png = 'plot_histogram_NTI_site_'+ vname + '.png'
       f1path = os.path.join(vname,fig3png)
       plt.savefig(f1path, dpi=300, bbox_inches = 'tight')
       fig3pdf = 'plot_histogram_NTI_site_'+ vname + '.pdf'
       f1path = os.path.join(vname,fig3pdf)
       plt.savefig(f1path, dpi=300, bbox_inches = 'tight')
       #
       #==========================================================================#
       #                     Guardar datos en archivos *.csv                      #
       #==========================================================================#
       dfile = 'modvolc_data_per_day_' + vname + '.csv' # datos por dia #
       df_dia.to_csv(os.path.join(vname,dfile)) # datos por dia #
       wfile = 'modvolc_data_per_week_' + vname + '.csv' # datos por semana #
       df_week.to_csv(os.path.join(vname,wfile)) # datos por semana #
       mfile = 'modvolc_data_per_month_' + vname + '.csv' # datos por mes #
       df_mes.to_csv(os.path.join(vname,mfile)) # datos por mes #
       yfile = 'modvolc_data_year_' + vname + '.csv' # datos anual #
       df_yr.to_csv(os.path.join(vname,yfile)) # datos anual #
       nfile = 'modvolc_all_data_site_' + vname + '.csv' # Anomalias originales #
       df_fecha.rename(columns={'lon':'longitude','lat':'latitude','b21':'radiance'}, inplace = True)
       print(df_fecha.head())
       columnas = ['fecha','longitude','latitude','radiance']
       df_fecha.to_csv(os.path.join(vname,nfile), index=False,columns = columnas)
       #===========================================================================#
       #                 Generar Google Map con anomalías térmicas                 #
       #===========================================================================#
       puntos = [];
       etiqueta = [];
       i = 0
       for index, row in df_fecha.iterrows():
           Date = row['fecha']
           Lat = row['latitude']
           Lon = row['longitude']
           Rad = row['radiance']
           NTI = row['nti']
           texto = f"Date: {Date}\nLatitude: {Lat}\nLongitude: {Lon}\nRadiance: {Rad}\n\nNTI = {NTI}"
           etiqueta.append(texto)
           puntos.append([df_fecha['latitude'][i],df_fecha['longitude'][i]])
           i = i+1
       #
       #
       map = folium.Map(location=[vlat, vlon], tiles = 'OpenStreetMap', zoom_start=13, control_scale=True)
       folium.raster_layers.TileLayer('cyclosm',attr="openstreet.com/").add_to(map)
       folium.raster_layers.TileLayer('OpenStreetMap.HOT', attr="http://openstreet.com/").add_to(map)
       folium.raster_layers.TileLayer('opentopomap').add_to(map)
       folium.LayerControl().add_to(map)
       #
       if len(puntos) > 10:
          i2 = 0
          for i2 in range(10):
              folium.CircleMarker(puntos[i2],popup = etiqueta[i2], radius = 8,color = 'red',fill = True).add_to(map)
              i2 = 1 + i2
              #
          for i2 in range(i2,len(puntos)):
              folium.CircleMarker(puntos[i2],popup = etiqueta[i2], radius = 8,color = 'orange',fill = True).add_to(map)
              i2 = 1 + i2
              #
       else:
          i3 = 0
          for point in puntos:
              folium.CircleMarker(point,popup = etiqueta[i3], radius = 8,color = 'red',fill = True).add_to(map)
              i3 = 1 + i3
          #
       nhtml = 'modvolc_' + vname + '.html'
       map.save(outfile = os.path.join(vname,nhtml))
       print(f'\nAll the results have been saved into the folder <{vname}>, inside the current folder\n')
       #
       #
    else:
         print(f'The MODVOLC algorithm "did not" detect any thermal anomalies for the site <{name}> during the given dates')
    #
# Fin de la función #

print(f'\nProcessing the MODVOLC thermal anomalies for the site <{name}>')
print('User input geographic coordinates for the site of interest: Longitude =', lon, '/ Latitude =', lat)
print(f'Start time: {ti}')
print(f'End time: {tf}')
print(f'Amount of days: {dt.days}\n')
print(f'Small sample of the thermal anomalies found. The generated CSV files contain all the anomalies:')

modvolc_points(name,lat,lon,rad,in_f1,dt)

# Fin del script #
