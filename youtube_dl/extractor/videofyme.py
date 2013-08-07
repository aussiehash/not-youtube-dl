import re
import xml.etree.ElementTree

from .common import InfoExtractor
from ..utils import (
    find_xpath_attr,
    determine_ext,
)

class VideofyMeIE(InfoExtractor):
    _VALID_URL = r'https?://(www.videofy.me/.+?|p.videofy.me/v)/(?P<id>\d+)(&|#|$)'
    IE_NAME = u'videofy.me'

    _TEST = {
        u'url': u'http://www.videofy.me/thisisvideofyme/1100701',
        u'file':  u'1100701.mp4',
        u'md5': u'2046dd5758541d630bfa93e741e2fd79',
        u'info_dict': {
            u'title': u'This is VideofyMe',
            u'description': None,
            u'uploader': u'VideofyMe',
            u'uploader_id': u'thisisvideofyme',
        },
        
    }

    def _real_extract(self, url):
        mobj = re.match(self._VALID_URL, url)
        video_id = mobj.group('id')
        config_xml = self._download_webpage('http://sunshine.videofy.me/?videoId=%s' % video_id,
                                            video_id)
        config = xml.etree.ElementTree.fromstring(config_xml.encode('utf-8'))
        video = config.find('video')
        sources = video.find('sources')
        url_node = find_xpath_attr(sources, 'source', 'id', 'HQ on')
        if url_node is None:
            url_node = find_xpath_attr(sources, 'source', 'id', 'HQ off')
        video_url = url_node.find('url').text

        return {'id': video_id,
                'title': video.find('title').text,
                'url': video_url,
                'ext': determine_ext(video_url),
                'thumbnail': video.find('thumb').text,
                'description': video.find('description').text,
                'uploader': config.find('blog/name').text,
                'uploader_id': video.find('identifier').text,
                'view_count': re.search(r'\d+', video.find('views').text).group(),
                }
