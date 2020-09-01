# Ali Ben Tiba
# 2020
# ////////////#



#/////////////////////////#
###########################
######### CLASSES #########
###########################
#/////////////////////////#

class Subscription(object):
    def __init__(self,ID,address):
        self.methods = []
        self.ID = ID
        self.address = address
    def add_method(self,func):
        self.methods.extend(func)
    def list_methods(self):
        return [func.__name__ for func in self.methods]
    def remove_method(self,func):
        if func in self.methods:
            self.methods.remove(func)

class Data_Stream(object):
    """Data_stream object. can have multiple observers. Whenever its value changes 
    observers are notified via a call to one of their functions

        Methods:
    subscribe: subscribes to the Data_Stream instance's notifications.\n
    unsubscribe: unsubscribes from Data_Stream instance's notifications.

        Attributes:
    self.data: The current value of the object. Is sent to observers whenever it is changed
    """
    
    def __init__(self,ID = 'Data Stream'):
        """
        Instantiate with a user friendly ID string to recognise the data stream
        """
        self.__ID = ID
        self.__observers = {}
        self.__data = None

    @property
    def data(self):
        """Getter Method"""
        # print('accessing {} data'.format(self.__ID))
        return self.__data

    @data.setter
    def data(self, value):
        """Setter Method"""
        # print('setting {} data'.format(self.__ID))
        self.__data = value
        self.__notify_subscribers(self.__data)

    def subscribe(self, callback,subscriber_ID):
        """subscribes to Data_Stream instance's notifications.

            Args:
        callback: func: class function to call on update\n
        subscriber_ID: str: ID for observer class

            Returns:
        self.ID: datastream identifier\n
        self
        """
        print('{} now recieving updates from {}'.format(subscriber_ID,self.__ID))
        self.__observers[callback] = subscriber_ID
        return self.__ID,self
    
    def unsubscribe(self, callback):
        """unsubscribes from Data_Stream instance's notifications.

            Args:
        callback: func: class function to remove from callback list
        """
        print('{} succesfully unsubscribed from {}'.format(self.__observers[callback],self.__ID))
        del self.__observers[callback]

    def __notify_subscribers(self,notification):
        """Private Func. notifies subscribers of value 
        change via a callback function.

            Args:
        notification: self.attribute: attribute to update
        """
        for callback,observer_ID in self.__observers.items():
            # print('notifying: {}'.format(observer_ID))
            callback(notification,self)

