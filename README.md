# Data_Stream and Subscriber Objects




## Quickstart

   
#### Instantiating Streams and Subscribers

A `Data_Stream` Object is instantiated with an optional but recommended id. :

```
    newStream = Data_Stream(ID = 'newStream')
```

A `Subscriber` Object is instantiated with an optional but recommended id, and an optional list of Data_Streams to subscribe to. For example:

```
    subscriber = Subscriber(ID = 'newSubscriber', data_streams = [stream])
    
```

#### Managing Subscriptions
To assign a callback function to a subscriber pass the `.manage_subscriptions` method a list of the Data_Streams to apply the call back to and a list of callback functions. For example:

```
    def call_back(stream_value):
        print('ping')
        
    subscriber.manage_subscriptions([stream],[call_back])
    
```
Now whenever a Data_stream is updated, the Subscriber callback will be triggered. It is also not necessary to pre-append a Data_Stream before adding callbacks. You can also assign multiple callbacks at once. For example:

```
    def do_something_else(stream_value):
        print('pong')
        
    other_stream = Data_Stream(ID = 'otherStream')
    
    subscriber.manage_subscriptions([other_stream],[call_back,do_something_else])
```

From now on, whenever each stream is updated, it will trigger a specific list of callback functions. Note they will be triggered in order of appendage. To update a Data_Stream, simply access it's `.data` property. For example:

```
    >>>other_stream.data = "Update"
    
    ping
    ping
    pong
```

To remove a callback function, use the `.manage_subscriptions` method in combination with the `'remove_func'` keyword and callback functions:

```
    >>>subscriber.manage_subscriptions(([other_stream],'remove_func',[callback])
    >>>other_stream.data = "Update"
    
    ping
    pong
```


To completely unsubscribe from a Data_Stream use the `.manage_subscriptions` method in combination with the `'remove'` keyword:

```

    >>>subscriber.manage_subscriptions(([stream],'remove')
    >>>other_stream.data = "Update"
    
    pong
```


## Working With Custom Objects

You can add more functionality by subclassing from Subscribers. Extending the `.notification_manager` method can help perform more complex operations with notifications. When a notification arrives it contains `notification` which is the updated `.data` attribute and `sender` which points to the Data_Stream object in memory.

```
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
```


```
    >>>land_area = Data_Stream('LAND AREA')
    >>>price_per_capita = Data_Stream('PRICE PER CAPITA')
```

```
    
    ESTATE WORTH now recieving updates from PRICE PER CAPITA
    
```
```

    >>>estate_worth = CustomSubscriber([price_per_capita,land_area],'ESTATE WORTH')
    
    ESTATE WORTH now recieving updates from LAND AREA
```
```
    >>>price_per_capita.data = 9785
    
    ESTATE WORTH now valued at £0.0
    
```
```
    >>>land_area.data = 60000
    
    ESTATE WORTH now valued at £587100000.0
```
