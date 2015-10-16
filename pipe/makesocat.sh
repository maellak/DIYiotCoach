#./pipeLH.sh | socat TCP:192.168.0.243:12345 stdio
./read.php | socat TCP:192.168.0.243:12345 stdio
