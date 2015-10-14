import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils


def NFMain():
    utils.addDir('[COLOR yellow]Categories[/COLOR]','http://www.nudeflix.com/browse',44,'','')
    NFList('http://www.nudeflix.com/browse/cover?order=released&page=1',1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def NFCat(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile(r'<li>\s+<a href="/browse/category/([^"]+)">([^<]+)<', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catpage, name in match:
        catpage = catpage.replace(' ','%20')
        catpage = 'http://www.nudeflix.com/browse/category/' + catpage + '/cover?order=released&page=1'
        utils.addDir(name, catpage, 41, '', 1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def NFList(url,page):
    listhtml = utils.getHtml(url, '')
    match = re.compile('href="([^"]+)" class="link">[^"]+?"([^"]+)" alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, name in match:
        videopage = 'http://www.nudeflix.com' + videopage
        utils.addDir(name, videopage, 42, img, '')
    if re.search("<strong>next &raquo;</strong>", listhtml, re.DOTALL | re.IGNORECASE):
        npage = page + 1        
        url = url.replace('page='+str(page),'page='+str(npage))
        utils.addDir('Next Page ('+str(npage)+')', url, 41, '', npage)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def NFScenes(url):
    scenehtml = utils.getHtml(url, '')
    match = re.compile('class="scene">.*?<img class="poster" src="([^"]+)".*?data-src="([^"]+)".*?<div class="description">[^>]+>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(scenehtml)
    scenecount = 1
    for img, sceneurl, desc in match:
        name = 'Scene ' + str(scenecount)
        scenecount = scenecount + 1
        utils.addDownLink(name, sceneurl, 43, img, desc)        
    xbmcplugin.endOfDirectory(utils.addon_handle)


def NFPlayvid(url, name, download=None):
    videourl = url
    if download == 1:
        utils.downloadVideo(videourl, name)
    else:
        iconimage = xbmc.getInfoImage("ListItem.Thumb")
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
        xbmc.Player().play(videourl, listitem)
