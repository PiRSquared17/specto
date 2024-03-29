# -*- coding: UTF8 -*-

# Specto , Unobtrusive event notifier
#
#       watch_mail_imap.py
#
# Copyright (c) 2005-2007, Jean-François Fortin Tam

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

from spectlib.watch import Watch

import poplib, email
import os
from socket import error
from spectlib.i18n import _
import thread
import gtk, time
import string

class Mail_watch(Watch):
    """ 
    Watch class that will check if you recevied a new mail on your pop3 account. 
    """
    updated = False
    actually_updated = False
    oldMsg = 0
    newMsg = 0
    type = 1
    prot = 0
    mail_info = []
    
    def __init__(self, refresh, host, username, password, ssl, specto, id,  name = _("Unknown Mail Watch")):
        Watch.__init__(self, specto)
        self.name = name
        self.refresh = refresh
        self.host = host
        self.user = username
        self.password = password
        self.id = id
        self.error = False
        self.ssl = ssl
                
        cacheSubDir__ = os.environ['HOME'] + "/.specto/cache/"
        if not os.path.exists(cacheSubDir__):
            os.mkdir(cacheSubDir__)
        cacheFileName = "pop" + name + ".cache"
        self.cacheFullPath_ = os.path.join(cacheSubDir__, cacheFileName)
        
    def dict_values(self):
        return { 'name': self.name, 'refresh': self.refresh, 'username': self.user, 'password':self.password, 'host':self.host, 'ssl':self.ssl, 'type':1, 'prot':0 }
        
    def start_watch(self):
        """ Start the watch. """
        self.thread_update()
        
    def _real_update(self):
        lock = thread.allocate_lock()
        lock.acquire()
        t=thread.start_new_thread(self.update,(lock,))
        while lock.locked():
            while gtk.events_pending():
                gtk.main_iteration()
            time.sleep(0.05)
        while gtk.events_pending():
            gtk.main_iteration()
        
    def thread_update(self):
        if not self.specto.connection_manager.connected():
            self.specto.logger.log(_("No network connection detected"),
                                   "info", self.__class__)
            self.specto.connection_manager.add_callback(self._real_update)
            self.specto.mark_watch_busy(False, self.id)
        else :
            self._real_update()
        
    def update(self, lock):
        """ Check for new mails on your pop3 account. """
        self.error = False
        self.specto.mark_watch_busy(True, self.id)
        self.specto.logger.log(_("Updating watch: \"%s\"") % self.name, "info", self.__class__)
        
        try:
            if str(self.ssl) == 'True':
                s = poplib.POP3_SSL(self.host)
            else:
                s = poplib.POP3(self.host)
        except error, e:
            self.error = True
            self.specto.logger.log(_("Watch: \"%s\" has error: ") % self.name + str(e), "error", self.__class__)
        else:
            try:
                s.user(self.user)
                s.pass_(self.password)
                self.oldMsg = len(s.list()[1])
                self.newMsg = 0
                                
                if self.oldMsg > 0:
                    i=1
                    while i < self.oldMsg+1:
                        #str_msg = string.join(s.top(i, 0)[1], "\n")
                        #msg = email.message_from_string(str_msg)
                        #print format % (i, msg["From"], msg["Subject"])
                        info = string.split(s.uidl(i))[2] #get unique info
                        if info not in self.mail_info: #check if it is a new email or just unread
                            self.actually_updated=True
                            self.mail_info.append(info)
                            self.newMsg+=1
                        i+=1
                    #print self.mail_info
                s.quit()
                        
                #if self.newMsg > int(self.check_old()):
                #    self.actually_updated = True
                #self.write_new()
                
            except poplib.error_proto, e:
                self.error = True
                self.specto.logger.log(_("Watch: \"%s\" has error: ") % self.name + str(e), "error", self.__class__)

        self.specto.mark_watch_busy(False, self.id)
        Watch.update(self, lock)
        
    def check_old(self):
        """ Check how many messages there were last time. """
        if (os.path.exists(self.cacheFullPath_)):
            f = file(self.cacheFullPath_, "r")
            oldMsg = f.read()
            f.close()
        else:
            oldMsg = 0
        
        return oldMsg
    
    def write_new(self):
        """ Write the new number of messages in the cache file. """
        f = file(self.cacheFullPath_, "w")
        f.write(str(self.newMsg))
        f.close()
        
    def set_username(self, username):
        """ Set the username for the watch. """
        self.user = username
        
    def set_password(self, password):
        """ Set the password for the watch. """
        self.password = password
        
    def set_host(self, host):
        """ Set the host for the watch. """
        self.host = host
        
    def set_ssl(self, ssl):
        """ Use ssl support. """
        self.ssl = ssl
