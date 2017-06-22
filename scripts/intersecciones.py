import geopandas as gpd
from os import path
import glob

# Aqui defino donde estan los folders donde estan los
# datos
DATA_FOLDER = path.join('..', 'datos')

shapes_anfibios = glob.glob(
    path.join(
        DATA_FOLDER,
        'anfibios',  # Nombre la carpeta con los shapes
        '*.shp'
    )
)

shapesANPS_gdf = gpd.GeoDataFrame.from_file(
        path.join(DATA_FOLDER, 'SHAPE_ANPS',
                  '181ANP_Geo_ITRF08_Enero_2017.shp'))

# Obtengo la proyeccion de alguno de los rasters de anfibios
anfibios_crs = gpd.GeoDataFrame.from_file(shapes_anfibios[0]).crs

shapesANPS_gdf = shapesANPS_gdf.to_crs(anfibios_crs)

for shape in shapes_anfibios:
    nombre = path.basename(shape)
    nombre = path.splitext(nombre)[0]
    shape_gdf = gpd.GeoDataFrame.from_file(shape)

    shapesANPS_gdf[nombre] = shapesANPS_gdf.geometry.intersects(
            shape_gdf.geometry.unary_union)

    shapesANPS_gdf[nombre] = shapesANPS_gdf[nombre].astype('int')

shapesANPS_gdf.to_file('riquezaAnfibios.shp')
