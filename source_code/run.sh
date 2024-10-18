#!/usr/bin/with-contenv bashio
bashio::log.info "bashio::log.info -> start !!"

echo $(bashio::config "eladdr")
echo $(bashio::config "elport")
echo $(bashio::config "matteraddr")

echo $(bashio::config "tpcre")
echo $(bashio::config "tpdel")
echo $(bashio::config "tpupd")
echo $(bashio::config "tpope")
echo $(bashio::config "tpres")

. ./venv/bin/activate
python3 main.py $(bashio::config 'eladdr') $(bashio::config 'elport') $(bashio::config 'matteraddr') $(bashio::config "tpcre") $(bashio::config "tpdel") $(bashio::config "tpupd") $(bashio::config "tpope") $(bashio::config "tpres")