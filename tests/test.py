import urllib


link = 'https://raw.githubusercontent.com/FLAFLALEBG/Ultimate_Auto_Check_Services/origin/docs/help.txt'
f = urllib.urlopen(link)
myfile = f.readline()
print(myfile)

