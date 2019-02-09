#!/usr/bin/python3
# encoding: utf-8

'''

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
from Utils.Mobac import ExtractMapsFromAtlas
from Utils.Helper import ChartInfo
from tile.manager import TileManager
from Utils.glog import getlog, initlog
from tile.sqllitedb import TileSqlLiteDB
from Utils.download import CheckExternelUtils
import time

DBDIR = './work/database/'
WDIR = './work/'


def main():
    parser = OptionParser()

    parser.add_option("-i", "--InFile",
                      type="string",
                      help="MOBAC Project File",
                      dest="ProjectFile",
                      default="./sample/atlas/mobac/mobac-profile-testprj.xml")

    parser.add_option("-d", "--DatabaseDirectory",
                      type="string",
                      help="tile store directory",
                      dest="DBDIR",
                      default=DBDIR)

    parser.add_option("-u", "--update",
                      action="store_true",
                      dest="update",
                      help="update tile if new version existes")

    parser.add_option("-q", "--quiet",
                      action="store_false",
                      dest="quiet",
                      default=True,
                      help="set log level to info (instead debug)")

    parser.add_option("-s", "--skip",
                      action="store_true",
                      dest="skip_os",
                      help="skip odd zoom levels")

    options, arguments = parser.parse_args()
    arguments = arguments

    initlog('fetch', options.quiet)
    logger = getlog()

    logger.info('Start fetch tiles')

    if(options.skip_os is True):
        zoom_filter = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    else:
        zoom_filter = []

    # get maps from mobac project file
    if options.ProjectFile is not None:
        # get list of chart areas from project file
        atlas, name = ExtractMapsFromAtlas(options.ProjectFile, zoom_filter)
        logger.info('atlas name={} number of maps={}'.format(name, len(atlas)))
    else:
        exit()

    CheckExternelUtils()

    db = TileSqlLiteDB(options.DBDIR)
    tm = TileManager(WDIR, db)
    mapcnt = 1

    for singlemap in atlas:
        ti = ChartInfo(singlemap)
        logger.info('Start UpdateTile for map {} / {}:'.format(mapcnt, len(atlas)))
        mapcnt += 1
        starttime = time.time()
        logger.info(ti)
        tm.UpdateTiles(ti, options.update)
        stoptime = time.time()
        logger.info('time: {} s'.format(int(stoptime - starttime)))
        logger.info('tiles skipped          {}'.format(tm.tileskipped))
        logger.info('tiles merged           {}'.format(tm.tilemerged))
        logger.info('tiles downloaded       {}'.format(tm.tiledownloaded))
        logger.info('tiles download skipped {}'.format(tm.tiledownloadskipped))
        logger.info('tiles download error   {}'.format(tm.tiledownloaderror))

    logger.info('ready')
    db.CloseDB()
    return


if __name__ == "__main__":
    exit(main())
