# About Box
import wx
import wx.html
class SketchAbout(wx.Dialog):
     
     text = '''
<html>
<body bgcolor="#ACAA60">
<center><table bgcolor="#455481" width="100%" cellspacing="0"
cellpadding="0" border="1">
<tr>
     <td align="center"><h1>PyBase!</h1></td>
</tr>
</table>
</center>
<p><b>PyBase</b> is a wrapper software for
<b>database management.</b>
It is based on Python programming language and its API
for MySQL database.
</p>
<p><b>MySQl</b> and <b>Python</b> are brought together for providing
<b>User Interface</b> and <b>Efficient Database Management</b></p>
<p>
Creator : Arun Kumar Muralidharan
          (2009 Sept-Oct).  </p>
<p>Email : arun11299@gmail.com</p>
</body>
</html>
'''
     def __init__(self, parent):
          wx.Dialog.__init__(self, parent, -1, 'About Sketch',\
                           size=(440, 400) )
          html = wx.html.HtmlWindow(self)
          html.SetPage(self.text)
          button = wx.Button(self, wx.ID_OK, "Okay")
          sizer = wx.BoxSizer(wx.VERTICAL)
          sizer.Add(html, 1, wx.EXPAND|wx.ALL, 5)
          sizer.Add(button, 0, wx.ALIGN_CENTER|wx.ALL, 5)
          self.SetSizer(sizer)
          self.Layout()
def main():
     dialog = SketchAbout(None)
     dialog.Show(True)
