from pylxd import Clientclient = Client()client.authenticate('a-secret-trust-password')assert(client.trusted == True)def all():   containers =  client.containers.all()   return containersdef create():    config = {'name': 'my-container', 'source': {'type': 'none'}}    container = client.containers.create(config, wait=False)    container.devices = { 'root': { 'path': '/', 'type': 'disk', 'size': '7GB'} }    container.save()    return containerdef actionOnContainer(container, action):      if container:          if action == "start":              container.start()          if action == "freeze":              container.freeze()          if action == "delete":               container.delete()def createprofile():      profile = client.profiles.create(             'a-profile', config={'security.nesting': 'true'}, devices={'root': {'path': '/', 'size': '10GB', 'type': 'disk'}
