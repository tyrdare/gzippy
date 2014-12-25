import sys
import os
import gzip
import argparse


BUFRSZ = 1048576

def file_ok(filename):

    # if user overrode the default logfile name then we have to check that the directory exists
    directory = os.path.split(filename)[0]
    print directory
    if os.path.exists(directory):
        print "% s exists" % directory
    else:
        raise Exception("%s does not exist" % directory)
    
    if os.path.isdir(directory):
        print "%s is a directory" % directory
    else:
        raise Exception("%s is not a directory" % directory)
    
    # attempt to open the file in write mode
    try:
        print "Opening %s" % filename
        f = open(filename, 'a')
        f.close()
        return True
    except Exception as e:
        print e.args[0]
        return False

        
if __name__ == "__main__":

    
    parser = argparse.ArgumentParser()

    parser.add_argument("src", help="source(path and filename to gzip)")
    parser.add_argument(
        "--dest",
        help="Optional destination (path and filename), else source filename + .gz and current directory is used"
    )
    args = parser.parse_args()
    print args.dest
    

    
    
    gz_filename = None    
    # see if an output file name was provided and set the gzip filename to that
    if args.dest is not None and args.dest != '':
        if file_ok(args.dest):
            # wait - did they put the .gz ending on the filename?
            if not args.dest.endswith('.gz'):
                gz_filename = args.dest + '.gz'
            else:
                # Yes, they did
                gz_filename = args.dest
            
        else:
            # The destination filename provided failed the open() test
            raise Exception('%s could not be opened' % gz_filename)
    else:
        # Otherwise, use the current directory and filename as destination
        # and the file is "remote"
        path, fname = os.path.split(args.src)
        if path != '':
            gz_filename = fname + 'gz'
        else:
            gz_filename = args.src + '.gz'
            
    gz_writer = gzip.open(gz_filename, 'wb')
                            
    # now try to open the source file to read it.
    content_reader = os.open(args.src, os.O_RDONLY|os.O_BINARY)
    buffer = os.read(content_reader, BUFRSZ)
    while buffer != '':
        gz_writer.write(buffer)
        buffer = os.read(content_reader, BUFRSZ)
    gz_writer.close()
    content_reader.close()
