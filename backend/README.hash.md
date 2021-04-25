import hashlib;

text = 'nowonbun';
binary = text.encode('utf-8');
enc = hashlib.md5();
enc.update(binary);
ret = enc.hexdigest();
print(ret);


import base64;
data = base64.b64encode(binary);
binary = base64.b64decode(data);
