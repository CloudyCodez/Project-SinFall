"""Exercise Hub profile switching using UI text, without screenshots or game input."""
import subprocess,time,xml.etree.ElementTree as ET,re
ADB='C:/Program Files (x86)/Android/android-sdk/platform-tools/adb.exe'
SERIAL='RFGL61DWL1F'
def adb(*args):return subprocess.check_output([ADB,'-s',SERIAL,*args],stderr=subprocess.STDOUT).decode('utf8','replace')
def nodes():
 adb('shell','uiautomator','dump','/data/local/tmp/hub-ui.xml')
 return list(ET.fromstring(adb('shell','cat','/data/local/tmp/hub-ui.xml')).iter('node'))
def click(label):
 candidates=[n for n in nodes() if n.get('text','').upper()==label.upper() and n.get('clickable')=='true']
 assert candidates,label
 bounds=list(map(int,re.findall(r'\d+',candidates[-1].get('bounds'))))
 adb('shell','input','tap',str((bounds[0]+bounds[2])//2),str((bounds[1]+bounds[3])//2))
def pid():return adb('shell','pidof','com.phoenix.sevends:server').strip()
click('Accounts');before=pid();assert before
click('Create Account')
entry=[n for n in nodes() if n.get('class')=='android.widget.EditText'][-1]
bounds=list(map(int,re.findall(r'\d+',entry.get('bounds'))))
adb('shell','input','tap',str((bounds[0]+bounds[2])//2),str((bounds[1]+bounds[3])//2))
adb('shell','input','text','QA_Profile');click('Create')
time.sleep(1)
assert any('QA_Profile' in n.get('text','') and 'Active' in n.get('text','') for n in nodes())
assert pid() and pid()!=before,'Server process did not restart'
qa=pid();click('Switch to Original account');time.sleep(1)
assert any('Original account' in n.get('text','') and 'Active' in n.get('text','') for n in nodes())
assert pid() and pid()!=qa
click('Delete QA_Profile');click('Delete')
assert not any('QA_Profile' in n.get('text','') for n in nodes())
click('Server')
assert any('Server running' in n.get('text','') for n in nodes())
print('PASS: account creation, independent server restart, switch back, confirmed scratch-account deletion; original account restored')
