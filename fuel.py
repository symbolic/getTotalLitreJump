#-*- coding:utf-8 -*-
import string
import sys
import os

def check_usage():
    print '\n' + '用途：从Fuel日志文件中，找到特定枪号的泵码跳变，定位故障时间'.decode('utf-8')+'\n'
    if len(sys.argv) != 3:
        print '\n用法：可执行文件   fule日志文件   （10进制）枪号'.decode('utf-8')
        sys.exit()

def getValidLine():
    prefix = 'PAKReadyTransaction2 - PumpID='
    key = prefix + sys.argv[2]
    src = open(sys.argv[1], 'r')
    dest = open('dest_'+sys.argv[2]+'.txt', 'w')
    oneline = src.readline()

    while oneline:
        if key in oneline:
            dest.write(oneline)

        oneline = src.readline()

    src.close()
    dest.close()

def getVolTotal():
    src = open('dest_'+sys.argv[2]+'.txt', 'r')
    dest = open('result_'+sys.argv[2]+'.txt', 'w')
    isFirstLine = True
    lastLineCurrentVolCurrent = 0       #前一行当前累计

    oneline = src.readline()
    print '*'*20 + '\n'
    dest.write('*'*20 + '\n')
    while oneline:
        if len(oneline) > 10:
            currentVol = oneline.split('lVolume=')[1].split(', lValue=')[0]
            lastVolTotal = oneline.split('SCounter=')[1].split(', ECounter=')[0]
            currentVolTotal = oneline.split('ECounter=')[1][:-3]
            currentVolDec = string.atoi(currentVol)         #本行加油量
            lastVolTotalDec = string.atoi(lastVolTotal)     #本行加油前累计
            currentVolTotalDec = string.atoi(currentVolTotal)   #本行加油后累计

            if isFirstLine:
                lastLineCurrentVolCurrent = lastVolTotalDec
                isFirstLine = False

            if currentVolTotalDec != (lastVolTotalDec+currentVolDec):
                print ''+'当次加油累计有误'.decode('utf-8')
                print '\n'+'加油前累计：'.decode('utf-8') + lastVolTotal
                print '\n'+'加油量：'.decode('utf-8') + currentVol
                print '\n'+'加油后累计：'.decode('utf-8') + currentVolTotal
                print '\n'+'差额：'.decode('utf-8') + str(currentVolTotalDec-lastVolTotalDec-currentVolDec)
                print '\n' + oneline
                print '*'*20 + '\n'

                dest.write(''+'当次加油累计有误')
                dest.write('\n'+'加油前累计：' + lastVolTotal)
                dest.write('\n'+'加油量：' + currentVol)
                dest.write('\n'+'加油后累计：' + currentVolTotal)
                dest.write('\n'+'差额：' + str(currentVolTotalDec-lastVolTotalDec-currentVolDec))
                dest.write('\n' + oneline + '*'*20 + '\n')


            if lastLineCurrentVolCurrent != lastVolTotalDec:
                print ''+'泵码跳变'.decode('utf-8')
                print '\n'+'上一行加油后累计：'.decode('utf-8') + str(lastLineCurrentVolCurrent)
                print '\n'+'本行加油前累计：'.decode('utf-8') + str(lastVolTotalDec)
                print '\n'+'差额：'.decode('utf-8') + str(lastVolTotalDec - lastLineCurrentVolCurrent)
                print '\n' + oneline
                print '*'*20 + '\n'

                dest.write(''+'泵码跳变')
                dest.write('\n'+'上一行加油后累计：' + str(lastLineCurrentVolCurrent))
                dest.write('\n'+'本行加油前累计：' + str(lastVolTotalDec))
                dest.write('\n'+'差额：' + str(lastVolTotalDec - lastLineCurrentVolCurrent))
                dest.write('\n' + oneline + '*'*20 + '\n')

            lastLineCurrentVolCurrent = currentVolTotalDec
            #print currentVolTotal

        oneline = src.readline()


    src.close()
    dest.close()

def finish():
    print '+'+'-'*50+'+\n'
    print ' '*10+'分析完毕，请查看 '.decode('utf-8')+'result_'+sys.argv[2]+'.txt '+'文件'.decode('utf-8')+'\n'
    print '+'+'-'*50+'+'


if __name__ == '__main__':
    check_usage()
    getValidLine()
    getVolTotal()
    finish()
