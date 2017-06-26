# Debian with my user and sudo
#


FROM      debian
LABEL Description="Just to start and up-to-date debian with a test login as sudo" Version="1.0"
RUN apt-get update && apt-get install -y sudo vim perl man curl bzip2
RUN useradd -c "Test user" -s /bin/bash -m -d /home/test -p '$6$4eQHl/BR$xfLzB1FwnLUIoqPz1y.z5saCJckFoZhW.4D5W84CRr459Pf8SxzHUwlgOJj0qFw/VtcnZD4usk1j3EVMsYYCq0' test 
RUN usermod -G sudo test
