import subprocess

try:
    subprocess.check_output(["./stderrecho", "blahha"], stderr=open("/tmp/seoseo", "w"), shell=True)
except:
    print "a"
print "b"
 
