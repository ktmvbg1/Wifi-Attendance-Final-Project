from models import *

def add_device(session, user_id, mac_address, ip_address):
	device = session.query(device).filter_by(user_id=user_id, mac_address=mac_address).first()
	if device:
		return (False, 'device already exists')
	new_device = UserDevice(name = user_id, mac_address = mac_address, ip_address = ip_address)
	session.add(new_device)
	session.commit()
	return (True, "Created device {}".format(mac_address))

def get_devices(session, user_id):
	devices = session.query(UserDevice).filter_by(user_id=user_id)
	return devices

def check_device_exists(session, user_id, mac_address):
	device = session.query(UserDevice).filter_by(user_id = user_id, mac_address = mac_address).first()
	return device != None

def update_device(session, device_id, user_id = None, mac_address = None, ip_address = None):
	device = session.query(UserDevice).filter_by(id=device_id).first()
	if not device:
		return (False, 'Device does not exist')
	if user_id:
		device.user_id = user_id
	if mac_address:
		device.mac_address = mac_address
	if ip_address:
		device.ip_address = ip_address
	session.commit()
	return (True, "Updated {}".format(device_id))

def delete_device(session, device_id):
	device = session.query(UserDevice).filter_by(id=device_id).first()
	if not device:
		return (False, 'Device does not exist')
	session.delete(device)
	session.commit()
	return (True, "Deleted {}".format(device_id))