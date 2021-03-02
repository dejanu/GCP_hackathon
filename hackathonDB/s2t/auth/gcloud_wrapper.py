#!/usr/bin/env python3

from subprocess import Popen, PIPE
from txt2speech_tst import text_to_wav
#mine
from micreader import *

def run_cmd_once(intent_cmd):
    if isinstance(intent_cmd,str):
        intent_cmd_list=intent_cmd.split(" ")
        print(intent_cmd_list)
        process = Popen(intent_cmd,shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        print(stderr)
        return stdout


if __name__=="__main__":

    #gcloud iam service-accounts list
    #gcloud container clusters list --format='table(status)'
 
    cmd_result=run_cmd_once("kubectl get pods")
    if cmd_result:
        text_to_wav("en-AU-Wavenet-A",cmd_result)
        play_wavfile("en-AU.wav")
