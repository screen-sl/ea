#!/bin/bash

# To keep Drill running in embedded mode we
# run it in screen and then run tail command
# until the container is killed. 

screen -d -m /opt/drill/apache-drill-$DRILL_VERSION/bin/drill-embedded

tail -f /dev/null