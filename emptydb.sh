psql -d postgres -c "drop database slstracker;"
psql -d postgres -c "create database slstracker;"
psql -d postgres -c "alter database slstracker owner to slstracker;"
psql -d slstracker -U slstracker -f schema.sql
psql -d slstracker -U slstracker -f testdata.sql
