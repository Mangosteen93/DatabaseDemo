#由windows生成的脚本拷贝到linux下，需要先执行dos2unix

file_name="$0"

#resolve links - $0 may be a softlink
while [ -h "$file_name" ] ; do
  ls=`ls -ld "$file_name"`
  link=`expr "$ls" : '.*-> \(.*\)$'`
  if expr "$link" : '.*/.*' > /dev/null; then
    file_name="$link"
  else
    file_name=`dirname "$file_name"`/"$link"
  fi
done

file_path=`dirname "$file_name"`
file_absolute_path=`cd "$file_path" ; pwd`

cd $file_absolute_path
/watcher/app/java/jdk1.8.0_121/bin/java -jar localip_cron.jar
