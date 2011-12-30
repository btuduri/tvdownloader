#!/usr/bin/env python
#
# smooth-dl - download videos served using Smooth Streaming technology
#
# Copyright (C) 2010  Antonio Ospite <ospite@studenti.unina.it>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# TODO:
#  - Handle HTTP errors:
#       "Connection reset by peer"
#       "Resource not  available"
#       "Gateway Time-out"
# - Support more Manifest formats:
#       WaveFormatEx attribute instead of PrivateCodecdata
#       'd' and other attributes in chunk element ('i', 's', 'q')
#
# basically, write a proper implementation of manifest parsing and chunk
# downloading


__description = "Download videos served using Smooth Streaming technology"
__version = "0.x"
__author_info = "Written by Antonio Ospite http://ao2.it"

import os
import sys
import xml.etree.ElementTree as etree
import urllib2
import struct
import tempfile
from optparse import OptionParser


def get_chunk_data(data):

    moof_size = struct.unpack(">L", data[0:4])[0]
    mdat_size = struct.unpack(">L", data[moof_size:moof_size + 4])[0]

    data_start = moof_size + 4 + len('mdat')
    data_size = mdat_size - 4 - len('mdat')

    #print len(data[data_start:]), \
    #        len(data[data_start:data_start + data_size]), data_size

    assert(len(data[data_start:]) == data_size)

    return data[data_start:data_start + data_size]


def hexstring_to_bytes(hex_string):
    res = ""
    for i in range(0, len(hex_string), 2):
            res += chr(int(hex_string[i:i + 2], 16))

    return res


def write_wav_header(out_file, fmt, codec_private_data, data_len):

    extradata = hexstring_to_bytes(codec_private_data)

    fmt['cbSize'] = len(extradata)
    fmt_len = 18 + fmt['cbSize']
    wave_len = len("WAVEfmt ") + 4 + fmt_len + len('data') + 4

    out_file.write("RIFF")
    out_file.write(struct.pack('<L', wave_len))
    out_file.write("WAVEfmt ")
    out_file.write(struct.pack('<L', fmt_len))
    out_file.write(struct.pack('<H', fmt['wFormatTag']))
    out_file.write(struct.pack('<H', fmt['nChannels']))
    out_file.write(struct.pack('<L', fmt['nSamplesPerSec']))
    out_file.write(struct.pack('<L', fmt['nAvgBytesPerSec']))
    out_file.write(struct.pack('<H', fmt['nBlockAlign']))
    out_file.write(struct.pack('<H', fmt['wBitsPerSample']))
    out_file.write(struct.pack('<H', fmt['cbSize']))
    out_file.write(extradata)
    out_file.write("data")
    out_file.write(struct.pack('<L', data_len))


def get_manifest(base_url, dest_dir=tempfile.gettempdir(),
        manifest_file='Manifest'):
    """Returns the manifest and the new URL if this is changed"""

    if os.path.exists(dest_dir) == False:
        os.mkdir(dest_dir, 0755)

    if base_url.startswith('http://'):

        manifest_url = base_url
        if not manifest_url.lower().endswith(('/manifest', '.ismc', '.csm')):
            manifest_url += '/Manifest'

        response = urllib2.urlopen(manifest_url)
        data = response.read()

        manifest_path = os.path.join(dest_dir, manifest_file)
        f = open(manifest_path, "w")
        f.write(data)
        f.close()
    else:
        manifest_path = base_url

    manifest = etree.parse(manifest_path)

    version = manifest.getroot().attrib['MajorVersion']
    if version != "2":
        raise Exception('Only Smooth Streaming version 2 supported')

    try:
        # if some intermediate client Manifest is used, like in Rai Replay
        clip = manifest.find("Clip")
        actual_manifest_url = clip.attrib["Url"]
        base_url = actual_manifest_url.lower().replace("/manifest", "")
    except:
        pass

    return (manifest, base_url)


def print_manifest_info(manifest):

    streams = manifest.findall('//StreamIndex')

    for i, s in enumerate(streams):
        stream_type = s.attrib["Type"]
        url = s.attrib["Url"]

        print "Stream: %s Type: %s" % (i, stream_type)

        print "\tQuality Levels:"
        qualities = s.findall("QualityLevel")
        for i, q in enumerate(qualities):
            bitrate = q.attrib["Bitrate"]
            fourcc = q.attrib["FourCC"]

            if stream_type == "video":
                size = "%sx%s" % (q.attrib["MaxWidth"], q.attrib["MaxHeight"])
                print "\t%2s: %4s %10s @ %7s bps" % (i, fourcc, size, bitrate)
            if stream_type == "audio":
                channels = q.attrib["Channels"]
                sampling_rate = q.attrib["SamplingRate"]
                bits_per_sample = q.attrib["BitsPerSample"]
                print "\t%2s: %4s %sHz %sbits %sch @ %7s bps" % (i, fourcc,
                        sampling_rate, bits_per_sample, channels, bitrate)

    print


