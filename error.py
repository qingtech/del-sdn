import sys
frame = sys._getframe()
code = frame.f_code
def report(fname, name, lineno, message):
	print 'file:%s,function:%s,line:%d\nmessage:%s'%(fname, name, lineno, message)
	exit(0)
if __name__ == '__main__':
	print 'hello'
	#report(sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno)
	#report(frame.f_code.co_filename, frame.f_code.co_name, frame.f_lineno)
	#report(code.co_filename, code.co_name, frame.f_lineno)
