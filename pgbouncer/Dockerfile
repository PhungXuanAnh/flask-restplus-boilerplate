FROM edoburu/pgbouncer:1.9.0

# These below line for fix permission denined with these folder 
USER root
RUN chown -R postgres:root /var/log/pgbouncer
USER postgres

EXPOSE 6432

CMD ["/usr/bin/pgbouncer", "/etc/pgbouncer/pgbouncer.ini"]
