#!/usr/bin/env python
# Create a storage pool of 'dir' type

import os
import re
import sys

import libvirt
from libvirt import libvirtError

from src import sharedmod
from utils import xml_builder

required_params = ('poolname', 'pooltype',)
optional_params = {}

def check_pool_create(conn, poolname, logger):
    """Check the result of create storage pool.
    """
    pool_names = conn.listStoragePools()
    logger.info("poolnames is: %s " % pool_names)
    # check thru libvirt that it's really created..
    try:
        pool_names.index(poolname)
    except ValueError:
        logger.info("check_pool_create %s storage pool \
                     is UNSUCCESSFUL!!" % poolname)
        return False
    return True

def display_pool_info(conn, logger):
    """Display current storage pool information"""
    logger.debug("current define storage pool: %s" % conn.listDefinedStoragePools())
    logger.debug("current active storage pool: %s" % conn.listStoragePools())

def create_dir_pool(params):
    """ Create a dir type storage pool from xml"""
    logger = params['logger']
    poolname = params['poolname']
    pooltype = params['pooltype']

    conn = sharedmod.libvirtobj['conn']

    if check_pool_create(conn, poolname, logger):
        logger.error("%s storage pool has already been created" % poolname)
        return 1

    xmlobj = xml_builder.XmlBuilder()
    poolxml = xmlobj.build_pool(params)
    logger.debug("storage pool xml:\n%s" % poolxml)

    try:
        logger.info("Creating %s storage pool" % poolname)
        conn.storagePoolCreateXML(poolxml, 0)
        display_pool_info(conn, logger)
        if check_pool_create(conn, poolname, logger):
            logger.info("creating %s storage pool is SUCCESSFUL!!!" % poolname)
        else:
            logger.info("aa creating %s storage pool is UNSUCCESSFUL!!!" % poolname)
            return 1
    except libvirtError, e:
        logger.error("API error message: %s, error code is %s" \
                     % (e.message, e.get_error_code()))
        return 1

    return 0
