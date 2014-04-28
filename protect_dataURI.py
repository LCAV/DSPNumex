
import sys

file_in = sys.argv[1]
file_out = sys.argv[2]

f = open(file_in,'r')
lines = f.readlines()
f.close()

newlines = []

prefix = '<img src="data:image/png;base64,'
suffix = '">'
fig_counter = 0

newprefix = 'document.getElementById(\'imgid\').setAttribute(\'src\','

is_dataURI = False
data = []

insert_index = -1

for i, line in enumerate(lines):

  # find end of header
  if line.find('</head>') != -1:
    insert_index = i

  # catch the data URI
  if not is_dataURI:

    if line[:len(prefix)] == prefix:
      is_dataURI = True
      fig_counter += 1
      data.append(line[len(prefix):-1])

    else:
      newlines.append(line)

  else:

    if not line[:len(suffix)] == suffix:
      data[-1] = data[-1] + line[:-1]

    else:
      newlines.append('<img id=\'figure' + str(fig_counter-1) + '\'>')
      is_dataURI = False

# add script in head section
# use insert instead of append
newlines.insert(insert_index,   '<script>\n')
newlines.insert(insert_index+1, '  window.onload = function() {\n')
for i in range(fig_counter):
  newlines.insert(insert_index+i+2, '    document.getElementById(\'figure' + str(i) + '\').setAttribute(\'src\',\'data:image/png;base64,' + data[i] + '\');\n')
newlines.insert(insert_index+fig_counter+2, '  }\n')
newlines.insert(insert_index+fig_counter+3, '</script>\n');

# write new file
f = open(file_out, 'w')
f.writelines(newlines)
f.close()


