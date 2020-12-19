#! /usr/bin/env python3
import sys
import os


logFile = '/stockli.log'
oldLogFile = '/var/log/stockli.log.old'
LOGSIZE = 10000000

# check if log file needs to be rotated
if os.path.exists(logFile) and os.path.getsize(logFile) > LOGSIZE:
    if os.path.exists(oldLogFile):
        os.remove(oldLogFile)
    print("Rotating Log File")
    os.rename(logFile, oldLogFile)
    os.remove(logFile)


def helpString():
    help_string = '''
    Usage: ./stockli.py [OPTION]...

    Options:
     -h, --help                 prints this page and exits.
     -u, --update               checks for updates.
     -s [SYMBOL]                grabs relevant information for [SYMBOL]

    stockli is pre-pre-pre-pre-pre alpha and comes with NO WARRANTY.
    If you're seeing this, you probably shouldn't be. Shame on you.
    At this time functionality is incomplete and in development.
    '''
    print(help_string)
    return


if __name__ == '__main__':
    for i in range(1,len(sys.argv)):
        if (sys.argv[i] == '-h') or (sys.argv[i] == '--help'):
            helpString()
            break

        elif (sys.argv[i] == '-u') or (sys.argv[i] == '--update'):
            o = os.system('./update.sh')
            break

        elif (sys.argv[i] == '-s'):
            import utils.class_gen
            #close = round(utils.class_gen.Symbol(sys.argv[i+1]).lastClose,2)
            print(sys.argv[i+1] + ' closed at $' + str(round(utils.class_gen.Symbol(sys.argv[i+1]).lastClose,2)))
            break

        else:
            print('Specified option not recognized. Do main.py -h or --help for help.')
