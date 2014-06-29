#!/usr/bin/python


#Function to process hyperlinks into 2nd level or 3rd level domains 
def load(line):
  #fault proof
  try:
      text = line.decode()
      page, id = text.split('\t')
      # remove http:// if there
      a = page.split("//")
      if len(a) == 1:
        b = a[0]
      else:
        b = a[1]
      #remove pages
      c = b.split("/")[0]
      #remove credentials
      d = c.split("@")
      if len(d) == 1:
        e = d[0]
      else:
        e = d[1]
      #strip www, ww2, etc
      f = e.split('.')
      if f[0][0:2] == 'ww':
        g = '.'.join(f[1:])
      else:
        g = e
      #leave only 3 sub-domains
      h = g.split('.')
      if len(h) > 3:
        l = '.'.join(h[-3:])
      else:
        l = g
      return l, id
  except:
    return 'domain error', '-1'