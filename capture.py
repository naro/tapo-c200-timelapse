import time
import subprocess
import datetime
import os
import timelapseconfig

# prepare the output folder
write_path = timelapseconfig.output_dir + datetime.datetime.today().strftime(timelapseconfig.daily_foldername_date_formatstring)
if not os.path.exists(write_path):
    os.makedirs(write_path)

if timelapseconfig.symlink_latest:
    if not os.path.exists(os.path.dirname(timelapseconfig.symlink_latest)):
        os.makedirs(os.path.dirname(timelapseconfig.symlink_latest))

print ("staring capture")
starttime = datetime.datetime.now().timestamp()
while datetime.datetime.now().timestamp() < starttime + timelapseconfig.cronjob_repeat_time:
    cycle_starttime = datetime.datetime.now().timestamp()
    file_name = write_path + "/" + str(int(datetime.datetime.now().timestamp())) + ".png"
    print(file_name)
    cmd = [timelapseconfig.ffmpeg] + timelapseconfig.ffmpeg_cmdline + [file_name]
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode != 0:
        print('Command:', ' '.join(cmd))
        print('Unable to take a capture. Returncode:', result.returncode)
    else:
        if timelapseconfig.symlink_latest:
            if os.path.islink(timelapseconfig.symlink_latest):
                os.unlink(timelapseconfig.symlink_latest)
            os.symlink(file_name, timelapseconfig.symlink_latest)
    while datetime.datetime.now().timestamp() < cycle_starttime + timelapseconfig.delay_between_images:
        time.sleep(0.1)
