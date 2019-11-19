With FortiOS 5.6 and 6.0, to create a large custom list of IPs that can be used as an address object,
you need to create address objects for each subnet and assign, at most, 300(For lower-end models)
objects per address group. There's also a max of 5000 address objects for lower-end models. If you're using a
large granular list or several lists you might run into some serious issues. To simplify things I
built this tool using the system geoip-override. Since you can add up to 65,000+ ranges per custom geography address
and create a single address object for a geography address, address object limitations are of no concern here.
IPv4 addressing is used in this tool.

The FortiGate API will be integrated soon to automate things.


We simply build a geoip-override script using python.

https://help.fortinet.com/cli/fos60hlp/60/Content/FortiOS/fortiOS-cli-ref/config/system/geoip-override.htm
##########################
224.0.0.0 - 255.255.255.255 , 127.0.0.0 - 127.255.255.255 , 0.0.0.0 - 0.255.255.255 cannot be blocked !
##########################


config system geoip-override
    edit {name}
    # Configure geographical location mapping for IP address(es) to override mappings from FortiGuard.
        set name {string}   Location name. size[63]
        set description {string}   Description. size[127]
        set country-id {string}   Two character Country ID code. size[2]
        config ip-range
            edit {id}
            # Table of IP ranges assigned to country.
                set id {integer}   ID number for individual entry in the IP-Range table. range[0-65535]
                set start-ip {ipv4 address}   Starting IP address, inclusive, of the address range (format: xxx.xxx.xxx.xxx).
                set end-ip {ipv4 address}   Final IP address, inclusive, of the address range (format: xxx.xxx.xxx.xxx).
            next
    next
end