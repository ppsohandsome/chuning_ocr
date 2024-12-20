urls = [
    # 'testvideo/d25.mp4',
    # 'testvideo/d26.mp4',
    # 'testvideo/d27.mp4',
    # 'testvideo/d28.mp4',
    # 'testvideo/d29.mp4',
    # 'testvideo/d30.mp4',
     'rtsp://admin:abcd1234@192.168.1.103:554/h264/ch1/main/av_stream',
     'rtsp://admin:abcd1234@192.168.1.108:554/h264/ch1/main/av_stream',
     'rtsp://admin:abcd1234@192.168.1.129:554/h264/ch1/main/av_stream',
     'rtsp://admin:abcd1234@192.168.1.139:554/h264/ch1/main/av_stream',
     'rtsp://admin:abcd1234@192.168.1.67:554/h264/ch1/main/av_stream',
     'rtsp://admin:abcd1234@192.168.1.79:554/h264/ch1/main/av_stream',

    #'rtsp://admin:abcd1234@192.168.1.103/Streaming/Channels/103?transportmode=unicast',
    #'rtsp://admin:abcd1234@192.168.1.108/Streaming/Channels/103?transportmode=unicast',
    #'rtsp://admin:abcd1234@192.168.1.129/Streaming/Channels/103?transportmode=unicast',
    #'rtsp://admin:abcd1234@192.168.1.139/Streaming/Channels/103?transportmode=unicast',
    #'rtsp://admin:abcd1234@192.168.1.67/Streaming/Channels/103?transportmode=unicast',
    #'rtsp://admin:abcd1234@192.168.1.79/Streaming/Channels/103?transportmode=unicast',
]
def get_id_from_rtsp(url):
    if "192.168.1.103" in url:
        return 39
    elif "192.168.1.108" in url:
        return 43
    elif "192.168.1.129" in url:
        return 65
    elif "192.168.1.139" in url:
        return 75
    elif "192.168.1.67" in url:
        return 3
    elif "192.168.1.79" in url:
        return 15
    else:
        return 0
