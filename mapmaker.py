from easygui import *
import sys

while 1:
  msgbox("Map Maker")

  choice = ''

  if ynbox("Open a file?","LoadFile"):
    choice = fileopenbox("","Load File","*",["*.txt"])
  else:
    sys.exit(0)           # user chose Cancel

  codebox( '', choice, open(choice).read() )