class Subscriber(object):
    """
    Recieves notifications from Data_Stream object
    
        Methods:   
    manage_subscriptions(self,data_streams,add = True): Subscribes or unaubscribes to data streams\n
    notification_manager(self,notification,sender): handles notifications from data streams

        Attributes:
    notifications: history of all notifications from data_streams (read_only)
    ID: user friend;y identifier for the subscriber object
    subscriptions (read only) list of data streams to which the subscriber is subscribed
    """

    def __init__(self, data_streams = [],ID = 'Subscriber'):
        """
        __________
        
            Args:
        data_streams:list: list of data_stream objects\n
        ID: Instantiate with a user friendly ID string to recognise the subscriber"""
        self.ID = ID
        self.__data_streams = {}
        self.manage_subscriptions(data_streams)
        self.__notifications = []

    def __str__(self):
        return "\n{} Subscriber Object\nSubscribed to:\n {}".format(self.ID,'\n '.join(self.__data_streams.values()))

    def manage_subscriptions(self,data_streams,manager = 'add',functions = []):
        """
        Add or remove data_stream subscriptions from self.data_streams. default is to add

            Args:
        data_streams: list: list of Data_Stream objects to subscribe/unsubscribe to\n
        manager: str: 'add'-> add a new subscription(s) or add additional functions to a
        current subscription(s). 'remove' -> terminate a subscription 'remove_func' remove a
        function(s) from a current subscription(s)\n
        functions: list: list of functions to automatically call when a Data_Stream object notifies
        

        """

        if not isinstance(data_streams, list):
            data_streams = [data_streams]

        for stream in data_streams:
            if manager == 'add' and stream not in self.__data_streams.keys():
                ID,other = stream.subscribe(self._Subscriber__notification_manager,self.ID)
                self.__data_streams[other] = Subscription(ID,other)
                self.__data_streams[other].add_method(functions)
                
            elif stream in self.__data_streams.keys() and manager == 'remove':
                stream.unsubscribe(self._Subscriber__notification_manager)
                del self.__data_streams[stream]

            elif stream in self.__data_streams.keys() and manager == 'add':
                self.__data_streams[stream].add_method(functions)
                print('{} will now be called whenever {} updates'.format(' ,'.join(['<' + func.__name__ + '>' for func in functions]), self.__data_streams[stream].ID))
            elif stream in self.__data_streams.keys() and manager == 'remove_func':
                self.__data_streams[stream].remove_method(functions)
                print('{} will no longer be called from {}'.format(' ,'.join(['<' + func.__name__ + '>' for func in functions]),self.__data_streams[stream].ID))

            else:
                print('Not currently subscribed to {}'.format(stream))    

    @property
    def notifications (self):
        """Getter Method"""
        return self.__notifications
    @property
    def subscriptions (self):
        """Getter Method"""
        return [sub.ID for sub in self.__data_streams.values()]

    def get_subscription_functions(self,data_stream):
        """returns a list of functions that will be automatically be called when the
        input data stream sends a notification

            Args:
        data_stream: Data_Stream object
        """
        try:
            return self.__data_streams[data_stream].list_methods()
        except:
            print('{} is not subscribed to {}'.format(self.ID,data_stream))


    def __notification_manager(self, notification,sender = 'Unkown'):
        """PRIVATE METHOD: updates notification_value whenever it is called
        
            Args:
        notification: the updated value from the datastream\n
        sender: str: the sender address
        """
        self.__notifications.append([self.__data_streams[sender].ID,notification])
        # print("Update Recieved from {}".format(self.__data_streams[sender].ID))
        self.notification_manager(notification,self.__data_streams[sender])

        # execute subscription methods
        for method in self.__data_streams[sender].methods:
            method(notification)

    def notification_manager(self,notification,sender):
        """
        public method to handle notifications
        """
        pass

class CustomSubscriber(Subscriber):
    def __init__(self,data_stream,ID='Custom_Subscriber'):
        super().__init__(data_stream,ID)
        self.land_area = 0
        self.price_per_capita = 0
        self.units = '£'

        # if data_stream.data is not empty
        self.worth = 0
    


    def notification_manager(self, notification, sender='Unkown'):
        super().notification_manager(notification, sender=sender)
        if sender.ID == 'PRICE PER CAPITA':
            self.price_per_capita = notification
        elif sender.ID == 'LAND AREA':
            self.land_area = notification
        self.calculate_worth()
    
    def calculate_worth(self):
        self.worth = int(self.price_per_capita) * float(self.land_area)
        print('{} now valued at {}{}'.format(self.ID,self.units,self.worth))




# # EXAMPLE
# if __name__ == '__main__':
   
#     def print_something(*args):
#         print('something')

#     land_area = Data_Stream('LAND AREA')
#     price_per_capita = Data_Stream('PRICE PER CAPITA')
#     estate_worth = CustomSubscriber([price_per_capita,land_area],'ESTATE WORTH')
#     estate_worth.manage_subscriptions([land_area],functions=[print_something])
#     estate_worth.manage_subscriptions([land_area],'remove')
#     estate_worth.manage_subscriptions([price_per_capita],functions=[print_something])
#     estate_worth.manage_subscriptions(land_area)
#     estate_worth.manage_subscriptions([price_per_capita],'remove_func',[print_something])
#     price_per_capita.data = 9785
#     land_area.data = 60000
 


    