def download_chunks(base_url, manifest, stream_index, quality_level, dest_dir):

    if os.path.exists(dest_dir) == False:
        os.mkdir(dest_dir, 0755)

    stream = manifest.findall('//StreamIndex')[stream_index]

    quality = stream.findall("QualityLevel")[quality_level]
    bitrate = quality.attrib["Bitrate"]

    # Assume URLs are in this form:
    # Url="QualityLevels({bitrate})/Fragments(video={start time})"
    url = stream.attrib["Url"]

    chunks_quality = url.split('/')[0].replace("{bitrate}", bitrate)
    chunks_dest_dir = os.path.join(dest_dir, chunks_quality)
    if os.path.exists(chunks_dest_dir) == False:
        os.mkdir(chunks_dest_dir, 0755)

    chunks = stream.findall("c")
    data_size = 0
    print "\nDownloading Stream %d" % stream_index
    print "\tChunks %10d/%-10d" % (0, len(chunks)), "\r",
    sys.stdout.flush()
    for i, c in enumerate(chunks):
        t = c.attrib["t"]

        chunk_name = url.split('/')[1].replace("{start time}", t)
        chunk_file = os.path.join(dest_dir,  chunks_quality, chunk_name)

        if os.path.exists(chunk_file) == False:
            chunk_url = base_url + '/' + chunks_quality + '/' + chunk_name
            response = urllib2.urlopen(chunk_url)
            data = response.read()

            f = open(chunk_file, "wb")
            f.write(data)
            f.close()
        else:
            f = open(chunk_file, "rb")
            data = f.read()
            f.close()

        data_size += len(data)
        print "\tChunks %10d/%-10d" % (i + 1, len(chunks)), "\r",
        sys.stdout.flush()
    print "\tDownloaded size:", data_size


def rebuild_stream(manifest, stream_index, quality_level, src_dir,
        dest_file_name, final_dest_file=None):

    if final_dest_file == None:
        final_dest_file = dest_file_name

    stream = manifest.findall('//StreamIndex')[stream_index]

    quality = stream.findall("QualityLevel")[quality_level]
    bitrate = quality.attrib["Bitrate"]

    # Assume URLs are in this form:
    # Url="QualityLevels({bitrate})/Fragments(video={start time})"
    url = stream.attrib["Url"]

    chunks_quality = url.split('/')[0].replace("{bitrate}", bitrate)
    chunks_src_dir = os.path.join(src_dir, chunks_quality)

    dest_file = open(dest_file_name, "wb")

    chunks = stream.findall("c")
    data_size = 0
    print "\nRebuilding Stream %d" % stream_index
    print "\tChunks %10d/%-10d" % (0, len(chunks)), "\r",
    sys.stdout.flush()
    for i, c in enumerate(chunks):
        t = c.attrib["t"]

        chunk_name = url.split('/')[1].replace("{start time}", t)
        chunk_file = os.path.join(chunks_src_dir, chunk_name)

        f = open(chunk_file, "rb")
        data = get_chunk_data(f.read())
        f.close()
        dest_file.write(data)
        data_size += len(data)
        print "\tChunks %10d/%-10d" % (i + 1, len(chunks)), "\r",
        sys.stdout.flush()

    # Add a nice WAV header
    if stream.attrib['Type'] == "audio":
        codec_private_data = quality.attrib['CodecPrivateData']

        fmt = {}
        fmt['wFormatTag'] = int(quality.attrib['AudioTag'])
        fmt['nChannels'] = int(quality.attrib['Channels'])
        fmt['nSamplesPerSec'] = int(quality.attrib['SamplingRate'])
        fmt['nAvgBytesPerSec'] = int(quality.attrib['Bitrate']) / 8
        fmt['wBitsPerSample'] = int(quality.attrib['BitsPerSample'])
        fmt['nBlockAlign'] = int(quality.attrib['PacketSize'])
        fmt['cbSize'] = 0

        f = open(final_dest_file, "wb")
        write_wav_header(f, fmt, codec_private_data, data_size)
        dest_file.close()
        dest_file = open(dest_file_name, "rb")
        f.write(dest_file.read())
        f.close()
        dest_file.close()

    print
    print "Stream %d, actual data size: %d\n" % (stream_index, data_size)


