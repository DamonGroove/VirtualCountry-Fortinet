This tool gets large IPv4 lists via webrequests and converts them into a custom geography address. 
There is a limitation of 65536[0-65535] ranges. 

The FortiGate API will be integrated soon for error checking and automating the config.


We simply build a geoip-override script using python.

https://help.fortinet.com/cli/fos60hlp/60/Content/FortiOS/fortiOS-cli-ref/config/system/geoip-override.htm
##########################
224.0.0.0 - 255.255.255.255 , 127.0.0.0 - 127.255.255.255 , 0.0.0.0 - 0.255.255.255 cannot be blocked !
##########################
