from datetime import datetime, timedelta
import os

import timelapseconfig

yesterdays_date = (datetime.now() - timedelta(1)).strftime(timelapseconfig.daily_foldername_date_formatstring)
yesterdays_folder = timelapseconfig.output_dir + yesterdays_date
filename = yesterdays_date + ".mp4"
output_video_path = timelapseconfig.output_dir_for_daily_timelapse_videos + filename
os.chdir(yesterdays_folder)
returnval = os.system("ffmpeg -r 24 -pattern_type glob -i '*.png' -s hd1080 -vcodec libx264 -g 8 '" + output_video_path + "'")
n = str(int(timelapseconfig.keep_every_nth_picture))

if returnval == 0: #if making the video was successful, delete the files
    os.system("for file in `find " + yesterdays_folder + " -type f | sort | awk 'NR %" + n + " != 0'`; do rm $file ; done")

if timelapseconfig.symlink_latest_daily_dirname:
    if not os.path.isdir(timelapseconfig.symlink_latest_daily_dirname):
        os.makedirs(timelapseconfig.symlink_latest_daily_dirname)
    spath = os.path.join(timelapseconfig.symlink_latest_daily_dirname, filename)
    if os.path.islink(spath):
        os.unlink(spath)
    os.symlink(output_video_path, spath)