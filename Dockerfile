
FROM kingarthurxu/baas
MAINTAINER ArthurXu <qingyu.xu@veritas.com>

ENV BAAS_VERSION=1.1
ENV BAAS_DATE=20181225

ADD ./ /baas

VOLUME /baas
EXPOSE 5000
EXPOSE 5001
WORKDIR /baas

CMD ["/usr/bin/bash", "run.sh"]