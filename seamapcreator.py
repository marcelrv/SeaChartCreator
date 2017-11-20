#!/usr/bin/env python
# encoding: utf-8

'''
SeaMapCreator - create sea map in KAP Format

Copyright (C) 2017  Steffen Volkmann

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

from optparse import OptionParser
from Utils.Helper import area, TileInfo
from Utils.Mobac import ExtractMapsFromAtlas
from Utils.DlMan import MapDownloadManager

__app_identifier__ = "seamapcreator version 0.1"


# python createmap.py -i ./sample/atlas/mobac-profile-testprj.xml
# python createmap.py --latnw 52.3705686692 --lonnw 12.9116821289 --latse 52.3437296183 --lonse 12.9446411133 --name GlindowerSee --zoom 15
if __name__ == "__main__":

    parser = OptionParser()
    usage = "usage: %prog [options] arg1 arg2"
    atlas=list()
    
    parser.add_option("-d",     "--DownloadPath", type="string", help="download path",                       dest="DownloadPath", default="./download")
    parser.add_option("-w",     "--WorkingPath",  type="string", help="working path",                        dest="WorkingPath",  default="./work")
    parser.add_option("-i",     "--InFile",       type="string", help="MOBAC Project File",                  dest="ProjectFile")
    parser.add_option("--latnw",                  type="float",  help="latitude north west corner of map",   dest="latnw")
    parser.add_option("--lonnw",                  type="float",  help="longitude north west corner of map",  dest="lonnw")
    parser.add_option("--latse",                  type="float",  help="latitude south east corner of map",   dest="latse")
    parser.add_option("--lonse",                  type="float",  help="longitude south east corner of map",  dest="lonse")
    parser.add_option("-n",      "--name",        type="string", help="name",                                dest="name")
    parser.add_option("-z",      "--zoom",        type="int",    help="zoom level (1-17)",                   dest="level")
    
    options, arguments = parser.parse_args()
    
    if( options.latnw != None and 
        options.lonnw != None and
        options.latse != None and
        options.lonse != None and
        options.name  != None and
        options.level != None ):
        #                   lat0, lon0, lat1, lon1
        atlas.append( area( options.latnw, options.lonnw, options.latse, options.lonse, options.name, options.level ))
    
    elif options.ProjectFile != None:
        # get list of chart areas from project file
        atlas = ExtractMapsFromAtlas(options.ProjectFile) 
    else:
        exit        
    
    dl = MapDownloadManager(options.DownloadPath, options.WorkingPath, __app_identifier__)
    
    for singlemap in atlas:
        ti = TileInfo(singlemap)
        print(ti)
        # check requested zoom level and number of tiles to meet the tile usage policy
        if(ti.zoom >= 17):
            print("zoom level {} not supported. Please check https://operations.osmfoundation.org/policies/tiles/ for detailes ")
            continue  
        elif(ti.nr_of_tiles >= 100):
            print(singlemap)
            continue  
        dl.LoadTiles(ti)
        dl.MergeTiles(ti)
        dl.GenKapFile(ti)
    
    print("end")