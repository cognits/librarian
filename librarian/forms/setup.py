"""
setup.py: Setup wizard forms

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import datetime
import pytz

from bottle_utils.i18n import lazy_gettext as _

from ..lib import forms
from ..utils.lang import UI_LANGS, DEFAULT_LOCALE


class SetupLanguageForm(forms.Form):
    # Translators, used as label for language
    language = forms.SelectField(_('Language'),
                                 value=DEFAULT_LOCALE,
                                 validators=[forms.Required()],
                                 choices=UI_LANGS)


class SetupDateTimeForm(forms.Form):
    HOURS = [(i, i) for i in range(24)]
    MINUTES = [(i, str(i).zfill(2)) for i in range(60)]
    TIMEZONES = [(tzname, tzname) for tzname in pytz.common_timezones]
    DEFAULT_TIMEZONE = pytz.common_timezones[0]
    # Translators, used as label for date and time setup
    date = forms.DateField(_("Date"),
                           value=lambda: datetime.date.today().isoformat(),
                           validators=[forms.Required()],
                           _class="date")
    # Translators, used as label for date and time setup
    hour = forms.SelectField(_("Hour"),
                             value=lambda: datetime.datetime.now().hour,
                             validators=[forms.Required()],
                             choices=HOURS)
    # Translators, used as label for date and time setup
    minute = forms.SelectField(_("Minute"),
                               value=lambda: datetime.datetime.now().minute,
                               validators=[forms.Required()],
                               choices=MINUTES)
    # Translators, used as label for date and time setup
    timezone = forms.SelectField(_("Timezone"),
                                 value=DEFAULT_TIMEZONE,
                                 validators=[forms.Required()],
                                 choices=TIMEZONES)
