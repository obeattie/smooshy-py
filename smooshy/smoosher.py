from __future__ import with_statement # Yes, yes, I know...
import decimal, fcntl, os, shutil, simplejson, sys, urllib2, urlparse

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import multipart_handler

# --- Smoosher --- #

ACCEPTED_FILE_TYPES = ('jpeg', 'jpg', 'png')

opener = urllib2.build_opener(multipart_handler.MultipartPostHandler)

def saving_percent(original_size, replacement_size):
    reduction = float(replacement_size) / float(original_size)
    reduction = reduction * 100
    reduction = decimal.Decimal(str(reduction))
    reduction = reduction.quantize(decimal.Decimal('0.00'))
    return decimal.Decimal('100') - reduction

class SmushItException(Exception):
    pass

class SmoosherFile(file):
    """File subclass that provides locking and unlocking when used inside a
       'with' statement."""
    def __enter__(self, *args, **kwargs):
        fcntl.flock(self, fcntl.LOCK_EX)
        return super(SmoosherFile, self).__enter__(*args, **kwargs)
    
    def __exit__(self, *args, **kwargs):
        if hasattr(self, 'backup'):
            self.restore_backup()
        
        fcntl.flock(self, fcntl.LOCK_UN)
        return super(SmoosherFile, self).__exit__(*args, **kwargs)
    
    def create_backup(self):
        """Backs up this file, by creating a copy with a .backup extension."""
        if not hasattr(self, 'backup'):
            # Don't create another if a backup already exists
            backup_path = (self.name + '.backup')
            shutil.copy2(self.name, backup_path)
            self.backup = SmoosherFile(backup_path)
    
    def destroy_backup(self):
        """Destroys the backup file."""
        os.remove(self.backup.name)
        del self.backup
    
    def restore_backup(self):
        """Restores the backup file."""
        shutil.copy2(self.backup.name, self.name)
        self.destroy_backup()

class Smoosher(object):
    def __init__(self, original_path, *args, **kwargs):
        self.original = SmoosherFile(original_path)
        return super(Smoosher, self).__init__(*args, **kwargs)
    
    def get_smooshed(self):
        """Sends the original file to smoosh.it and returns the resulting data
           as a file-like object (StringIO)."""
        response = opener.open('http://smush.it/ws.php', {
            'files': self.original,
        }).read()
        response = simplejson.loads(response)
        
        # If smush.it reported an error, raise it
        if 'error' in response:
            raise SmushItException, response['error']
        
        result = urlparse.urljoin('http://smush.it', response['dest'])
        
        # Download the smushed file and return it in a StringIO
        return StringIO(urllib2.urlopen(result).read())
    
    def smoosh(self):
        """Smooshes the file:
           
           1) Creates a backup of the file (in case anything goes awry).
           2) Sends the file to smoosh.it, and saves the result.
           3) Compares the sizes of both files (the original and the smooshed)
              If the smooshed file is smaller, the original is overwritten.
              If the smooshed file is not smaller, the backup is restored.
           4) If any any errors occur, the backup is restored, so no damaged
              data can (in theory) be left lying around.
        """
        original_size = os.path.getsize(self.original.name)
        bytes_saved = 0
        
        # Man, I love the with statement...
        with self.original:
            try:
                print 'Smooshing %s...' % self.original.name
                self.original.create_backup()
                
                smooshed = self.get_smooshed()
                replacement = SmoosherFile((self.original.name + '.new'), 'w')
                replacement.write(smooshed.read())
                replacement.flush()
                replacement_size = os.path.getsize(replacement.name)
                
                if not replacement_size < original_size:
                    raise SmushItException, 'No savings'
                
                # Store the size reduction
                bytes_saved = original_size - replacement_size
                # Calculate how much smaller the smooshed file is
                reduction = saving_percent(original_size, replacement_size)
                # Destroy the backup
                self.original.destroy_backup()
                # Move the replacment to overwrite the original
                os.remove(self.original.name)
                shutil.move(replacement.name, self.original.name)
                # Print a success message
                print '  WIN: Smooshed file %s%% smaller :)' % reduction
            
            except SmushItException, e:
                if e.message == 'No savings':
                    # Restore backup, destroy replacment, and print fail notice
                    self.original.restore_backup()
                    # os.remove(replacement.name)
                    print '  FAIL: Smooshed file not smaller. Backup restored.'
                else:
                    print '  FAIL: Smooshing error. Backup restored.'
                    raise
        
        return (original_size, bytes_saved)

def recursive_smoosher(roots):
    """Recursively smooshes its way through a directory of files."""
    files_processed = 0
    total_originals = 0
    total_saved = 0
    
    for root in roots:
        if os.path.isdir(root):
            # The root is a directory, so process everything under it
            for base, dirs, files in os.walk(root):
                for name in files:
                    if name.rsplit('.', 1)[-1].lower() in ACCEPTED_FILE_TYPES:
                        result = Smoosher(os.path.join(base, name)).smoosh()
                        files_processed += 1
                        total_originals += result[0]
                        total_saved += result[1]
        else:
            # The root is just a file, so smoosh!
            result = Smoosher(root).smoosh()
            files_processed += 1
            total_originals += result[0]
            total_saved += result[1]
    
    print '--------------------'
    print 'EPIC WIN: Smooshed %i files, and cut %d%% bulk away (%i bytes)' % (
        files_processed,
        saving_percent(total_originals, total_saved),
        total_saved
    )

def main():
    args = sys.argv[1:]
    
    if not args:
        recursive_smoosher(os.getcwd())
    
    for arg in args:
        # Ensure all passed paths exist before we do anything
        assert os.path.exists(arg), u'%s does not exist' % arg
    
    recursive_smoosher(args)
    sys.exit(0)
