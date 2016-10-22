This is a collection of snippets, libraries, scripts, etc, mostly culled from gists by people way smarter than me. If I failed to add a reference link in any of these scripts, please let me know and I will gladly do so.

Originally the ideas was to create a single module called 'pyfacts' that could be imported into existing projects. While this is still possible, I've abandonded that original intent and am using this repo for experimentation instead.

pyfacts.py
=======

This script returns all or specified facts about your Mac.

Standalone
----------
Use pyfacts.py as a standalone script:

	./pyfacts.py [key]

Run with no arguments to return all facts:

	./pyfacts.py

Use the list argument to see all available keys:

	./pyfacts.py -l

Module
------
Import the module into your python script:

	from pyfacts import Facts

	fact = Facts()
	serial = fact.get_serial()
	print serial

License
-------

	Copyright 2016 Joseph Chilcote
	
	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at
	
		http://www.apache.org/licenses/LICENSE-2.0
	
	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.
