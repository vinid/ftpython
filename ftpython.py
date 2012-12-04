import os, sys, getpass
from ftplib import FTP

DATASIZE = 8192

toret = "-help"
if(sys.argv[1] == toret):
    helplo()

if(len(sys.argv) != 5):
    print 'general usage: %s <host> <username> <directory> <file>' % (sys.argv[0])
    print '%s -help for help\n' % (sys.argv[0])
    exit(1)

host, username, remotedir, ufile = sys.argv[1:]
password = getpass.getpass(prompt='FTP password: ', stream=None)

ftp = FTP(host)
ftp.login(username, password)

ftp.cwd(remotedir)
ftp.voidcmd("TYPE I")

filedesc = open(ufile, 'rb')

stocked, stsize = ftp.ntransfercmd('STOR %s' % os.path.basename(ufile))
size = os.stat(ufile)[6]

bytes_stored = 0

while 1:
    buf = filedesc.read(DATASIZE)
    if not buf:
        break
    stocked.sendall(buf)
    bytes_stored += len(buf)
    tupl = (bytes_stored, ufile, size)
    print '\rSent {0}  of {1} -> size {2} bytes'.format(*tupl)
    sys.stdout.flush()

print "Upload Complete"

stocked.close()
filedesc.close()
ftp.voidresp()
ftp.quit()

#Function


def helplo():
    print "\n******************************************************"
    print "\nThis is a simple script that loads a file to an FTP server."
    print "first parameter is the host (ex = ftp.something.com)"
    print "second parameter is your username"
    print "third parameter is the file you want to upload"
    print "\n******************************************************"
