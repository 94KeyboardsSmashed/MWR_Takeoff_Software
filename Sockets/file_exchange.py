import lightblue
import bluetooth 

  # known  
  target_name = "RPI"  
  file_to_send = "/MWR_TAKEOFF_SOFTWARE/loggnd.txt"  
    
  # unknown  
  obex_port = None                 
  target_address = None  
    
  print "searching for nearby devices..."  
  nearby_devices = bluetooth.discover_devices()  
    
  for bdaddr in nearby_devices:  
    print bluetooth.lookup_name( bdaddr )  
    if target_name == bluetooth.lookup_name( bdaddr ):  
       print "found the target device!"  
      target_address = bdaddr  
      break  
    
  print "searching for the object push service..."  
  services = lightblue.findservices(target_address)  
  for service in services:  
       if service[2] == "OBEX Object Push":  
            obex_port = service[1]       
            print "OK, service '", service[2], "' is in port", service[1], "!"  
            break  
    
  print "sending a file..."  
  try:  
       lightblue.obex.sendfile( target_address, service[1], file_to_send )  
       print "completed!\n"  
  except:  
       print "an error occurred while sending file\n"