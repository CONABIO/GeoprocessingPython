#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import geopandas as gpd
import pandas as pd
import numpy as np

COLUMNA_NOMBRE_REGION = 'country'
COLUMNA_NOMBRE_ESPECIE = 'SCINAME'


def main(regiones, modelos_distribucion, out_counts, out_presenceabsence):
    '''Está función clacula la intersección de los archivos vectoriales
    `regiones` y `modelos_distribucion` y genera las estadística de riqueza de
    especies por región y matriz de presencias-ausencias, las que guarda en los
    archivos correspondientes.

    Parameters
    ----------
    regiones
        Dirección del archivo en formato vectorial con la regiones de interés
    modelos_distribucion
        Dirección del archivo en formato vectorial con las área de distribución
        potencial de las especies (ver Fiona extensiones)
    out_counts
        Ruta del archivo donde se escribirá el conteo de especies por región
    out_presenceabsence
        Ruta del archivo donde se escribirá la matriz de prensencies-ausencias
        por especie por región
    '''
    regiones_gdf = gpd.GeoDataFrame.from_file(regiones)
    modelos_distribucion_gdf = gpd.GeoDataFrame.from_file(modelos_distribucion)

    especies_x_region = gpd.sjoin(regiones_gdf, modelos_distribucion_gdf,
                                  how='inner', op='intersects')
    especies_x_region['auxcol'] = 1

    agrupado_x_region = especies_x_region.groupby(by=COLUMNA_NOMBRE_REGION)
    agrupado_x_region.count()[COLUMNA_NOMBRE_ESPECIE].to_csv(out_counts)

    pivote_regionespecies = pd.pivot_table(
        especies_x_region[[COLUMNA_NOMBRE_REGION,
                           COLUMNA_NOMBRE_ESPECIE,
                           'auxcol']].reset_index(drop=True),
        index=COLUMNA_NOMBRE_REGION,
        columns=COLUMNA_NOMBRE_ESPECIE,
        values='auxcol')
    pivote_regionespecies = pivote_regionespecies.applymap(
        lambda x: 0 if np.isnan(x) else 1)
    pivote_regionespecies.to_csv(out_presenceabsence)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=('Script para encontar la '
                                     'interseccion entre dos shapefiles y '
                                     'generar los archivos de estadísticas '
                                     'de riqueza y matriz de presencias-ausencias'))

    parser.add_argument('regiones', help='Shapefile con la regiones de interés')
    parser.add_argument('modelos_distribucion',
                        help=('Shapefile con modelos de distribución potencial '
                              'con las especies de interés'))
    parser.add_argument('-oc', '--out_counts',
                        help='Nombre de archivo para guardar los conteos por región',
                        default='out_counts.csv')
    parser.add_argument('-om', '--out_presenceabsence',
                        help=('Nombre de archivo para guardar la matriz de '
                              'presencias-ausencias con las regiones de interés'),
                        default='out_presenceabsence.csv')

    args = parser.parse_args()
    main(args.regiones, args.modelos_distribucion,
         args.out_counts, args.out_presenceabsence)
