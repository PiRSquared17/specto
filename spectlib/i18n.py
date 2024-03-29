# Copyright (C) 2000-2003 by the Free Software Foundation, Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import sys
import time
import gettext
from types import StringType, UnicodeType

from spectlib.i18n_safedict import SafeDict

_translation = None

MESSAGES_DIR = "%s/share/locale" % sys.prefix


def set_language(language=None):
    global _translation
    if language is not None:
        language = [language]
    try:
        _translation = gettext.translation('specto', MESSAGES_DIR,
                                           language)
    except IOError:
        # The selected language was not installed in messages, so fall back to
        # untranslated English.
        _translation = gettext.NullTranslations()

def get_translation():
    return _translation

def set_translation(translation):
    global _translation
    _translation = translation


# Set up the global translation based on environment variables.  Mostly used
# for command line scripts.
if _translation is None:
    set_language()

##this small part was taken from gajim's i18n.py, because the mailman one was pure CRAP. It was impossible use strings that had % characters in them.
def _(s):
    if s == '':
        return s
    return _translation.ugettext(s)


# def ctime(date):
#     # Don't make these module globals since we have to do runtime translation
#     # of the strings anyway.
#     daysofweek = [
#         _('Mon'), _('Tue'), _('Wed'), _('Thu'),
#         _('Fri'), _('Sat'), _('Sun')
#         ]
#     months = [
#         '',
#         _('Jan'), _('Feb'), _('Mar'), _('Apr'), _('May'), _('Jun'),
#         _('Jul'), _('Aug'), _('Sep'), _('Oct'), _('Nov'), _('Dec')
#         ]

#     tzname = _('Server Local Time')
#     if isinstance(date, StringType):
#         try:
#             year, mon, day, hh, mm, ss, wday, ydat, dst = time.strptime(date)
#             tzname = time.tzname[dst and 1 or 0]
#         except ValueError:
#             try:
#                 wday, mon, day, hms, year = date.split()
#                 hh, mm, ss = hms.split(':')
#                 year = int(year)
#                 day = int(day)
#                 hh = int(hh)
#                 mm = int(mm)
#                 ss = int(ss)
#             except ValueError:
#                 return date
#             else:
#                 for i in range(0, 7):
#                     wconst = (1999, 1, 1, 0, 0, 0, i, 1, 0)
#                     if wday.lower() == time.strftime('%a', wconst).lower():
#                         wday = i
#                         break
#                 for i in range(1, 13):
#                     mconst = (1999, i, 1, 0, 0, 0, 0, 1, 0)
#                     if mon.lower() == time.strftime('%b', mconst).lower():
#                         mon = i
#                         break
#     else:
#         year, mon, day, hh, mm, ss, wday, yday, dst = time.localtime(date)
#         tzname = time.tzname[dst and 1 or 0]

#     wday = daysofweek[wday]
#     mon = months[mon]
#     return _('%(wday)s %(mon)s %(day)2i %(hh)02i:%(mm)02i:%(ss)02i '
#              '%(tzname)s %(year)04i')
