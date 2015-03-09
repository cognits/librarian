"""
downloads.py: routes related to downloads

Copyright 2014, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import os
import logging
from datetime import datetime

from bottle import request, view, redirect, default_app

from ..core import archive
from ..core import metadata
from ..core import downloads

from ..lib.i18n import i18n_path, lazy_gettext as _
from ..lib.pager import Pager

__all__ = ('app', 'list_downloads', 'manage_downloads',)

PER_PAGE = 20


app = default_app()


@view('downloads', vals={})
def list_downloads():
    """ Render a list of downloaded content """
    conf = request.app.config
    cover_dir = conf['content.covers']
    selection = request.params.get('sel', '1') != '0'
    zipballs = downloads.get_zipballs()
    zipballs = list(reversed(downloads.order_zipballs(zipballs)))
    if zipballs:
        last_zip = datetime.fromtimestamp(zipballs[0][1])
        nzipballs = len(zipballs)
        logging.info('Found %s updates', nzipballs)
    else:
        last_zip = None
        nzipballs = 0
        logging.info('No updates found')
    pager = Pager(zipballs, pid='downloads')
    pager.get_paging_params()
    metas = []
    for z, ts in pager.get_items():
        logging.debug("<%s> getting metas" % z)
        try:
            meta = downloads.get_metadata(z)
            meta['md5'] = downloads.get_md5_from_path(z)
            meta['ftimestamp'] = datetime.fromtimestamp(ts)
            metas.append(metadata.Meta(meta, cover_dir, zip_path=z))
        except downloads.ContentError as err:
            # Zip file is invalid. This means that the file is corrupted or the
            # original file was signed with corrupt data in it. Either way, we
            # don't know what to do with the file so we'll remove it.
            logging.error("<%s> error unpacking: %s" % (z, err))
            os.unlink(z)
            continue
    archive.get_replacements(metas)

    vals = dict(request.params)
    vals.update({'pp': pager.per_page})

    return dict(vals=vals, metadata=metas, selection=selection, pager=pager,
                nzipballs=nzipballs, last_zip=last_zip)


@view('downloads_error')  # TODO: Add this view
def manage_downloads():
    """ Manage the downloaded content """
    forms = request.forms
    action = forms.get('action')
    file_list = forms.getall('selection')
    if not action:
        # Translators, used as error message shown to user when wrong action
        # code is submitted to server
        return {'error': _('Invalid action, please use one of the form '
                           'buttons.')}
    if action == 'add':
        archive.add_to_archive(file_list)
    if action == 'delete':
        downloads.remove_downloads(file_list)
    if action == 'deleteall':
        downloads.remove_downloads()
    redirect(i18n_path('/downloads/'))

