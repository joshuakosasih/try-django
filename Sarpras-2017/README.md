# SarprasI

<br />

### Programming Language

<ul>
	<li>Python 2.7.x</li>
</ul>

-----

### Frameworks

-----

<ul>
	<li>Django 1.11b1</li>
	<li>AngularJS</li>
</ul>

-----

### Problems and Solutions

-----

**Prob:**
<b>django.db.utils.OperationalError: (1044, "Access denied for user ''@'localhost' to database 'sarpras_peminjamanruang'")</b>

**Solution:**
<ul>
	<li>Go to your project root directory</li>
	<li>Run <b>python tambahuser.py</b></li>
	<li>Go to MySQL prompt (mysql -u root)</li>
	<li>Run <b>SELECT host,user,password,Grant_priv,Super_priv FROM mysql.user;</b></li>
	<li>You should see the new user <b>admin_penjadwalan</b> with host <b>localhost</b></li>
	<li>If the value of Grant_priv or Super_priv is set to 'N', run this: <b>UPDATE mysql.user SET Grant_priv='Y', Super_priv='Y' WHERE User='admin_penjadwalan';</b></li>
	<li>Quit from the MySQL prompt. Execute <b>python manage.py runserver</b> and everything should be OK</li>
</ul>

---

**Prob:**
After the image requirement (for logo, etc) was added, you might encounter this issue:
<b>Cannot use ImageField because Pillow is not installed.</b>

**Solution:**
Just execute this command: pip install Pillow

---

**Prob:**
There were some additions for several models, such as the new fields called 'foto' and 'warna'.
When you're migrating, this problem might be encountered:
<b>django.db.utils.IntegrityError: (1062, "Duplicate entry '#FFFFFF' for key 'ruangan_ruangan_warna_529d0479_uniq'")</b>

**Solution:**
<ul>
<li>It is because you already have existing fields in the table 'ruangan'</li>
<li>Django asked you to provide default value for those existing fields, and in this case the default value is '#FFFFFF'. You can see this value in file with the name similar with '0004_ruangan_warna.py'</li>
<li>Delete those existing elements</li>
<li>Run <b>python manage.py migrate</b> and the process should be OK</li>
</ul>

