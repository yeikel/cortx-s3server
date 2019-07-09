#!/bin/sh -xe
# S3 server start script in deployment environment.
#   Usage: s3startsystem.sh <process FID>
#             where process FID: S3 server process FID generated by halon.


if [ $# -ne 1 ]
then
  echo "Invalid number of arguments passed to the script"
  echo "Usage: s3startsystem.sh <process FID>"
  exit 1
fi

ha_config="/etc/sysconfig/s3server-$1"
if [[ ! -r $ha_config ]]
then
  echo "config file '$ha_config' either doesn't exist or not readable"
  exit 1
else
  source $ha_config
fi

# Ensure default working dir is present
s3_working_dir=`python -c '
import yaml;
print yaml.load(open("/opt/seagate/s3/conf/s3config.yaml"))["S3_SERVER_CONFIG"]["S3_DAEMON_WORKING_DIR"];
' | tr -d '\r\n'
`"/s3server-$1"

mkdir -p $s3_working_dir

# Log dir configured in s3config.yaml
s3_log_dir=`python -c '
import yaml;
print yaml.load(open("/opt/seagate/s3/conf/s3config.yaml"))["S3_SERVER_CONFIG"]["S3_LOG_DIR"];
' | tr -d '\r\n'
`"/s3server-$1"
mkdir -p $s3_log_dir

#set the maximum size of core file to unlimited
ulimit -c unlimited

#Set the open file limit to 10240
ulimit -n 10240

# Start the s3server
export PATH=$PATH:/opt/seagate/s3/bin
local_ep=$MERO_S3SERVER_EP
ha_ep=$MERO_HA_EP
profile_fid="<$MERO_PROFILE_FID>"
process_fid="<$MERO_PROCESS_FID>"
s3port=$MERO_S3SERVER_PORT


# s3server cmd parameters allowing to fake some clovis functionality
# --fake_clovis_writeobj - stub for clovis write object with all zeros
# --fake_clovis_readobj - stub for clovis read object with all zeros
# --fake_clovis_createidx - stub for clovis create idx - does nothing
# --fake_clovis_deleteidx - stub for clovis delete idx - does nothing
# --fake_clovis_getkv - stub for clovis get key-value - read from memory hash map
# --fake_clovis_putkv - stub for clovis put kye-value - stores in memory hash map
# --fake_clovis_deletekv - stub for clovis delete key-value - deletes from memory hash map
# for proper KV mocking one should use following combination
#    --fake_clovis_createidx true --fake_clovis_deleteidx true --fake_clovis_getkv true --fake_clovis_putkv true --fake_clovis_deletekv true


pid_filename='/var/run/s3server.'$1'.pid'
s3server --s3pidfile $pid_filename \
         --clovislocal $local_ep --clovisha $ha_ep \
         --clovisprofilefid $profile_fid --clovisprocessfid $process_fid \
         --s3port $s3port --log_dir $s3_log_dir
