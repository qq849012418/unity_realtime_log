#coding=utf-8

COMMENT = """
 ##############################################
##                                            ##
##                                            ##
##                                            ##
 ##############################################
"""

import chardet
import platform
import time
import fileinput
import subprocess
import os
import sys
import _thread as thread
import time
import tail




def tail_thread(tail_file):

    print("wait for tail file ... %s" % tail_file)

    while True:
        if os.path.exists(tail_file):
            print( "Start tail file..... %s" % tail_file)
            break

    t = tail.Tail(tail_file)
    t.register_callback(unity_log_tail)
    t.follow(s=1)

def unity_log_tail(txt):
    print(txt)

def build(unity_path, project_path, log_path, input_path, output_path):
    """
    call unity process to build
    """

    build_cmd = [unity_path, '-silent-crashes','-batchmode', '-projectPath', project_path, '-nographics', '-executeMethod', 'WJGMain.import', '-logFile', log_path, '-quit', '-inputpath',input_path,'-outputpath',output_path]
    print( 'Unity running ....')

    if os.path.exists(log_path):
        os.remove(log_path)
        print( 'delete %s' % log_path)

    # new thread to tail log file
    thread.start_new_thread(tail_thread, (log_path, ))

    process = subprocess.Popen(
        build_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=project_path
    )

    while True:
        out = str(process.stdout.read(1),encoding='utf-8')
        if out == '' and process.poll() != None:
            break
        if out != '':
            print("[Unity process console output]: "+out,flush=True)

    time.sleep(5)
    print ('done!')





def fullpath(path):
    return os.path.abspath(os.path.expanduser(path))

if __name__ == '__main__':
    print (COMMENT)
    import argparse
    parser = argparse.ArgumentParser(description=u'Unity realtime log printing build!')

    parser.add_argument('-unity', required=True, help=u'Unity executable file path')
    parser.add_argument('-project', required=True, help=u'Unity project path')
    parser.add_argument('-input', required=True, help=u'Full Path of input model')
    parser.add_argument('-output', required=True, help=u'Save Path of bundle')

    args = parser.parse_args()
    build(fullpath(args.unity), fullpath(args.project), fullpath(os.path.join(args.project, '__keensterlog.txt')),fullpath(args.input),fullpath(args.output))
    #build(fullpath('D:\\Software\\Unity\\2019.4.0f1\\Editor\\Unity.exe'), fullpath('D:\\code\\unity\\PIXYZ2019CRACKTEST'), fullpath('D:\\code\\unity\\PIXYZ2019CRACKTEST\\__kellylog.txt'))
