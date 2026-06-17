import os
import sys
sys.stderr = open(os.devnull, 'w')
a = 'a'
b = 1
print(a + b)


{
	"servers": {
		"cash-gift-server":{
			"command": "/home/pc/Documents/projects/mcp_server/venv/bin/python3",
			"args": ["/home/pc/Documents/projects/mcp_server/cash_gift.py"]

		}
	}
}