def calc_tracks_delay(manifest, stream1_index, stream2_index):
    streams = manifest.findall('//StreamIndex')

    s1 = streams[stream1_index]
    s2 = streams[stream2_index]

    s1_start_chunk = s1.find("c")
    s2_start_chunk = s2.find("c")

    s1_start_time = int(s1_start_chunk.attrib['t'])
    s2_start_time = int(s2_start_chunk.attrib['t'])

    s1_timescale = float(s1.attrib['TimeScale'])
    s2_timescale = float(s2.attrib['TimeScale'])

    # calc difference in seconds
    delay = s2_start_time / s2_timescale - \
            s1_start_time / s1_timescale

    return delay


def get_clip_duration(manifest):
    # TODO: use <Clip ClipBegin="" ClipEnd=""> if Duration is not available
    duration = manifest.getroot().attrib['Duration']

    return float(duration) / 10000000  # here is the default timescale


def smooth_download(url, manifest, dest_dir=tempfile.gettempdir(),
        video_stream_index=0, audio_stream_index=1,
        video_quality_level=0, audio_quality_level=0,
        chunks_dir=None, download=True,
        out_video_file='_video.vc1', out_audio_file='_audio.raw'):

        if chunks_dir == None:
            chunks_dir = dest_dir

        if download:
            download_chunks(url, manifest, video_stream_index,
                    video_quality_level, chunks_dir)
            download_chunks(url, manifest, audio_stream_index,
                    audio_quality_level, chunks_dir)

        dest_video = os.path.join(dest_dir, out_video_file)
        dest_audio = os.path.join(dest_dir, out_audio_file)

        rebuild_stream(manifest, video_stream_index, video_quality_level,
                chunks_dir, dest_video)
        rebuild_stream(manifest, audio_stream_index, audio_quality_level,
                chunks_dir, dest_audio, dest_audio + '.wav')

        #duration = get_clip_duration(manifest)

        delay = calc_tracks_delay(manifest, video_stream_index,
                audio_stream_index)

        # optionally encode audio to vorbis:
        # ffmpeg -i _audio.raw.wav -acodec libvorbis -aq 60 audio.ogg
        mux_command = ("ffmpeg -i %s \\\n" +
                      "  -itsoffset %f -async 1 -i %s \\\n" +
                      "  -vcodec copy -acodec copy ffout.mkv") % \
                      (dest_video, delay, dest_audio + '.wav')

        print mux_command


def options_parser():
    version = "%%prog %s" % __version
    usage = "usage: %prog [options] <manifest URL or file>"
    parser = OptionParser(usage=usage, version=version,
            description=__description, epilog=__author_info)
    parser.add_option("-i", "--info",
                      action="store_true", dest="info_only",
                      default=False, help="print Manifest info and exit")
    parser.add_option("-m", "--manifest-only",
                      action="store_true", dest="manifest_only",
                      default=False, help="download Manifest file and exit")
    parser.add_option("-n", "--no-download",
                      action="store_false", dest="download",
                      default=True, help="disable downloading chunks")
    parser.add_option("-s", "--sync-delay",
                      action="store_true", dest="sync_delay",
                      default=False, help="show the sync delay between the given streams and exit")
    parser.add_option("-d", "--dest-dir", metavar="<dir>",
                      dest="dest_dir", default=tempfile.gettempdir(),
                      help="destination directory")
    parser.add_option("-c", "--chunks-dir", metavar="<dir>",
                      dest="chunks_dir", default=None,
                      help="directory containing chunks, if different from destination dir")
    parser.add_option("-v", "--video-stream",  metavar="<n>",
                      type="int", dest="video_stream_index", default=0,
                      help="index of the video stream")
    parser.add_option("-a", "--audio-stream", metavar="<n>",
                      type="int", dest="audio_stream_index", default=1,
                      help="index of the audio stream")
    parser.add_option("-q", "--video-quality", metavar="<n>",
                      type="int", dest="video_quality_level", default=0,
                      help="index of the video quality level")
    parser.add_option("-Q", "--audio-quality", metavar="<n>",
                      type="int", dest="audio_quality_level", default=0,
                      help="index of the audio quality level")

    return parser


if __name__ == "__main__":

    parser = options_parser()
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
        parser.exit(1)

    url = args[0]
    manifest, url = get_manifest(url, options.dest_dir)

    if options.manifest_only:
        parser.exit(0)

    if options.sync_delay:
        print calc_tracks_delay(manifest,
                options.video_stream_index,
                options.audio_stream_index)
        parser.exit(0)

    if options.info_only:
        print_manifest_info(manifest)
        parser.exit(0)

    print_manifest_info(manifest)

    smooth_download(url, manifest, options.dest_dir,
            options.video_stream_index, options.audio_stream_index,
            options.video_quality_level, options.audio_quality_level,
            options.chunks_dir, options.download)
