############################################################
# /home/peter/_work/CRISMA-sw/indicators-py/Makefile
# Peter Kutschera, Thu Feb  6 12:42:00 2014
# Time-stamp: "2014-02-07 10:04:12 peter"
# 
# Peter.Kutschera@ait.ac.at
#
#    Copyright (C) 2014  AIT / Austrian Institute of Technology
#    http://www.ait.ac.at
# 
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as
#    published by the Free Software Foundation, either version 2 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
# 
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/gpl-2.0.html
#############################################################

WPS_DIR = /usr/local/wps/indicators
WEB_DIR = /home/crisma/public_html/indicators

install: install_wps install_web

install_wps:
	@echo "Setup WPS processes"
	[ -d $(WPS_DIR) ] || mkdir $(WPS_DIR)
	[ -d $(WPS_DIR)/processes ] || mkdir $(WPS_DIR)/processes
	install -p wps/pywps.cfg $(WPS_DIR)
	install -p wps/processes/__init__.py $(WPS_DIR)/processes
	install -p wps/processes/lifeIndicator.py $(WPS_DIR)/processes
	install -p wps/processes/deathsIndicator.py $(WPS_DIR)/processes

install_web:
	@echo "Setup web page"
	[ -d $(WEB_DIR) ] || mkdir $(WEB_DIR)
	install -p web/pywps.cgi $(WEB_DIR)
	install -p web/jquery-1.10.2.min.js $(WEB_DIR)
	install -p web/indicators.html $(WEB_DIR)
	install -p web/OrionListener.py $(WEB_DIR)

clean:
	rm -rf $(WPS_DIR) $(WEB_DIR)

.PHONY: install clean
